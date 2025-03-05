import pandas as pd

def transform(df):
    
    # Calculate total goals for each team
    home_teams = df[["Season", "HomeTeam", "FTHG"]].rename(
        columns={"HomeTeam": "Team", "FTHG": "GoalsScored"}
    )
    away_teams = df[["Season", "AwayTeam", "FTAG"]].rename(
        columns={"AwayTeam": "Team", "FTAG": "GoalsScored"}
    )
    all_teams = pd.concat([home_teams, away_teams])
    team_stats = all_teams.groupby(["Season", "Team"]).agg(
        GoalsScored=("GoalsScored", "sum")
    ).reset_index()
    
    # Find best-scoring team by season
    best_scoring_teams = team_stats.loc[team_stats.groupby("Season")["GoalsScored"].idxmax()]
    
    return best_scoring_teams