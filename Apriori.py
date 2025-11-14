import numpy as np
import pandas as pd

data_dir = "steam-200k.csv"

df = pd.read_csv(data_dir, header=None, names=["user_id", "game_title", "behavior_name", "value", "unknown"])
# print(df.head())

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Lọc dữ liệu
df = df[(df["behavior_name"] == "purchase") | ((df["behavior_name"] == "play") & (df["value"] > 0))]

# Gom transaction theo user
transactions = df.groupby("user_id")["game_title"].apply(list).tolist()
# print(transactions[1])

# Mã hoá One-hot
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
# print(df_encoded.head())

# Tìm itemsets
frequent_itemsets = apriori(df_encoded, min_support=0.02, use_colnames=True)

# Tạo luật
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(['lift', 'confidence'], ascending=False)

# print("Các tập phổ biến")
# print(frequent_itemsets)

# print("\nLuật kết hợp (Association Rules)")
# print(rules[["antecedents", "consequents", "support", "confidence", "lift"]])


rules_by_antecedent = {}

for idx, row in rules.iterrows():
    for g in row['antecedents']:
        if g not in rules_by_antecedent:
            rules_by_antecedent[g] = []
        rules_by_antecedent[g].append(idx)


def recommend_games_fast(owned_games, rules, rules_by_antecedent, top_n=5):
    owned_set = set(owned_games)
    candidate_rules = set()

    # Tập các rule có liên quan
    for g in owned_set:
        if g in rules_by_antecedent:
            candidate_rules.update(rules_by_antecedent[g])

    recommendations = []

    for idx in candidate_rules:
        rule = rules.loc[idx]
        antecedents = rule['antecedents']
        consequents = rule['consequents']

        if antecedents.issubset(owned_set):
            for game in consequents:
                if game not in owned_set:
                    recommendations.append({
                        'game': game,
                        'based_on': list(antecedents),
                        'confidence': rule['confidence'],
                        'lift': rule['lift'],
                        'support': rule['support']
                    })

    if not recommendations:
        return pd.DataFrame()

    rec_df = pd.DataFrame(recommendations)
    rec_df = rec_df.sort_values('confidence', ascending=False).drop_duplicates('game')
    return rec_df.head(top_n)


def get_recommendations_interactive(owned_games_input):

    if isinstance(owned_games_input, str):
        owned_games = [g.strip() for g in owned_games_input.split(',')]
    else:
        owned_games = owned_games_input

    print(f"🎮 Game bạn đang có: {', '.join(owned_games)}\n")

    recommendations = recommend_games_fast(owned_games, rules, rules_by_antecedent, top_n=10)

    if recommendations.empty:
        print("Không tìm thấy gợi ý phù hợp.")
        return None
    return recommendations



# ========== CHẠY THỬ ==========

# owned_games = ["Counter-Strike Global Offensive", "Dota 2"]
# recommendations = get_recommendations_interactive(owned_games)
#
# recommendations1 = get_recommendations_interactive("Counter-Strike Global Offensive, Dota 2, Team Fortress 2")
#

# ========== TÌM GAME TƯƠNG TỰ ==========

def find_similar_fast(game_name, rules, rules_by_antecedent, top_n=5):
    related = rules_by_antecedent.get(game_name, [])
    results = []

    for idx in related:
        r = rules.loc[idx]
        if game_name in r['antecedents']:
            for g in r['consequents']:
                results.append((g, r['lift'], r['confidence']))
        if game_name in r['consequents']:
            for g in r['antecedents']:
                results.append((g, r['lift'], r['confidence']))

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results, columns=['game', 'lift', 'confidence'])
    return df.sort_values('lift', ascending=False).drop_duplicates('game').head(top_n)


# similar = find_similar_fast("Counter-Strike Global Offensive", rules, rules_by_antecedent)
