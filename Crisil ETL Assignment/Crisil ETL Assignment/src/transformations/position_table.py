import pandas as pd

def calculate_points(row, team_type):
    # Points calculation
    if team_type == "home":
        if row["FTR"] == "H":
            return 3  
        elif row["FTR"] == "A":
            return 0  
        else:
            return 1  
    elif team_type == "away":
        if row["FTR"] == "A":
            return 3  
        elif row["FTR"] == "H":
            return 0  
        else:
            return 1  

def transform(df):
    #print(df)
    
    home_teams = df[["Season", "HomeTeam", "FTHG", "FTAG", "FTR"]].copy()
    home_teams["Points"] = home_teams.apply(lambda row: calculate_points(row, "home"), axis=1)
    home_teams.rename(
        columns={"HomeTeam": "Team", "FTHG": "GoalsScored", "FTAG": "GoalsConceded"},
        inplace=True
    )
    
    #print(home_teams)
    
    away_teams = df[["Season", "AwayTeam", "FTHG", "FTAG", "FTR"]].copy()
    away_teams["Points"] = away_teams.apply(lambda row: calculate_points(row, "away"), axis=1)
    away_teams.rename(
        columns={"AwayTeam": "Team", "FTAG": "GoalsScored", "FTHG": "GoalsConceded"},
        inplace=True
    )
    
    #print(away_teams)
    
    # Combine home and away data
    all_teams = pd.concat([home_teams, away_teams])
    
    # Aggregate team statistics
    team_stats = all_teams.groupby(["Season", "Team"]).agg(
        Points=("Points", "sum"),
        GoalsScored=("GoalsScored", "sum"),
        GoalsConceded=("GoalsConceded", "sum")
    ).reset_index()
    
    # Calculate Goal Difference
    team_stats["GoalDifference"] = team_stats["GoalsScored"] - team_stats["GoalsConceded"]
    
    # Sort by Points
    team_stats = team_stats.sort_values(
        by=["Season", "Points", "GoalDifference", "GoalsScored"],
        ascending=[True, False, False, False]
    )
    
    # Assign positions within each season
    team_stats["Position"] = team_stats.groupby("Season").cumcount() + 1
    
    # Final sorting for output
    team_stats = team_stats.sort_values(by=["Season", "Position"])
    
    return team_stats