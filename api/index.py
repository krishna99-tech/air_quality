import json
import urllib.request
from datetime import datetime

# YOUR GOOGLE SHEET ID
SHEET_ID = "1hWJVUKR-3PB_b4XwgHwvoGNEg2B51eQTHD6gvuAaRfI"

def main(request):
    try:
        # Parse ESP32 JSON data
        data = request.get_json()
        
        # Format timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        
        # Prepare row for Google Sheets
        row = [
            timestamp,
            float(data.get('temperature', 0)),
            float(data.get('humidity', 0)),
            int(data.get('co2', 0)),
            int(data.get('tvoc', 0)),
            float(data.get('no2', 0)),
            int(data.get('pm1', 0)),
            int(data.get('pm25', 0)),
            int(data.get('pm10', 0))
        ]
        
        # Direct Google Sheets API (NO AUTH needed for public edit)
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Sheet1!A:J:append?valueInputOption=USER_ENTERED&key=AIzaSyDWhZa6K8Mgx7scvK3M6fGSgD3pRSB4F4E'
        
        req = urllib.request.Request(
            url,
            data=json.dumps({"values": [row]}).encode('utf-8'),
            method='POST',
            headers={'Content-Type': 'application/json'}
        )
        
        urllib.request.urlopen(req)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'success',
                'timestamp': timestamp,
                'data': data,
                'rows_added': 1
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
