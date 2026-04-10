import json
import cv2
import numpy as np
import os
import sys

# -------------------------------
# 🔹 Core Logic: Reflectivity Estimation
# -------------------------------
def predict_reflectivity(image_path):
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "message": f"Image not found: {image_path}"
            }

        # Read image
        image = cv2.imread(image_path)

        if image is None:
            return {
                "status": "error",
                "message": "Invalid image format"
            }

        # Convert to grayscale (simulate reflectivity measurement)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate brightness (proxy for reflectivity)
        reflectivity_score = float(np.mean(gray)) / 255.0

        # Classify condition
        if reflectivity_score > 0.7:
            condition = "Good"
        elif reflectivity_score > 0.4:
            condition = "Moderate"
        else:
            condition = "Poor"

        return {
            "status": "success",
            "reflectivity_score": round(reflectivity_score, 3),
            "condition": condition
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# -------------------------------
# 🔹 Main Entry Point
# -------------------------------
if __name__ == "__main__":
    try:
        # Hackathon input format (can be modified based on requirement)
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
        else:
            # Default test image
            image_path = "test.jpg"

        result = predict_reflectivity(image_path)

        # Print output as JSON (VERY IMPORTANT)
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }))
