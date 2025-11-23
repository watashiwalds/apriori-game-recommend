import pandas as pd
import numpy as np

def preprocess(input_path:str):
    df = pd.read_csv('steam-200k.csv', header=None, names=['user_id', 'game_title', 'behavior', 'value', 'date'])

    df.dropna(subset=['user_id', 'game_title', 'behavior'], inplace=True)
    df['behavior'] = df['behavior'].str.lower()
    df['game_title'] = df['game_title'].str.strip()

    df_play = df[df['behavior'] == 'play']

    game_playtime = (
        df_play.groupby('game_title')['value']
        .mean()
        .reset_index()
        .rename(columns={'value': 'avg_playtime'})
    )

    df_purchase = df[df['behavior'] == 'purchase']
    all_games = pd.DataFrame(df_purchase['game_title'].unique(),columns=['game_title'])
    full_game_df = all_games.merge(game_playtime, on='game_title', how='left')
    full_game_df['avg_playtime'] = full_game_df['avg_playtime'].fillna(0)

    full_game_df['game_id'] = np.arange(1,len(full_game_df)+1)
    game_df = full_game_df[['game_id', 'game_title', 'avg_playtime']]

    merged = df_purchase.merge(game_df, on='game_title', how='inner')

    library_df = (
        merged.groupby('user_id')['game_id']
        .apply(list)
        .reset_index()
        .rename(columns={'user_id': 'lib_id', 'game_id': 'games'})
    )

    game_path = 'game_table.csv'
    library_path = 'library_table.csv'
    game_df.to_csv(game_path, index=False)
    library_df.to_csv(library_path, index=False)
    return game_path, library_path