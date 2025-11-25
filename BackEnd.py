from flask import Flask, request, jsonify
from Apriori_new import recommend_game, game_filter_time
from Game_Model import SteamGame
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:3636"])

steam_Game = SteamGame()

@app.route('/get_game', methods=['GET'])
def get_game():
    return steam_Game.get_Game()

@app.route('/get_game_id/<int:id>', methods=['GET'])
def get_game_id(id):
    return steam_Game.get_Game_Id(id)

@app.route('/recomment', methods=['POST'])
def recomment():
    data = request.json
    raw_id = data.get('id_game')
    if isinstance(raw_id, list):
        game_id_list = raw_id
    else:
        game_id_list = [raw_id]

    playtime_wanted = float(data.get('time', 0))
    checkbox = int(data.get('check', 1))
    game_recommend = recommend_game(game_id_list, 20)
    final_list = game_filter_time(game_recommend, playtime_wanted, checkbox)
    return jsonify(final_list)


@app.route('/get_games_by_ids', methods=['POST'])
def get_games_by_ids():
    data = request.get_json()
    if not data or 'ids' not in data:
        return jsonify({"message": "Dữ liệu không hợp lệ. Cần cung cấp một JSON object với key là 'ids'."}), 400
    id_list = data['ids']
    if not isinstance(id_list, list):
        return jsonify({"message": "'ids' phải là một danh sách (array)."}), 400
    return steam_Game.get_Games_by_Ids(id_list)

@app.route('/search_game', methods=['GET'])
def search_game_by_name():
    search_term = request.args.get('name')
    return steam_Game.search_Game_by_Name(search_term)

if __name__ == '__main__':
    app.run(debug=True)



