from uvicorn import run
from fastapi import FastAPI, Depends, HTTPException
import requests
from bs4 import BeautifulSoup
from utils.convert_to_iso import convert_to_iso
from pprint import pprint as print
from time import sleep


def get_fixture(team_id: int):
    url = f"https://sports.uz/oz/teams/fixtures?id={team_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    fixture_data = []
    fixtures = soup.find_all("div", class_="item")
    for fixture in fixtures:
        match_url = "https://sports.uz" + fixture.find("div", class_="game-info").find("a")["href"]
        match_id = match_url.split("/")[-1]
        match_page = requests.get(match_url)
        match_soup = BeautifulSoup(match_page.content, "html.parser")

        match_league = match_soup.find("ul", class_="scoreboard-header").find("li").text.strip()

        homeTeam = match_soup.find("div", id="team-home")
        homeTeamLogo = homeTeam.find("img")["src"]
        homeTeamName = homeTeam.find("h3").text.strip()
        awayTeam = match_soup.find("div", id="team-away")
        awayTeamLogo = awayTeam.find("img")["src"]
        awayTeamName = awayTeam.find("h3").text.strip()

        scoreboard_date = match_soup.find("p", class_="scoreboard-date").text.strip()
        date = convert_to_iso(scoreboard_date)

        scoreboard_footer = match_soup.find("div", class_="scoreboard-footer")
        venue = scoreboard_footer.find("p").text.strip()
        venue = venue.split(":")[-1].strip()

        match_score = match_soup.find("div", class_="game-score")
        goals = match_score.find_all("span", class_="winner")
        homeScore = goals[0]
        awayScore = goals[1]

        game_status = fixture.find("div", class_="game-status").text.strip()
        if game_status == "Tugadi":
            game_status = "finished"
        elif game_status == "Tez orada":
            game_status = "upcoming"
        else:
            game_status = "upcoming"
        fixture_data.append({
            "id": match_id,
            "competition": match_league,
            "homeTeam": homeTeamName,
            "homeTeamLogo": homeTeamLogo,
            "awayTeam": awayTeamName,
            "awayTeamLogo": awayTeamLogo,
            "date": date,
            "venue": venue,
            "homeScore": homeScore.text.strip(),
            "awayScore": awayScore.text.strip(),
            "game_status": game_status,
            
        })
        sleep(0.5)
    return fixture_data
    
