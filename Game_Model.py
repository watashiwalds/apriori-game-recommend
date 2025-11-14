import json

from flask import jsonify
from sqlalchemy import create_engine, MetaData, Table, text, select


class SteamGame():
    def __init__(self, engine = None):
        try:
            if engine:
                self.engine = engine
            else:
                server = 'DESKTOP-PIULBJ0\\SQLEXPRESS'
                database = 'SteamGameRec'
                driver = 'ODBC Driver 17 for SQL Server'
                conn_str = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver={driver}'
                self.engine = create_engine(conn_str)

            self.metadata = MetaData()
            self.Game = Table("Game", self.metadata, autoload_with=self.engine)
            self.Library = Table("Library", self.metadata, autoload_with= self.engine)

            print('Connected to database successfully!')
        except Exception as e:
            print(f'Connection failed: {e}')

    def get_Game(self):
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Game.c.game_id,self.Game.c.game_title)
                result = conn.execute(stmt).fetchall()
                if result:
                    games = []
                    for row in result:
                        game_id, game_title = row
                        games.append({
                            "game_id": game_id,
                            "game_title":game_title
                        })
                    return jsonify({"data": games}), 200
                else:
                    return jsonify({"message": "Không tìm thấy sách!"}), 404
        except Exception as e:
            return jsonify({"error": f"Query failed: {e}"}), 500

    def get_Game_Id(self, id):
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Game.c.game_id,self.Game.c.game_title).where(self.Game.c.game_id == id)
                result = conn.execute(stmt).fetchone()
                if result:
                    game_id, game_title = result
                    games = {
                        "game_id": game_id,
                        "game_title": game_title
                    }
                    return jsonify({"data": games}), 200
                else:
                    return jsonify({"message": "Không tìm thấy sách!"}), 404
        except Exception as e:
            return jsonify({"error": f"Query failed: {e}"}), 500

    def get_Games_by_Ids(self, id_list):
        if not id_list:
            return jsonify({"message": "Danh sách ID không được để trống!"}), 400
        try:
            with self.engine.connect() as conn:
                stmt = select(self.Game.c.game_id, self.Game.c.game_title).where(self.Game.c.game_id.in_(id_list))
                result = conn.execute(stmt).fetchall()

                if result:
                    games = []
                    for row in result:
                        game_id, game_title = row
                        games.append({
                            "game_id": game_id,
                            "game_title": game_title
                        })
                    return jsonify({"data": games}), 200
                else:
                    return jsonify({"message": "Không tìm thấy game nào với các ID đã cho!"}), 404
        except Exception as e:
            return jsonify({"error": f"Query failed: {e}"}), 500

    def search_Game_by_Name(self, search_term):

        if not search_term or not search_term.strip():
            return jsonify({"message": "Từ khóa tìm kiếm không được để trống!"}), 400

        try:
            with self.engine.connect() as conn:
                search_pattern = f'%{search_term}%'
                stmt = select(self.Game.c.game_id, self.Game.c.game_title).where(
                    self.Game.c.game_title.like(search_pattern))
                result = conn.execute(stmt).fetchall()

                if result:
                    games = []
                    for row in result:
                        game_id, game_title = row
                        games.append({
                            "game_id": game_id,
                            "game_title": game_title
                        })
                    return jsonify({"data": games}), 200
                else:
                    return jsonify({"message": f"Không tìm thấy game nào phù hợp với từ khóa: '{search_term}'"}), 404
        except Exception as e:
            return jsonify({"error": f"Query failed: {e}"}), 500