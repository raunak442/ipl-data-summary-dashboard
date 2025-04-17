# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import json
import pandas as pd

FOLDER = r"C:\Users\Raunak\ipl_json"

all_deliveries = []
match_summaries = []

for filename in os.listdir(FOLDER):
    if filename.endswith(".json"):
        filepath = os.path.join(FOLDER, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        info = data.get('info',{})
        match_id = filename.replace(".json", " ")
        
        match_summary = {
            "match_id": match_id,
            "date": info.get("dates",[None])[0],
            "venue": info.get("venue", ""),
            "team1": info["teams"][0],
            "team2": info["teams"][1],
            "winner": info.get("outcome",{}).get("winner", "No Result"),
            "player_of_match": info.get("player_of_match", [None])[0],
            "toss_winner": info["toss"]["winner"],
            "toss_decision": info["toss"]["decision"],
            "season": info.get("season", "")
            }
            
        match_summaries.append(match_summary)
        
        for inning in data.get("innings", []):
            team = inning['team']
            for over in inning['overs']:
                for delivery in over['deliveries']:
                    delivery_data = {
                        "match_id": match_id,
                        "team": team,
                        "over": over['over'],
                        "batter": delivery.get('batter'),
                        "bowler": delivery.get('bowler'),
                        "non_striker": delivery.get('non_striker'),
                        "runs_batter": delivery.get('runs', {}).get('batter', 0),
                        "runs_extras": delivery.get('runs', {}).get('extras', 0),
                        "runs_total": delivery.get('runs', {}).get('total', 0),

                        "wicket_kind": delivery.get("wickets", [{}])[0].get("kind") if "wickets" in delivery else None,
                        "wicket_player_out": delivery.get("wickets", [{}])[0].get("player_out") if "wickets" in delivery else None,
                        }
                    all_deliveries.append(delivery_data)
                    
                    
df_matches = pd.DataFrame(match_summaries)
df_deliveries = pd.DataFrame(all_deliveries)

df_matches.to_csv("ipl_matches_summary.csv", index = False)
df_deliveries.to_csv("ipl_deliveries.csv", index = False)

print("✅ Matches loaded:", len(df_matches))
print("✅ Deliveries loaded:", len(df_deliveries))
print("\nSample Matches:")
print(df_matches.head())
print("\nSample Deliveries:")
print(df_deliveries.head())
                        
