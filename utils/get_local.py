import json


def get_fixture(team_id: int):
    with open("./data/fixtures.json", "r") as file:
        fixture_data = json.load(file)
    
    return fixture_data

