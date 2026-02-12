import requests
import json
import time
from datetime import datetime
import ctypes  # For Windows popup

# Configuration
LATITUDE = 44.6488
LONGITUDE = -63.5752
API_URL = "https://api.open-meteo.com/v1/forecast"
SNOW_THRESHOLD_CM = 5.0  # 50 mm = 5 cm
CHECK_INTERVAL_SECONDS = 4 * 3600  # Check every 4 hours

def get_forecast():
    """Fetches the weather forecast from Open-Meteo."""
    try:
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "hourly": "snowfall",
            "timezone": "auto"
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forecast: {e}")
        return None

def check_snowfall(forecast_data):
    """Checks if snowfall exceeds the threshold in the next 24 hours."""
    if not forecast_data or 'hourly' not in forecast_data:
        return;

    hourly = forecast_data['hourly']
    snowfall = hourly.get('snowfall', [])
    times = hourly.get('time', [])

    # Get current time index (approximate)
    # Open-Meteo returns ISO 8601 strings, checking the first 24 slots from now
    # Since the API returns past data for the current day too, we need to be careful.
    # However, 'hourly' usually starts at 00:00 of the requested day (or today).
    # Let's just sum the next 24 entries from the current hour.
    
    current_hour_iso = datetime.now().strftime("%Y-%m-%dT%H:00")
    
    start_index = 0
    try:
        # Find the index of the current hour
        # This is a simple string match, might need robust parsing if format changes, 
        # but Open-Meteo is consistent.
        # If not found (e.g. slight time diff), we'll iterate to find the closest or just take the first 24 if uncertain.
        # Actually, simpler: datetime objects.
        
        # Let's just take the next 24 items provided by the API if we assume the API returns relevant future data.
        # Default API call returns 7 days.
        
        # Better approach: Filter for future times only, up to 24 hours from now.
        now = datetime.now()
        accumulated_snow = 0.0
        
        count = 0
        for t_str, snow_cm in zip(times, snowfall):
            if snow_cm is None: continue
            
            # Open-Meteo time format: "2023-10-27T00:00"
            t = datetime.strptime(t_str, "%Y-%m-%dT%H:%M")
            
            if t >= now:
                accumulated_snow += snow_cm
                count += 1
                if count >= 24: # Check next 24 hours
                    break
        
        print(f"[{datetime.now()}] Forecasted snowfall next 24h: {accumulated_snow:.2f} cm")
        
        if accumulated_snow >= SNOW_THRESHOLD_CM:
            trigger_alert(accumulated_snow)
            
    except ValueError as e:
        print(f"Error parsing time data: {e}")

def trigger_alert(amount_cm):
    """Triggers a Windows alert."""
    message = f"WARNING: Heavy Snowfall Forecast!\nAmount: {amount_cm:.2f} cm ({amount_cm*10:.0f} mm) expected in the next 24 hours."
    title = "Weather Agent Alert"
    print(message)
    # 0x40 is MB_ICONINFORMATION, 0x1000 is MB_SYSTEMMODAL (plays sound, stays on top)
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1000)

def main():
    print("Starting Weather Monitoring Agent...")
    print(f"Monitoring for snowfall > {SNOW_THRESHOLD_CM} cm in Halifax.")
    
    while True:
        data = get_forecast()
        if data:
            check_snowfall(data)
        
        # Wait for next check
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
