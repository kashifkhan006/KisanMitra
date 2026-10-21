
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from inference import model_files_exist, predict, validate_upload
from disease_info import get_disease_info, is_healthy, split_class_name

app = Flask(
    __name__,
    static_folder=str(ROOT / "public"),
    static_url_path=""
)

app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024


@app.get("/")
def home():
    return send_from_directory(ROOT / "public", "index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "model_files_present": model_files_exist()
    })


@app.route("/api/predict", methods=["GET", "POST"])
def prediction():

    if request.method == "GET":
        return jsonify({
            "ok": True,
            "message": "Prediction endpoint exists. Upload an image using POST."
        })

    if not model_files_exist():
        return jsonify({
            "error": "Model files are missing. Check the models folder."
        }), 503

    file = request.files.get("image")

    if not file:
        return jsonify({
            "error": "Choose a leaf image first."
        }), 400

    img, error = validate_upload(
        file.filename or "",
        file.read()
    )

    if error:
        return jsonify({"error": error}), 400

    try:
        result = predict(img)

        crop, disease = split_class_name(result["label"])

        result["crop"] = crop
        result["disease"] = disease
        result["healthy"] = is_healthy(disease)
        result["info"] = get_disease_info(disease)

        result["top"] = [
            {
                "label": label,
                "confidence": confidence
            }
            for label, confidence in result["top"]
        ]

        return jsonify(result)

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Prediction failed. Check the Render logs."
        }), 500


@app.errorhandler(413)
def too_large(error):
    return jsonify({
        "error": "Image is too large. Please use an image under 4 MB."
    }), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```
