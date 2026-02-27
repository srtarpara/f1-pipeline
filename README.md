# F1 Data Pipeline

A data engineering project that pulls live Formula 1 data from the [OpenF1 API](https://openf1.org/), stores it in a structured database, and serves it through a custom REST API.

## What It Does

- Fetches real-time F1 data including drivers, sessions, and lap times
- Stores data in a structured SQLite database with relational tables
- Exposes data through a FastAPI REST API with multiple query endpoints
- Supports querying fastest laps per driver for any race session

## Tech Stack

- **Python** — data fetching, processing, and API logic
- **SQLite** — structured local database storage
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **OpenF1 API** — free, real-time F1 data source

## Project Structure

```
f1-data-pipeline/
├── database.py       # Database connection and table creation
├── insert_data.py    # Fetches data from OpenF1 API and stores it
├── api.py            # FastAPI endpoints
└── requirements.txt  # Project dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/drivers` | All current F1 drivers |
| GET | `/sessions` | All 2024 race sessions |
| GET | `/sessions/{location}` | Sessions filtered by location |
| GET | `/laps/{session_key}` | All lap times for a session |
| GET | `/laps/{session_key}/fastest` | Fastest lap per driver for a session |

## Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/YOURUSERNAME/f1-data-pipeline.git
cd f1-data-pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Populate the database**
```bash
python insert_data.py
```

**4. Start the API**
```bash
uvicorn api:app --reload
```

**5. Query the API**
```
http://127.0.0.1:8000/drivers
http://127.0.0.1:8000/sessions/Bahrain
http://127.0.0.1:8000/laps/9472/fastest
```

## Example Response

`GET /laps/9472/fastest` — Fastest lap per driver, 2024 Bahrain Grand Prix:

```json
{
  "fastest_laps": [
    { "driver_number": 1, "fastest_lap": 92.608 },
    { "driver_number": 16, "fastest_lap": 94.09 },
    { "driver_number": 14, "fastest_lap": 94.199 }
  ]
}
```

## Data Model

```
drivers         sessions          lap_times
-----------     -----------       -----------
driver_number   session_key       id
full_name       session_name      session_key (FK)
team_name       session_type      driver_number (FK)
country_code    date_start        lap_number
headshot_url    location          lap_duration
                country_name
                year
```