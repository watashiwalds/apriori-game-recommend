import ast
import pandas as pd
from psycopg2 import sql, extras
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
            if table_name == "game":
                cur.execute(
                    """
                    INSERT INTO game (game_id, game_title, avg_playtime)
                    VALUES (%s, %s, %s) ON CONFLICT (game_id) DO NOTHING
                    """,
                    (int(row["game_id"]), row["game_title"], float(row["avg_playtime"]))
                )
            elif table_name == "library":
                games_list = ast.literal_eval(row["games"])
                cur.execute(
                    """
                    INSERT INTO library (lib_id, games)
                    VALUES (%s, %s::bigint[]) ON CONFLICT (lib_id) DO NOTHING
                    """,
                    (int(row["lib_id"]), games_list)
                )

        except Exception as e:
            print(f"⚠️ Lỗi khi insert lib_id={row.get('lib_id', 'N/A')}: {e}")
            conn.rollback()
        else:
            conn.commit()
    cur.close()
    conn.close()