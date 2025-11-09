from insert_data import *
from Preprocess import preprocess
from insert_steam_video_games import *

if __name__ == '__main__':
    input_path = 'steam-200k.csv'
    # game_csv, library_csv = preprocess(input_path)
    #     # insert_data(game_csv, 'Game')
    #     # insert_data(library_csv, 'Library')
    insert_steam_games(input_path)
    print('DONE')
