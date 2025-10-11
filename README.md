# IBM Z Datathon 2025
## HeeboAI - "Community-Driven Solution to Tackle Waste Problem"

## Problem Statement
Everyone has a phone—so reporting should be “see waste → take photo → submit.” Yet communities still lack this practice. Illegal dumping and litter persist because today’s reporting pipeline lacks trusted, timely visibility. Installing cameras or placing officials everywhere isn’t feasible, making areas prone to waste hotspots and land degradation. This slows response, raises costs, and lets problems worsen. Such problems directly contribute to land pollution, water pollution, etc. that have direct affect in agriculture production, and enhance global warming that can lead to great catastrophe. Without fast, reliable image authentication (time, place, relevance), admins hesitate to dispatch teams. Genuine reports blend with spam, eroding trust. Volunteers who clean up get inconsistent recognition, lowering motivation and participation. Schools and community groups struggle to show verified impact, weakening accountability and funding. The absence of a consistent, auditable way to validate and prioritize proof distorts cleanliness maps and resource planning—like bin placement or patrol routes—leading to misallocated budgets. Communities have the will and the cameras, but not a dependable, low-friction verification and crediting pathway. The result? Slower action, wasted effort, and preventable waste persisting in public spaces.

## Solution Statement
Everyone has a phone, so reporting stays tap-simple. Behind that, an AI pipeline verifies authenticity, removes duplicates, and triages by confidence: high-confidence dirty goes straight to Action Now, unclear cases to Re-check with AI tips to retake better evidence. We prioritize recall—so real litter or waste hotspots doesn’t slip through, and immediate action can be taken—and we back that with threshold tuning from our PR curve. Admins get hotspot maps, photos of people littering, or doing volunteering work, to make sure actions and recognitions are given in a transparent manner. Our AI detects spam reports with the authentic ones, ensuring smooth workflow and immediate response. 
Participation in community works isn’t just about doing it for sake now: our AI keep tracks of useful, verified reports, powering fair recognitions by the admins keeping them motivated and active.  

Net result: phone-simple reporting, AI-authenticated proof, faster cleanups, actions and recognitions, ensuring visible and motivated community momentum.

## Audience
1.	Citizens & Students (Primary Reporters) – Use their phones to snap and submit waste/dumping photos; get AI-verified credit, points, badges, and leaderboard rank that mirrors familiar social-media attention mechanics (recognition replaces likes/followers).
2.	Teachers, Club Leaders & School Coordinators – Run weekly cleanup drives; rely on AI-authenticated photo attendance/proof, auto-compiled reports, and fair scoring to motivate sustained participation.
3.	Municipal Admins / City Operations – Receive an auto-triaged evidence queue (valid/re-check), hotspot maps, and action logs to dispatch crews faster, track SLAs, and allocate budgets efficiently.
4.	Enforcement Officers (Municipal/Police) – Access tamper-checked evidence bundles (time, location, duplicates) to act on illegal dumping with confidence and due process.
5.	Local Government Planners & Policy Makers – Use verified heatmaps and trend dashboards to plan bin placement, schedule patrols, and evaluate policy impact over time.
   
.
├─ app.py
├─ models.py
├─ ai/
│  ├─ verifier.py
│  └─ waste_v1/
│     ├─ validity_classifier.onnx        # <-- put model here
│     └─ class_map.json                  # <-- label map
├─ templates/                            # Jinja2 HTML
├─ static/                               # css/js + uploads/
├─ instance/                             # SQLite DB & instance files (gitignored)
├─ requirements.txt
└─ README.md/>

## Some Insights from the Jupyter Notebook that we found useful!
<img width="1810" height="933" alt="Screenshot 2025-10-11 151408" src="https://github.com/user-attachments/assets/30d11385-cec1-48bc-a578-91d181f7ab2e"/>
<img width="1852" height="973" alt="Screenshot 2025-10-11 151444" src="https://github.com/user-attachments/assets/2eeb9eeb-0559-4811-8161-6ebf83425879" />
<img width="1856" height="980" alt="Screenshot 2025-10-11 151557" src="https://github.com/user-attachments/assets/48558af9-4629-4577-a33a-de7962d22223" />
<img width="1857" height="979" alt="Screenshot 2025-10-11 151631" src="https://github.com/user-attachments/assets/940deadf-0fd5-43ae-aa3b-5937ba58f0dd" />




