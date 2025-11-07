from insert_data import *
from Preprocess import preprocess

if __name__ == '__main__':
    input_path = 'steam-200k.csv'
    game_csv, library_csv = preprocess(input_path)
    insert_data(game_csv, 'game')
    insert_data(library_csv, 'library')