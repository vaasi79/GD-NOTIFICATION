import os
import json
import boto3
import requests
from datetime import datetime, timedelta,timezone
#from dotenv import load_dotenv

#load_dotenv()
#load_dotenv() is only needed when reading environment variables from a local .env file.

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")

    quarters = game.get("Quarters",[])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore','N/A')}--{q.get('HomeScore','N/A')}" for q in quarters])

    if status in ['Final','F/OT'] :
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
            f"Quarter Scores: {quarter_scores}\n"
        )
    elif status == "InProgress":
        last_play = game.get('LastPlay','N/A')
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

def lambda_handler(event,context):
    api_key = os.getenv("NBA_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns = boto3.client("sns")

    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)  # Central Time is UTC-6
    today_date = central_time.strftime("%Y-%m-%d")

    print(f"Fetching games for the date: {today_date}")

    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"
    #api_url = "https://api.sportsdata.io/v3/nba/scores/json/GamesByDate"
    #params = {
    #"key": api_key,
    #"date": today_date
    #}
    try:
        response = requests.get(api_url)
        #response = requests.get(api_url,params=params)
        response.raise_for_status()
        data = response.json()
        print(json.dumps(data,indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return {"statusCode":500,"body": "Error fetching data"}
    
    messages = [format_game_data(game) for game in data]
    final_message = "\n-----\n".join(messages) if messages else f"No games available for today : {today_date}"

    try:
        sns.publish(
            TopicArn = sns_topic_arn,
            Message = final_message,
            Subject = "NBA Game Updates"
        )
        print("Message published to SNS successfully")
    except Exception as e:
        print(f"Error while publishing to SNS : {e}")
        return {"statusCode":500,"body":"Error publishing to SNS"}
    
        

    return {"statusCode": 200,"body":"Data processed and sent to SNS, all the work finally done!!"}
