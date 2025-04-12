# Solar Time

A Flask web application that provides accurate solar time information based on real-world solar motion. This app calculates and displays various solar events, time periods, seasonal data, and sun position based on geographical location.

## Features

- Solar events calculation (sunrise, noon, sunset, solar midnight)
- Current day period detection (morning, afternoon, evening, night)
- Period progress tracking
- Seasonal information and progress tracking
- Solar position calculation (altitude and azimuth)

## Requirements

- Python 3.6+
- Flask
- Astral
- pytz

## Installation

Create a virtual environment and install the requirements:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

If you don't have a requirements.txt file yet, create one with the following content:

```
flask
astral
pytz
```

## Usage

Run the application:

```bash
python app.py
```

The application will start a development server at http://127.0.0.1:5000/

## API Endpoints

### Main Page

- **URL**: `/`
- **Method**: `GET`
- **Description**: Serves the main HTML page

### Sun Data

- **URL**: `/sun-data/<latitude>/<longitude>`
- **Method**: `GET`
- **URL Parameters**: 
  - `latitude`: Decimal latitude coordinate
  - `longitude`: Decimal longitude coordinate
- **Response**: JSON containing solar events, current period information, season data, and sun position

Example response:
```json
{
  "events": {
    "sunrise": "2025-04-13T06:15:23+00:00",
    "noon": "2025-04-13T12:30:45+00:00",
    "sunset": "2025-04-13T18:45:12+00:00",
    "midnight": "2025-04-14T00:35:18+00:00"
  },
  "current_period": {
    "period": "afternoon",
    "total_seconds": 22467,
    "elapsed_seconds": 10234,
    "progress": 45.55
  },
  "season": {
    "current_season": "Spring",
    "season_start": "2025-03-20T00:00:00+00:00",
    "days_since_start": 24,
    "total_season_days": 93,
    "season_progress": 25.81
  },
  "sun_position": {
    "altitude": 45.7,
    "azimuth": 220.3,
    "is_daytime": true
  }
}
```
