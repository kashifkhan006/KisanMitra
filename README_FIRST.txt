KISANMITRA VERCEL STARTER — READ FIRST

This is a separate deployment project. It does not replace your original Streamlit app.

ALREADY INCLUDED:
- Green bilingual (English/Hindi) website with image upload and prediction display
- Flask API endpoint at api/index.py
- inference.py (supports config key image_size or img_size)
- disease_info.py from the compatible project
- models/crop_model.keras (9.29 MB)

YOU MUST COPY THESE TWO FILES FROM YOUR GOOGLE DRIVE MODEL FOLDER:
models/class_indices.json
models/config.json

Source folder in Drive:
MyDrive/KisanMitra/crop_disease_predictor/models/
Copy the two exact files into this project's models/ folder. Do not create guessed class labels.
Your config.json can contain "image_size": 224; inference.py supports that.

LOCAL TEST (Windows PowerShell, Python 3.10 or 3.11 recommended):
1. Install Python 3.11 if not installed.
2. Open this folder in PowerShell.
3. py -3.11 -m venv .venv
4. .venv\Scripts\Activate.ps1
5. python -m pip install --upgrade pip
6. pip install -r requirements.txt
7. python -m flask --app api.index run --debug
8. Open http://127.0.0.1:5000

DEPLOYMENT CAUTION:
Vercel Python functions have deployment/package and request-size constraints. TensorFlow is a large dependency and may fail to build or exceed Vercel's function bundle limit. This project is prepared for a deployment attempt, not a guarantee that TensorFlow inference will fit Vercel's current limits. If deployment fails because of TensorFlow size/runtime constraints, keep this frontend on Vercel and move /api/predict inference to a Python host that supports TensorFlow (e.g. a container service), then point the frontend to that API. Image uploads are limited to 4 MB in this project.

PREDICTION SAFETY:
A model score is not the same as verified field accuracy. Validate with held-out real leaf images and confirm serious crop issues with a local agricultural officer/KVK. The app gives educational guidance, not a definitive diagnosis.
