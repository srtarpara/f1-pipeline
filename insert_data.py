import requests
import sqlite3
from database import create_connection

def fetch_and_store_drivers():
    url = "https://api.openf1.org/v1/drivers?session_key=latest"
    response = requests.get(url)
    drivers = response.json()

    conn = create_connection()
    cursor = conn.cursor()

    for driver in drivers:
        cursor.execute("""
            INSERT OR REPLACE INTO drivers
            (driver_number, full_name, team_name, country_code, headshot_url)
            VALUES(?, ?, ?, ?, ?)
        """, (
            driver.get('driver_number'),
            driver.get('full_name'),
            driver.get('team_name'),
            driver.get('country_code'),
            driver.get('headshot_url')
        ))

    conn.commit()
    conn.close()

    print(f"Inserted {len(drivers)} drivers successfully")


def fetch_and_store_sessions():
    url = "https://api.openf1.org/v1/sessions?year=2024"
    response = requests.get(url)
    sessions = response.json()

    conn = create_connection()
    cursor = conn.cursor()

    for session in sessions:
        cursor.execute("""
            INSERT OR REPLACE INTO sessions
            (session_key, session_name, session_type, date_start, location, country_name, year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session.get('session_key'),
            session.get('session_name'),
            session.get('session_type'),
            session.get('date_start'),
            session.get('location'),
            session.get('country_name'),
            session.get('year')
        ))

    conn.commit()
    conn.close()
    print(f"Inserted {len(sessions)} sessions successfully")

def fetch_and_store_lap_times(session_key):
    url = f"https://api.openf1.org/v1/laps?session_key={session_key}"
    response = requests.get(url)
    laps = response.json()

    if not laps:
        print(f"No lap data for session {session_key}")
        return
    
    conn = create_connection()
    cursor = conn.cursor()

    for lap in laps:
        cursor.execute("""
            INSERT OR REPLACE INTO lap_times
            (session_key, driver_number, lap_number, lap_duration)
            VALUES (?, ?, ?, ?)
        """, (
            lap.get('session_key'),
            lap.get('driver_number'),
            lap.get('lap_number'),
            lap.get('lap_duration')
        ))

    conn.commit()
    conn.close()

    print(f"Inserted {len(laps)} laps for session {session_key}")

if __name__ == "__main__":
    fetch_and_store_drivers()
    fetch_and_store_sessions()
    fetch_and_store_lap_times(9472)