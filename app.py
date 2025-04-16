from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from utils.get_local import get_fixture as get_fixture_local, get_table as get_table_local
from utils.get_fixture import get_fixture
from utils.get_league_table import get_table
from uvicorn import run
import json
from time import sleep
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verify_team_id = Depends(lambda team_id: team_id)


import os

def update_fixtures():
    while True:
        fixture_data = get_fixture(83)
        os.makedirs("./data", exist_ok=True)
        with open("./data/fixtures.json", "w") as file:
            json.dump(fixture_data, file, indent=4)
        print("[SUCCESS] Data saved to fixtures.json")
        print("[WARNING] Waiting for 24 hours before the next update...")
        sleep(60*60*24)

def update_league_table():
    while True:
        try:
            table_data = get_table()
            
            file_path = os.path.join(os.getcwd(), 'data', 'table.json')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            print("[DEBUG] Saving to file:", file_path)

            with open(file_path, "w") as file:
                json.dump(table_data, file, indent=4)
            
            print("[SUCCESS] Data saved to table.json")
            print("[WARNING] Waiting for 1 hour before the next update...")
            sleep(60 * 60)

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            sleep(60 * 60) 



@app.on_event("startup")
def startup_event():
    thread_1 = threading.Thread(target=update_fixtures, daemon=True)
    thread_2 = threading.Thread(target=update_league_table, daemon=True)
    thread_1.start()
    thread_2.start()

@app.get("/fixtures")
async def get_fixtures(team_id: int = verify_team_id):
    fixture_data = get_fixture_local(team_id)
    if fixture_data:
        return fixture_data
    else:
        raise HTTPException(status_code=404, detail="Fixture not found")

@app.get("/table")
async def get_league_table():
    table = get_table_local()
    if table:
        return table
    else:
        raise HTTPException(status_code=404, detail="Table not found")

if __name__ == "__main__":
    run(app=app)

