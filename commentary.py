import os
import google.generativeai as genai
from database import create_connection

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")

def get_race_data(session_key: int):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions WHERE session_key = ?", (session_key,))
    session = cursor.fetchone()

    if not session:
        conn.close()
        return None, None
    
    session_info = {
        "session_name": session[1],
        "session_type": session[2],
        "location": session[4],
        "country_name": session[5],
        "year": session[6]
    }

    cursor.execute("""
                   SELECT d.full_name, d.team_name, MIN(l.lap_duration) as fastest_lap
                   FROM lap_times l
                   JOIN drivers d ON l.driver_number = d.driver_number
                   WHERE l.session_key = ? AND l.lap_duration IS NOT NULL
                   GROUP BY l.driver_number
                   ORDER BY fastest_lap ASC
                   """, (session_key,))
    
    rows = cursor.fetchall()
    conn.close()

    fastest_laps = [
        {
            "driver": row[0],
            "team": row[1],
            "fastest_lap_seconds": round(row[2], 3)
        }
        for row in rows
    ]

    return session_info, fastest_laps

def format_lap_seconds(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining = seconds % 60
    return f"{minutes}:{remaining:06.3f}"

def generate_commentary(session_key: int) -> dict:
    session_info, fastest_laps = get_race_data(session_key)

    if not session_info or not fastest_laps:
        return {"error": f"No data found for session {session_key}"}
    
    lap_summary_lines = []

    for i, entry in enumerate(fastest_laps):
        formatted_time = format_lap_seconds(entry["fastest_lap_seconds"])
        lap_summary_lines.append(f"{i+1}. {entry['driver']} ({entry['team']}) - {formatted_time}")

    lap_summary = "\n".join(lap_summary_lines)

    winner = fastest_laps[0]["driver"]
    winner_team = fastest_laps[0]["team"]
    winner_time = format_lap_seconds(fastest_laps[0]["fastest_lap_seconds"])

    prompt = f"""You are an expert Formula 1 race commentator in the style of an official F1 broadcast.

    Here is the data from the {session_info['year']} {session_info['location']} Grand Prix ({session_info['country_name']}):

    Fastest Laps Ranking:
    {lap_summary}

    Using this data, write a vivid, engaging race commentary summary. Include:
    1. An exciting opening line about the race and location
    2. A highlight of the race winner and their dominant performance
    3. Commentary on 2-3 notable battles or performances further down the order
    4. A closing line about what this result means for the championship

    Keep it under 200 words. Make it sound like a real broadcaster — energetic, knowledgeable, and dramatic."""

    response = model.generate_content(prompt)
    commentary_text = response.text.strip()

    return{
        "session": f"{session_info['year']} {session_info['location']} Grand Prix",
        "session_type": session_info["session_type"],
        "winner": winner,
        "winner_team": winner_team,
        "winner_fastest_lap": winner_time,
        "total_drivers": len(fastest_laps),
        "fastest_laps_ranking": fastest_laps,
        "ai_commentary": commentary_text
    }
