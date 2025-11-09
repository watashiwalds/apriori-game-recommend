import pandas as pd
from db_config import get_connection

def insert_steam_games(csv_path: str):
    conn = get_connection()
    if conn is None:
        print("Database connection failed. Check your connection")
        return
    df = pd.read_csv(csv_path, header=None, names=['user_id', 'game_title', 'behavior', 'playtime', 'date'])
    cur = conn.cursor()
    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO SteamVideoGame (user_id, game_title, behavior, playtime, date)
                VALUES (?, ?, ?, ?, ?)
            """
            cur.execute(
                query,
                (
                    int(row["user_id"]),
                    str(row["game_title"]),
                    str(row["behavior"]),
                    float(row["playtime"]) if pd.notna(row["playtime"]) else None,
                    int(row["date"]) if pd.notna(row["date"]) else None
                )
            )
        except Exception as e:
            print(f"Lỗi khi insert user_id={row.get('user_id', 'N/A')}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"Đã insert xong {len(df)} dòng vào SteamVideoGame.")
