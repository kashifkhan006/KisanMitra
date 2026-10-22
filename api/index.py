        return jsonify({
            "error": "Choose a leaf image first."
        }), 400

    img, error = validate_upload(file.filename or "", file.read())

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
            {"label": label, "confidence": confidence}
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
