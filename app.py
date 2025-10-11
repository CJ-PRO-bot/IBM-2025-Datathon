import os
import uuid
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from PIL import Image
import numpy as np
from sqlalchemy import desc

from models import db, User, Submission, Message

# Pluggable AI verifier (pHash + EXIF + model/ONNX or heuristic fallback)
from ai.verifier import Verifier
verifier = Verifier()

# ----------------------------
# Flask config
# ----------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)

app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# ----------------------------
# Image helpers
# ----------------------------
TARGET_H, TARGET_W, TARGET_C = 224, 224, 3
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def unique_filename(original: str) -> str:
    base = secure_filename(os.path.splitext(original)[0]) or "upload"
    ext = os.path.splitext(original)[1].lower()
    return f"{base}-{uuid.uuid4().hex[:8]}{ext}"

# ----------------------------
# Lightweight heuristic (utility used by verifier's internal copy if needed)
# ----------------------------
HEURISTIC_FLOOR  = float(os.getenv("PV_HEURISTIC_FLOOR", "0.08"))

def image_entropy(arr01: np.ndarray) -> float:
    """Entropy of grayscale histogram (0-1 normalized)."""
    gray = (0.299*arr01[...,0] + 0.587*arr01[...,1] + 0.114*arr01[...,2]).astype(np.float32)
    hist, _ = np.histogram(gray, bins=32, range=(0.0, 1.0), density=True)
    hist = hist + 1e-8
    ent = -np.sum(hist * np.log2(hist))
    ent_norm = ent / np.log2(32)  # normalize to 0..1
    return float(max(0.0, min(1.0, ent_norm)))

def heuristic_score(path: str, report_type: str = "illegal_dumping") -> float:
    """
    Score 0..1: higher => more likely 'real outdoor/waste'.
    """
    img = Image.open(path).convert("RGB").resize((320, 320))
    arr = np.asarray(img, dtype=np.float32) / 255.0

    R, G, B = arr[...,0], arr[...,1], arr[...,2]
    gray = (0.299*R + 0.587*G + 0.114*B)

    # --- Gradients / edges ---
    gx = np.abs(np.diff(gray, axis=1))  # (320,319)
    gy = np.abs(np.diff(gray, axis=0))  # (319,320)
    H = min(gx.shape[0], gy.shape[0]); W = min(gx.shape[1], gy.shape[1])
    mag = np.sqrt(gx[:H,:W]**2 + gy[:H,:W]**2)
    edge_thr = np.percentile(mag, 60)
    edge_density = float((mag > edge_thr).mean())

    # Straight edges (roads/bins)
    row_energy = float(np.mean(gx))
    col_energy = float(np.mean(gy))
    straightness = min(1.0, 4.0 * (0.5*(row_energy + col_energy)))

    # Outdoor colors + saturation
    maxc = np.maximum(np.maximum(R, G), B)
    minc = np.minimum(np.minimum(R, G), B)
    sat = np.where(maxc > 0, (maxc - minc) / (maxc + 1e-6), 0.0)
    mean_sat = float(np.mean(sat))
    greenish = (G > R) & (G > B) & (G > 0.28)
    brownish = (R > 0.28) & (G > 0.20) & (B < 0.38) & (R > B)
    outdoor_ratio = float((greenish | brownish).mean())

    # Forest/animal penalty (capped)
    forest_penalty = 0.0
    if outdoor_ratio > 0.20 and mean_sat > 0.30 and edge_density < 0.12:
        forest_penalty = min(0.10, 0.5*outdoor_ratio + 0.5*mean_sat)

    # Dark areas (bags/asphalt/containers)
    dark_ratio = float((gray < 0.28).mean())

    # "Trash cue": dark & edged pixels together
    dark_mask = (gray[:H,:W] < 0.28)
    edge_mask = (mag > np.percentile(mag, 70))
    trash_cue = float((dark_mask & edge_mask).mean()) * 1.5

    # Entropy
    ent = image_entropy(arr)

    base = (
        0.30 * edge_density +
        0.18 * straightness +
        0.14 * outdoor_ratio +
        0.18 * dark_ratio +
        0.12 * ent +
        0.08 * trash_cue
    )

    if report_type == "illegal_dumping":
        base += 0.05

    score = base - forest_penalty
    score = max(HEURISTIC_FLOOR, min(1.0, score))

    print(
        "[HEURISTIC DEBUG] "
        f"edges={edge_density:.3f} straight={straightness:.3f} "
        f"outdoor={outdoor_ratio:.3f} dark={dark_ratio:.3f} "
        f"trashcue={trash_cue:.3f} ent={ent:.3f} "
        f"penalty={forest_penalty:.3f} -> score={score:.3f}"
    )

    return float(score)

# ----------------------------
# Auth
# ----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username", "").strip()
        e = request.form.get("email", "").strip().lower()
        pw = request.form.get("password", "")
        if not u or not e or not pw:
            flash("All fields are required.")
            return redirect(url_for("register"))
        if User.query.filter((User.username == u) | (User.email == e)).first():
            flash("Username or email already exists.")
            return redirect(url_for("register"))
        user = User(username=u, email=e, password_hash=generate_password_hash(pw), role="user")
        db.session.add(user); db.session.commit()
        flash("Registered. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ident = request.form.get("identifier", "").strip()
        p = request.form.get("password", "")
        user = User.query.filter_by(username=ident).first()
        if not user:
            user = User.query.filter_by(email=ident.lower()).first()
        if user and check_password_hash(user.password_hash, p):
            login_user(user)
            nxt = request.args.get("next")
            return redirect(nxt or url_for("index"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

# ----------------------------
# User: upload + message (+ report type)
# ----------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        report_type = request.form.get("report_type", "illegal_dumping")
        f = request.files.get("photo")
        msg = request.form.get("message", "").strip()

        if not f or f.filename == "":
            flash("No file selected.")
            return redirect(url_for("index"))
        if not allowed_file(f.filename):
            flash("Unsupported file type. Please upload an image.")
            return redirect(url_for("index"))

        fname = unique_filename(f.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
        f.save(path)

        # --- New: use pluggable verifier (pHash + EXIF + model/ONNX or heuristic)
        recent = Submission.query.order_by(desc(Submission.created_at)).limit(200).all()
        existing = [(s.id, getattr(s, "phash", None)) for s in recent if getattr(s, "phash", None)]
        scores = verifier.score(path, existing_phashes=existing)

        sub = Submission(
            user_id=current_user.id,
            report_type=report_type,
            image_path=os.path.relpath(path, app.root_path).replace("\\", "/"),

            # legacy fields (kept for backwards compatibility in templates)
            ai_label=scores["ai_label"],
            ai_score=scores["action_score"],       # show action score in old slot

            status=scores["status"],

            # smart verifier fields
            phash=scores["phash"],
            duplicate_of=scores["duplicate_of"],
            exif_time_ok=scores["exif_time_ok"],
            action_score=scores["action_score"],
            auth_score=scores["auth_score"],
            relevance_score=scores["relevance_score"],
            model_version=scores["model_version"]
        )
        db.session.add(sub); db.session.commit()

        if msg:
            m = Message(submission_id=sub.id, sender_id=current_user.id, body=msg)
            db.session.add(m); db.session.commit()

        return redirect(url_for("result", sid=sub.id))

    return render_template("index.html")

@app.route("/result/<int:sid>")
@login_required
def result(sid):
    sub = Submission.query.get_or_404(sid)
    if sub.user_id != current_user.id and current_user.role != "admin":
        flash("Not authorized")
        return redirect(url_for("index"))

    # pass env-driven knobs to the template so you can see what decided the outcome
    cutoff = float(os.getenv("PV_ACTION_CUTOFF", "0.50"))
    dup_disabled = os.getenv("PV_DISABLE_DUP_PENALTY", "0") == "1"
    dup_penalty = float(os.getenv("PV_DUP_PENALTY", "0.40"))

    return render_template(
        "result.html",
        submission=sub,
        cutoff=cutoff,
        dup_disabled=dup_disabled,
        dup_penalty=dup_penalty,
    )

# ----------------------------
# Admin
# ----------------------------
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin only")
            return redirect(url_for("index"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/admin")
@login_required
@admin_required
def admin_home():
    auto_ok = Submission.query.filter_by(status="AUTO_OK").order_by(Submission.created_at.desc()).all()
    rechecks = Submission.query.filter_by(status="RECHECK").order_by(Submission.created_at.desc()).all()
    return render_template("admin_dashboard.html", auto_ok=auto_ok, rechecks=rechecks)

@app.route("/admin/mark/<int:sid>/<string:new_status>", methods=["POST"])
@login_required
@admin_required
def admin_mark(sid, new_status):
    sub = Submission.query.get_or_404(sid)
    if new_status not in ["AUTO_OK", "RECHECK"]:
        flash("Invalid status")
        return redirect(url_for("admin_home"))
    sub.status = new_status
    db.session.commit()
    return redirect(url_for("admin_home"))

@app.route("/message/<int:sid>", methods=["POST"])
@login_required
def post_message(sid):
    sub = Submission.query.get_or_404(sid)
    if sub.user_id != current_user.id and current_user.role != "admin":
        flash("Not authorized")
        return redirect(url_for("index"))
    body = request.form.get("body", "").strip()
    if body:
        m = Message(submission_id=sid, sender_id=current_user.id, body=body)
        db.session.add(m); db.session.commit()
    return redirect(url_for("result", sid=sid))

if __name__ == "__main__":
    # Ensure DB tables exist on first run
    with app.app_context():
        db.create_all()
    app.run(debug=True)
