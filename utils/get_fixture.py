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

        # Safely extract match league
        match_league = match_soup.find("ul", class_="scoreboard-header").find("li")
        match_league = match_league.text.strip() if match_league else ""

        # Safely extract home team details
        homeTeam = match_soup.find("div", id="team-home")
        homeTeamLogo = homeTeam.find("img")["src"] if homeTeam and homeTeam.find("img") else ""
        homeTeamName = homeTeam.find("h3").text.strip() if homeTeam and homeTeam.find("h3") else ""

        # Safely extract away team details
        awayTeam = match_soup.find("div", id="team-away")
        awayTeamLogo = awayTeam.find("img")["src"] if awayTeam and awayTeam.find("img") else ""
        awayTeamName = awayTeam.find("h3").text.strip() if awayTeam and awayTeam.find("h3") else ""

        # Safely extract date
        scoreboard_date = match_soup.find("p", class_="scoreboard-date")
        scoreboard_date = scoreboard_date.text.strip() if scoreboard_date else ""
        date = convert_to_iso(scoreboard_date) if scoreboard_date else ""

        # Safely extract venue
        scoreboard_footer = match_soup.find("div", class_="scoreboard-footer")
        venue = scoreboard_footer.find("p").text.strip() if scoreboard_footer and scoreboard_footer.find("p") else ""
        venue = venue.split(":")[-1].strip() if venue else ""

        # Safely extract scores
        match_score = match_soup.find("div", class_="game-score")
        goals = match_score.find_all("span", class_="winner") if match_score else []
        homeScore = goals[0].text.strip() if goals else "0"
        awayScore = goals[1].text.strip() if len(goals) > 1 else "0"

        # Safely extract game status
        game_status = fixture.find("div", class_="game-status")
        if game_status:
            game_status = game_status.text.strip()
            if game_status == "Tugadi":
                game_status = "finished"
            elif game_status == "Tez orada":
                game_status = "upcoming"
            else:
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
            "homeScore": homeScore,
            "awayScore": awayScore,
            "game_status": game_status,
        })

        sleep(0.5)
    return fixture_data
