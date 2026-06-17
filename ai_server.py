from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"

# Tomato Growing Conditions
TOMATO = {
    "temp_min": 21,
    "temp_max": 27,
    "humidity_min": 60,
    "humidity_max": 80,
    "soil_min": 60,
    "soil_max": 80,
    "light_min": 70,
    "light_max": 100,
}


@app.route("/")
def home():
    return "Smart Tomato Greenhouse AI Server Running"


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        temperature = float(data.get("temperature", 0))
        humidity = float(data.get("humidity", 0))
        soil = float(data.get("soil", 0))
        light = float(data.get("light", 0))

        health_score = 100
        issues = []

        # Temperature
        if temperature < TOMATO["temp_min"]:
            health_score -= 15
            issues.append("Temperature is below the ideal range")

        if temperature > TOMATO["temp_max"]:
            health_score -= 15
            issues.append("Temperature is above the ideal range")

        # Humidity
        if humidity < TOMATO["humidity_min"]:
            health_score -= 10
            issues.append("Humidity is below the ideal range")

        if humidity > TOMATO["humidity_max"]:
            health_score -= 10
            issues.append("Humidity is above the ideal range")

        # Soil Moisture
        if soil < TOMATO["soil_min"]:
            health_score -= 25
            issues.append("Soil moisture is too low")

        if soil > TOMATO["soil_max"]:
            health_score -= 15
            issues.append("Soil moisture is too high")

        # Light
        if light < TOMATO["light_min"]:
            health_score -= 20
            issues.append("Light level is too low")

        if light > TOMATO["light_max"]:
            health_score -= 10
            issues.append("Light level is too high")

        health_score = max(0, min(100, health_score))

        if not issues:
            issues.append("No issues detected")

        issues_text = "\n".join(
            [f"- {issue}" for issue in issues]
        )

        prompt = f"""
            You are an AI assistant for a tomato greenhouse.

            Health Score: {health_score}/100

            Detected Issues:
            {issues_text}

            Write exactly:

            Status:
            <one sentence>

            Recommendation:
            <one sentence>

            Maximum 25 words total.

            Do not explain calculations.
            Do not mention percentages.
            Do not invent new measurements.
            Use only the detected issues.
            """

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        ai_response = response.json()["response"].strip()

        return jsonify({
            "success": True,
            "plant": "Tomato",
            "temperature": temperature,
            "humidity": humidity,
            "soil": soil,
            "light": light,
            "health_score": health_score,
            "issues": issues,
            "analysis": ai_response
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    print("=" * 50)
    print("SMART TOMATO GREENHOUSE AI SERVER")
    print("=" * 50)
    print(f"Using Model: {MODEL_NAME}")
    print("Tomato Profile Loaded")
    print("Server Running...")
    print("http://127.0.0.1:5000")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )