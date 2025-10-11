# IBM Z Datathon 2025
## HeeboAI - "Community-Driven Solution to Tackle Waste Problem"

## Problem Statement
Unmanaged waste continues to fuel climate change as dumps emit methane and greenhouse gases, accelerating global warming. Plastic and toxic waste contaminate soil and water, damaging farmland and reducing crop quality, while communities lack efficient systems to monitor or prevent illegal dumping, making the crisis largely invisible. Manual cleanup reporting is slow, unreliable, and often falsified with unrelated or outdated photos, resulting in wasted resources, inaccurate data, and poor policy decisions that demotivate genuine volunteers who are not fairly recognized. Despite thousands of students, citizens, and volunteers contributing weekly to community cleanups, their real impact remains invisible and unrewarded due to the absence of transparent acknowledgment. Furthermore, the lack of a unified digital platform prevents communities and administrators from tracking verified activities, leading to inefficient waste programs and weak civic engagement. As a result, good initiatives fail to gain momentum, waste continues to pile up, and the combined effects harm the climate, public health, and agriculture — losing the opportunity to transform local volunteer efforts into a national movement for sustainability.

#### “Fake reports, lost recognition, and untracked waste activities weaken our fight against climate change — while real volunteers remain unseen.”

<img width="1600" height="864" alt="eee" src="https://github.com/user-attachments/assets/6d6e062d-7034-4a4d-9289-d4e6480ef70d" />
As shown in the flow chart, admin priortize valid photos, checking the authentic ones, and then the recheck_photos saving time and energy, while ensuring immediate response to the authenticated reports. 

## Solution Statement
Everyone has a phone, so reporting stays tap-simple. Behind that, an AI pipeline verifies authenticity, removes duplicates, and triages by confidence: high-confidence "dirty" goes straight to "Action Now", unclear cases to "Re-check" with AI tips to retake better evidence. We prioritize recall—so real litter or waste hotspots doesn’t slip through, and immediate action can be taken—and we back that with threshold tuning from our PR curve. Admins get hotspot maps, photos of people littering, or doing volunteering work, to make sure actions and recognitions are given in a transparent manner. Our AI detects spam reports with the authentic ones, ensuring smooth workflow and immediate response. 
Participation in community works isn’t just about doing it for sake now: our AI keep tracks of useful, verified reports, empowering individuals with fair recognitions by the admins through the convinient and visibility provided by the AI (leveraging the public people who can take photos and report to admins via mobile phone) keeping them motivated and active to contribute to their own clean environment.

#### “Our AI empowers every citizen and student to fight climate change — by turning every verified cleanup photo into measurable action for a cleaner, greener, and happier planet.” 

Net result: phone-simple reporting, AI-authenticated proof, faster cleanups, actions and recognitions by community leaders, ensuring visible and motivated community momentum.

## Target Audience
1.	Citizens & Students (Primary Reporters) – Use their phones to snap and submit waste/dumping photos; get AI-verified badges, by admins through leaderboard rank that mirrors familiar social-media attention mechanics (recognition replaces likes/followers, motivating individuals).
2.	Teachers, Club Leaders & School Coordinators – Run weekly cleanup drives; rely on AI-authenticated photo attendance/proof, auto-compiled reports, and fair scoring to motivate sustained participation.
3.	Municipal Admins / City Operations – Receive an auto-triaged evidence queue (valid/re-check), hotspot maps, and action logs to dispatch crews faster, track SLAs, and allocate budgets efficiently.
4.	Enforcement Officers (Municipal/Police) – Access tamper-checked evidence bundles (time, location, duplicates) to act on illegal dumping with confidence and due process.
5.	Local Government Planners & Policy Makers – Use verified heatmaps and trend dashboards to plan bin placement, schedule patrols, and evaluate policy impact over time.

## Datasets
Balanced binary image set: dirty_places vs invalid. We curated positives from Kaggle’s TACO Trash (kneroma/tacotrashdataset), Clean/Dirty Road (faizalkarim/cleandirty-road-classification), and Clean/Dirty Garbage (mfadliramadhan/cleandirtygarbage). Negatives reflect real spam/noise using Meme Images (hammadjavaid/6992-labeled-meme-images-dataset), Animals-10 (alessiocorrado99/animals10), Icons-50 (danhendrycks/icons50), and Selfies (jigrubhatt/selfieimagedetectiondataset). All images were EXIF-corrected, resized to 224×224, and split train ~2.4k / val ~0.6k (near-balanced) for fast CPU training on IBM LinuxONE.

## Leveraging the IBM-Z technology to the solution:
IBM LinuxONE (IBM Z) provided an interactive, secure cloud console with robust compute and rich Python packages that simplified our workflow and sped up experimentation. In 24 hours we curated data, trained, and validated a validity classifier for community waste photos, reaching ~83% accuracy with dirty-class recall 0.89, supported by ROC/PR curves. LinuxONE’s stable CPUs, ample memory, and fast I/O let us iterate quickly and save reproducible artifacts (confusion matrix/ROC/PR/class metrics and metrics.json) to a shared path for the team. The platform also made it easy to integrate data sources, perform batch feature extraction, and keep an auditable record of runs—ideal for civic deployments. Next, we’ll use the same environment to add an active-learning loop (admin feedback → periodic retrain) and to harden thresholds for recall-first triage in production.

## Some Insights from the Jupyter Notebook that we found useful!
<img width="1810" height="933" alt="Screenshot 2025-10-11 151408" src="https://github.com/user-attachments/assets/30d11385-cec1-48bc-a578-91d181f7ab2e"/>
<img width="1852" height="973" alt="Screenshot 2025-10-11 151444" src="https://github.com/user-attachments/assets/2eeb9eeb-0559-4811-8161-6ebf83425879" />
<img width="1856" height="980" alt="Screenshot 2025-10-11 151557" src="https://github.com/user-attachments/assets/48558af9-4629-4577-a33a-de7962d22223" />
<img width="1857" height="979" alt="Screenshot 2025-10-11 151631" src="https://github.com/user-attachments/assets/940deadf-0fd5-43ae-aa3b-5937ba58f0dd" />


