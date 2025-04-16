from uvicorn import run
from fastapi import FastAPI, Depends, HTTPException
import requests
from bs4 import BeautifulSoup
from utils.convert_to_iso import convert_to_iso
from pprint import pprint as print
from time import sleep



def get_table():
    url = f"https://sports.uz/oz/tournaments/league?country=32&league=564"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = []
    for i in range(0, 20):
        team = soup.find("tr", attrs={"data-key": f"{i}"})
        position = team.find_all("td", class_="center short")[0].text.strip()
        team_logo = team.find("img")["src"]
        team_name = team.find("a").text.strip()
        played = team.find_all("td", class_="center short")[1].text.strip()
        win = team.find_all("td", class_="center short")[2].text.strip()
        draw = team.find_all("td", class_="center short")[3].text.strip()
        lose = team.find_all("td", class_="center short")[4].text.strip()
        goal_difference = team.find_all("td", class_="center short")[5].text.strip()
        goals_scored = goal_difference.split("-")[0].strip()
        goals_conceded = goal_difference.split("-")[1].strip()
        goal_difference = int(goals_scored) - int(goals_conceded)
        points = team.find_all("td", class_="center short")[7].text.strip()
        table.append(
            {
                "position": position,
                "team": team_name,
                "teamLogo": team_logo,
                "played": played,
                "won": win,
                "drawn": draw,
                "lost": lose,
                "goalsFor": goals_scored,
                "goalsAgainst": goals_conceded,
                "goalDifference": goal_difference,
                "points": points
            }
        )
    return table








    
