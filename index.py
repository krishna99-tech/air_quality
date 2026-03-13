from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float
    co2: int
    tvoc: int
    no2: float
    pm1: int
    pm25: int
    pm10: int

# YOUR SHEET ID - Already filled!
SHEET_ID = "1hWJVUKR-3PB_b4XwgHwvoGNEg2B51eQTHD6gvuAaRfI"

# Simple auth for public sheets (no credentials needed)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
except:
    # Fallback for public sheets
    client = gspread.service_account_if_available()

doc = client.open_by_key(SHEET_ID)
sheet = doc.sheet1

@app.post("/sensor-data")
async def save_sensor_data(data: SensorData, request: Request):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row = [
        timestamp,
        round(data.temperature, 1),
        round(data.humidity, 1),
        data.co2,
        data.tvoc,
        round(data.no2, 2),
        data.pm1,
        data.pm25,
        data.pm10
    ]
    
    sheet.append_row(row)
    return {"status": "success", "message": f"Data saved at {timestamp}"}

@app.get("/")
async def root():
    return {"message": "ESP32 Air Quality API - Ready!", "sheet_id": SHEET_ID}
