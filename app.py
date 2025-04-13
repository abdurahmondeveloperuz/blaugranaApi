from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from utils.get_local import get_fixture as get_fixture_local
from utils.get_fixture import get_fixture
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

# Background task to update the fixtures.json file
def update_fixtures():
    while True:
        fixture_data = get_fixture(83)
        with open("./data/fixtures.json", "w") as file:
            json.dump(fixture_data, file, indent=4)
        print("[SUCCESS] Data saved to fixtures.json")
        print("[WARNING] Waiting for 24 hours before the next update...")
        sleep(60*60*24)  # Sleep for 24 hours

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=update_fixtures, daemon=True)
    thread.start()

@app.get("/fixtures")
async def get_fixtures(team_id: int = verify_team_id):
    fixture_data = get_fixture_local(team_id)
    if fixture_data:
        return fixture_data
    else:
        raise HTTPException(status_code=404, detail="Fixture not found")

if __name__ == "__main__":
    run(app=app)
