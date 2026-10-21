"""Model loading, upload validation and prediction for KisanMitra."""
import io, json
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
BASE = Path(__file__).parent
MODEL_PATH = BASE / "models" / "crop_model.keras"
CLASSES_PATH = BASE / "models" / "class_indices.json"
CONFIG_PATH = BASE / "models" / "config.json"
ALLOWED_EXT = {".jpg", ".jpeg", ".png"}
MAX_FILE_MB = 4
MIN_SIDE = 64
Image.MAX_IMAGE_PIXELS = 50_000_000

def model_files_exist():
    return all(p.exists() for p in (MODEL_PATH, CLASSES_PATH, CONFIG_PATH))

@lru_cache(maxsize=1)
def load_assets():
    import tensorflow as tf
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    with open(CLASSES_PATH, encoding="utf-8") as f: mapping = json.load(f)
    if mapping and all(str(k).isdigit() for k in mapping):
        idx_to_class = {int(k): str(v) for k, v in mapping.items()}
    else:
        idx_to_class = {int(v): str(k) for k, v in mapping.items()}
    with open(CONFIG_PATH, encoding="utf-8") as f: config = json.load(f)
    return model, idx_to_class, config

def validate_upload(name, data):
    if not data: return None, "The uploaded file is empty."
    if Path(name).suffix.lower() not in ALLOWED_EXT: return None, "Please upload a JPG, JPEG or PNG image."
    if len(data) > MAX_FILE_MB * 1024 * 1024: return None, f"Image must be smaller than {MAX_FILE_MB} MB."
    try:
        Image.open(io.BytesIO(data)).verify()
        img = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError, SyntaxError):
        return None, "This image cannot be read safely. Try another JPG or PNG."
    if min(img.size) < MIN_SIDE: return None, "Image must be at least 64 pixels wide and high."
    return img, None

def preprocess(img, size):
    return np.asarray(img.resize((size, size), Image.Resampling.BILINEAR), dtype=np.float32)[None, ...]

def predict(img, top_k=3):
    model, idx_to_class, config = load_assets()
    size = int(config.get("image_size", config.get("img_size", 224)))
    probs = model.predict(preprocess(img, size), verbose=0)[0]
    order = np.argsort(probs)[::-1]
    top = [(idx_to_class[int(i)], float(probs[i])) for i in order[:top_k]]
    unc = config.get("uncertainty", {})
    min_conf = float(unc.get("min_confidence", 0.70)); min_margin = float(unc.get("min_margin", 0.15))
    margin = top[0][1] - (top[1][1] if len(top) > 1 else 0.0)
    return {"top": top, "label": top[0][0], "confidence": top[0][1], "margin": margin,
            "uncertain": top[0][1] < min_conf or margin < min_margin,
            "min_confidence": min_conf, "min_margin": min_margin}
