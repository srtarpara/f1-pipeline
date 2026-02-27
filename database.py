import sqlite3

def create_connection():
    conn = sqlite3.connect("f1_data.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers(
            driver_number INTEGER PRIMARY KEY,
            full_name TEXT,
            team_name TEXT,
            country_code TEXT,
            headshot_url TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            session_key INTEGER PRIMARY KEY,
            session_name TEXT,
            session_type TEXT,
            date_start TEXT,
            location TEXT,
            country_name TEXT,
            year INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lap_times(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_key INTEGER,
            driver_number INTEGER,
            lap_number INTEGER,
            lap_duration REAL,
            FOREIGN KEY (session_key) REFERENCES sessions(session_key),
            FOREIGN KEY (driver_number) REFERENCES drivers(driver_number)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()