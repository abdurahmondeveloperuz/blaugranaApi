from utils.get_fixture import get_fixture
from utils.convert_to_iso import convert_to_iso
from pprint import pprint as print
import json
from time import sleep

print("[WARNING] Fixtures.json is being updated for the first time...")

while True:
    fixture_data = get_fixture(83)

    with open("./data/fixtures.json", "w") as file:
        json.dump(fixture_data, file, indent=4)

    print("[SUCCESS] Data saved to fixtures.json")
    print("[WARNING] Waiting for 1 hour before the next update...")
    sleep(60*60*24)  # Sleep for 24 hours (60 seconds * 60 minutes * 24 hours)
    print("[WARNING] Updating fixtures.json...")

