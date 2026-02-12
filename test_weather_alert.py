import weather_agent
from datetime import datetime, timedelta

def test_heavy_snow():
    print("Testing heavy snowfall alert...")
    
    # Create dummy data for next 24 hours
    now = datetime.now()
    hourly_times = []
    hourly_snow = []
    
    for i in range(48): # 48 hours of data
        t = now + timedelta(hours=i)
        hourly_times.append(t.strftime("%Y-%m-%dT%H:00"))
        # Simulating heavy snow: 0.5 cm per hour for 12 hours = 6cm
        if i < 12:
            hourly_snow.append(0.5)
        else:
            hourly_snow.append(0.0)
            
    dummy_data = {
        "hourly": {
            "time": hourly_times,
            "snowfall": hourly_snow
        }
    }
    
    print("Injecting dummy data with 6.0 cm accumulated snow.")
    weather_agent.check_snowfall(dummy_data)

if __name__ == "__main__":
    test_heavy_snow()
