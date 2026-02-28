from fastapi import FastAPI, HTTPException
from database import create_connection
from commentary import generate_commentary

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

@app.get("/laps/{session_key}")
def get_laps(session_key: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lap_times WHERE session_key = ?", (session_key,))
    rows = cursor.fetchall()
    conn.close()

    laps = []
    for row in rows:
        laps.append({
            "id": row[0],
            "session_key": row[1],
            "driver_number": row[2],
            "lap_number": row[3],
            "lap_duration": row[4]
        })
    
    return {"total_laps": len(laps), "laps" : laps}

@app.get("/laps/{session_key}/fastest")
def get_fastest_laps(session_key: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT driver_number, MIN(lap_duration) as fastest_lap
        FROM lap_times
        WHERE session_key = ? AND lap_duration IS NOT NULL
        GROUP BY driver_number
        ORDER BY fastest_lap ASC
    """, (session_key,))

    rows = cursor.fetchall()
    conn.close()

    return{"fastest_laps": [{"driver_number": row[0], "fastest_lap": row[1]} for row in rows]}

@app.get("/commentary/{session_key}")
def get_race_commentary(session_key: int):
    result = generate_commentary(session_key)

    if "error" in result:
        raise HTTPException(status_code = 404, detail = result["error"])
    
    return result