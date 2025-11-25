import pandas as pd

Game_table_dir = "game_table.csv"
Library_table_dir = "library_table.csv"

game_table = pd.read_csv(Game_table_dir)
library_table = pd.read_csv(Library_table_dir)
library_table = library_table.drop("lib_id",axis=1)

transactions = library_table["games"].apply(eval).tolist()

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

te = TransactionEncoder()
te_fit = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_fit, columns=te.columns_)
print(df_encoded.head())

frequent_itemsets = apriori(df_encoded, min_support=0.02, use_colnames=True)

# rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

rules = rules.sort_values(['lift', 'confidence'], ascending=False)

print(frequent_itemsets)
print(rules[["antecedents", "consequents", "support", "confidence", "lift"]])

def recommend_game_apriori(owned_game, rules, top_n = 5):
    owned_set = set(owned_game)
    recommendations = []
    for idx, rule in rules.iterrows():
        antecedents = rule['antecedents']
        consequents = rule['consequents']
        match_count = len(antecedents.intersection(owned_set))
        if match_count>0:
            # print(antecedents)
            for game in consequents:
                # print(game)
                if game not in owned_set:
                    # print("own:",game)
                    recommendations.append({
                        'game': game,
                        'match_count':match_count,
                        'based_on': list(antecedents),
                        'confidence': rule['confidence'],
                        'lift': rule['lift'],
                        'support': rule['support']
                    })
    # print(recommendations)
    if not recommendations:
        return pd.DataFrame()

    rec_df = pd.DataFrame(recommendations)
    rec_df = rec_df.sort_values(['match_count','confidence','lift'], ascending=False).drop_duplicates('game')
    return rec_df.head(top_n)

def recommend_game(game, top_n):
    result = recommend_game_apriori(game, rules, top_n)
    print(result)

    if result is None or result.empty:
        return []

    if 'game' not in result.columns:
        return []

    if len(result['game']) == 0:
        return []

    return result['game'].tolist()


def game_filter_time(game_list, time_limit, check):
    if not game_list:
        return []

    playtime_map = dict(zip(game_table["game_id"], game_table["avg_playtime"]))

    game_prioritize = []
    game_remain = []

    for game in game_list:
        p_time = playtime_map.get(game)

        if p_time is not None:
            if check == 0:
                if p_time < time_limit:
                    game_prioritize.append(game)
                else:
                    game_remain.append(game)
            elif check == 1:
                if p_time >= time_limit:
                    game_prioritize.append(game)
                else:
                    game_remain.append(game)
        else:
            game_remain.append(game)

    return game_prioritize + game_remain



