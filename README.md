# Halifax Snowfall Monitor Agent

This Python agent monitors the weather forecast for Halifax, Nova Scotia, using the Open-Meteo API. It alerts the user if heavy snowfall (> 5 cm / 50 mm) is predicted within the next 24 hours.

## Features

- **Automated Monitoring:** Checks the forecast every 4 hours.
- **Desktop Alerts:** Triggers a Windows popup alert if the snowfall threshold is exceeded.
- **Zero API Key:** Uses the free Open-Meteo API (no registration required).
- **Configurable:** Easy to adjust location, threshold, and check interval in the script.

## Files

- `weather_agent.py`: Main application script.
- `requirements.txt`: Python dependencies.
- `test_weather_alert.py`: Test script to simulate a heavy snowfall alert.

## Prerequisites

- Python 3.x
- Windows OS (for the popup alerts)

## Installation

1.  Clone or download this repository.
2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the agent in the background:

```bash
python weather_agent.py
```

The script will run continuously. To stop it, press `Ctrl+C` in the terminal window.

## Configuration

You can curb the behavior by editing `weather_agent.py`:

-   `SNOW_THRESHOLD_CM`: Snowfall amount in cm to trigger an alert (default: 5.0).
-   `CHECK_INTERVAL_SECONDS`: How often to check the forecast (default: 14400 seconds / 4 hours).
-   `LATITUDE` / `LONGITUDE`: Location coordinates (default is Halifax).

## Testing

To verify the alert system works without waiting for snow:

```bash
python test_weather_alert.py
```

This will inject dummy data simulating 6 cm of snow and trigger the popup immediately.

## Data Source

Weather data provided by [Open-Meteo.com](https://open-meteo.com/).
