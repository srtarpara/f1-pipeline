from fastapi import FastAPI
from database import create_connection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "F1 Data Pipeline API"}

@app.get("/drivers")
def get_drivers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drivers")
    rows = cursor.fetchall()
    conn.close()

    drivers = []
    for row in rows:
        drivers.append({
            "driver_number": row[0],
            "full_name": row[1],
            "team_name": row[2],
            "country_code": row[3],
            "headshot_url": row[4]
        })
    return {"drivers": drivers}

@app.get("/sessions")
def get_sessions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for row in rows:
        sessions.append({
            "session_key": row[0],
            "session_name": row[1],
            "session_type": row[2],
            "date_start": row[3],
            "location": row[4],
            "country_name": row[5],
            "year": row[6]
        })
    return {"sessions": sessions}

@app.get("/sessions/{location}")
def get_session_by_location(location: str):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE location LIKE ?", (f"%{location}%",))
    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for row in rows:
        sessions.append({
            "session_key": row[0],
            "session_name": row[1],
            "session_type": row[2],
            "date_start": row[3],
            "location": row[4],
            "country_name": row[5],
            "year": row[6]
        })
    return {"sessions": sessions}