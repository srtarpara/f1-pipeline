from apscheduler.schedulers.blocking import BlockingScheduler
from insert_data import fetch_and_store_drivers, fetch_and_store_sessions, fetch_and_store_lap_times
from database import create_connection

def get_latest_session_key():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_key FROM sessions 
        WHERE session_type = 'Race'
        ORDER BY date_start DESC 
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def run_pipeline():
    print("Running pipeline...")
    fetch_and_store_drivers()
    fetch_and_store_sessions()
    session_key = get_latest_session_key()
    if session_key:
        fetch_and_store_lap_times(session_key)
    print("Pipeline complete.")

scheduler = BlockingScheduler()

scheduler.add_job(run_pipeline, 'interval', hours=24)

print("Scheduler started — pipeline will run every 24 hours")
print("Running pipeline now for first time...")
run_pipeline()

scheduler.start()
