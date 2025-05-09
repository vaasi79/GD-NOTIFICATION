import os
import json
import boto3
import requests
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv

load_dotenv()

def fetch_nba_data():
    api_key = os.getenv("NBA_API_KEY")
    
    if not api_key:
        print("Error: NBA_API_KEY is not set.")
        return
    
    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/2025-02-13?key={api_key}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        print("Raw JSON Data:")
        print(json.dumps(data, indent=4)) 
        
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    fetch_nba_data()
