# check_one.py
import os, sys, os.path as osp
os.environ.setdefault("PV_MODEL_PATH", r"ai\waste_v1\validity_classifier.onnx")
os.environ.setdefault("PV_CLASS_MAP_PATH", r"ai\waste_v1\class_map.json")

from ai.verifier import Verifier
v = Verifier()

if len(sys.argv) < 2:
    print("Usage: python check_one.py path\\to\\image.jpeg")
    sys.exit(1)

img_path = sys.argv[1]
if not osp.isfile(img_path):
    print("File not found:", img_path)
    sys.exit(1)

out = v.score(img_path, existing_phashes=[])
print(osp.basename(img_path), "→", out["ai_label"],
      f"(rel={out['relevance_score']:.2f}, action={out['action_score']:.2f}, backend={out['model_version']})")
