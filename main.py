from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt

API_KEY = "12345"

app = FastAPI()

# Allow all origins for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate_forecast(Authorization: str = Header(None)):
    if Authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ───────────────────────────────
    # SIMPLE FAKE PREDICTION EXAMPLE
    # Replace with your real ML model if you want
    # ───────────────────────────────
    dates = pd.date_range(start="2025-01-01", periods=30)
    predictions = np.random.randint(100, 500, size=30).tolist()

    # Generate plot
    plt.figure(figsize=(10, 4))
    plt.plot(dates, predictions)
    plt.title("Future Sales Forecast")
    plt.xlabel("Date")
    plt.ylabel("Sales")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode()

    return {
        "dates": dates.strftime("%Y-%m-%d").tolist(),
        "predictions": predictions,
        "plot_base64": plot_base64
    }
