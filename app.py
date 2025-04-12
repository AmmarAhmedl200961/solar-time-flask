from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun, azimuth, elevation
import pytz
import math

app = Flask(__name__)

def get_solar_events(lat, lon, date=None):
    if date is None:
        date = datetime.now(pytz.UTC)
    
    location = LocationInfo(
        'Custom',
        'Region',
        'UTC',
        latitude=lat,
        longitude=lon
    )
    
    s = sun(location.observer, date=date)
    
    # Calculate solar midnight (halfway between sunset and next sunrise)
    next_day = date + timedelta(days=1)
    tomorrow_sun = sun(location.observer, date=next_day)
    solar_midnight = s['sunset'] + (tomorrow_sun['sunrise'] - s['sunset']) / 2
    
    return {
        'sunrise': s['sunrise'],
        'noon': s['noon'],
        'sunset': s['sunset'],
        'midnight': solar_midnight
    }

def get_current_period(events, current_time=None):
    if current_time is None:
        current_time = datetime.now(pytz.UTC)
    
    if current_time < events['sunrise']:
        return 'night'
    elif current_time < events['noon']:
        return 'morning'
    elif current_time < events['sunset']:
        return 'afternoon'
    elif current_time < events['midnight']:
        return 'evening'
    else:
        return 'night'

def calculate_period_progress(events, current_time=None):
    if current_time is None:
        current_time = datetime.now(pytz.UTC)
    
    period = get_current_period(events, current_time)
    
    period_starts = {
        'morning': events['sunrise'],
        'afternoon': events['noon'],
        'evening': events['sunset'],
        'night': events['midnight']
    }
    
    period_ends = {
        'morning': events['noon'],
        'afternoon': events['sunset'],
        'evening': events['midnight'],
        'night': events['sunrise'] + timedelta(days=1)
    }
    
    start_time = period_starts[period]
    end_time = period_ends[period]
    
    total_seconds = (end_time - start_time).total_seconds()
    elapsed_seconds = (current_time - start_time).total_seconds()
    
    return {
        'period': period,
        'total_seconds': total_seconds,
        'elapsed_seconds': elapsed_seconds,
        'progress': (elapsed_seconds / total_seconds) * 100
    }

def get_season_info(lat, lon, current_time=None):
    if current_time is None:
        current_time = datetime.now(pytz.UTC)
    
    year = current_time.year
    
    # Approximate equinoxes and solstices
    spring_equinox = datetime(year, 3, 20, tzinfo=pytz.UTC)
    summer_solstice = datetime(year, 6, 21, tzinfo=pytz.UTC)
    autumn_equinox = datetime(year, 9, 22, tzinfo=pytz.UTC)
    winter_solstice = datetime(year, 12, 21, tzinfo=pytz.UTC)
    
    seasons = [
        ('Spring', spring_equinox),
        ('Summer', summer_solstice),
        ('Autumn', autumn_equinox),
        ('Winter', winter_solstice)
    ]
    
    current_season = None
    season_start = None
    next_season = None
    
    for i, (season, date) in enumerate(seasons):
        if current_time >= date:
            if i == len(seasons) - 1:
                current_season = season
                season_start = date
                next_season = seasons[0][1].replace(year=year + 1)
            else:
                current_season = season
                season_start = date
                next_season = seasons[i + 1][1]
    
    days_since_start = (current_time - season_start).days
    total_season_days = (next_season - season_start).days
    
    return {
        'current_season': current_season,
        'season_start': season_start.isoformat(),
        'days_since_start': days_since_start,
        'total_season_days': total_season_days,
        'season_progress': (days_since_start / total_season_days) * 100
    }

def calculate_sun_position(lat, lon, current_time=None):
    if current_time is None:
        current_time = datetime.now(pytz.UTC)
    
    location = LocationInfo('Custom', 'Region', 'UTC', latitude=lat, longitude=lon)
    
    # Calculate sun's position using astral
    az = azimuth(location.observer, current_time)
    alt = elevation(location.observer, current_time)
    
    return {
        'altitude': alt,
        'azimuth': az,
        'is_daytime': alt > 0
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sun-data/<float:lat>/<float:lon>')
def get_sun_data(lat, lon):
    current_time = datetime.now(pytz.UTC)
    events = get_solar_events(lat, lon, current_time)
    period_progress = calculate_period_progress(events, current_time)
    season_info = get_season_info(lat, lon, current_time)
    sun_position = calculate_sun_position(lat, lon, current_time)
    
    return jsonify({
        'events': {
            'sunrise': events['sunrise'].isoformat(),
            'noon': events['noon'].isoformat(),
            'sunset': events['sunset'].isoformat(),
            'midnight': events['midnight'].isoformat()
        },
        'current_period': period_progress,
        'season': season_info,
        'sun_position': sun_position
    })

if __name__ == '__main__':
    app.run(debug=True)
