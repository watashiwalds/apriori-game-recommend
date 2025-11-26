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

frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.35)

rules = rules.sort_values(['lift', 'confidence'], ascending=False)

print(frequent_itemsets)
print(rules[["antecedents", "consequents", "support", "confidence", "lift"]])


def recommend_game_apriori(owned_game, rules, top_n=5):
    owned_set = set(owned_game)

    rules['match_count'] = rules['antecedents'].apply(lambda x: len(x.intersection(owned_set)))
    valid_rules = rules[rules['match_count'] > 0].copy()
    # input_set = frozenset(owned_game)
    # valid_rules = rules[rules['antecedents'] == input_set].copy()

    if valid_rules.empty:
        return pd.DataFrame()

    recommendations = valid_rules.explode('consequents')
    recommendations = recommendations.rename(columns={'consequents': 'game'})
    recommendations = recommendations[~recommendations['game'].isin(owned_set)]

    if recommendations.empty:
        return pd.DataFrame()

    recommendations['based_on'] = recommendations['antecedents'].apply(list)

    cols = ['game', 'match_count', 'based_on', 'confidence', 'lift', 'support']
    final_df = recommendations[cols]
    final_df = final_df.sort_values(['match_count', 'confidence', 'lift'],ascending=False)
    final_df = final_df.drop_duplicates(subset='game')

    return final_df.head(top_n)

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