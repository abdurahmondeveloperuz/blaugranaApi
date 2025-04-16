import json


def get_fixture(team_id: int):
    with open("./data/fixtures.json", "r") as file:
        fixture_data = json.load(file)
    
    return fixture_data

def get_table():
    with open("./data/table.json", "r") as file:
        table_data = json.load(file)
    
    return table_data

