import ast
import pandas as pd
import json
from db_config import get_connection

def insert_data(csv_path: str, table_name:str):
    conn = get_connection()
    if conn is None:
        print('connection failed')
        return
    df = pd.read_csv(csv_path)
    cur = conn.cursor()

    for _, row in df.iterrows():
        try:
            if table_name == "Game":
                query = """
                    INSERT INTO Game (game_id, game_title, avg_playtime)
                    VALUES(?, ?, ?)
                    """
                cur.execute (
                    query,
                    (int(row["game_id"]),row["game_title"],float(row["avg_playtime"]))
                )
            elif table_name == "Library":
                game_list = ast.literal_eval(row["games"])
                game_json = json.dumps(game_list)
                query = """
                    INSERT INTO Library (lib_id, games)
                    VALUES(?, ?)
                """
                cur.execute (
                    query,
                    (int(row["lib_id"]),game_json)
                )

        except Exception as e:
            print(f"Lỗi khi insert lib_id={row.get('lib_id', 'N/A')}: {e}")

    conn.commit()
    cur.close()
    conn.close()