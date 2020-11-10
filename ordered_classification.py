import pandas as pd


nutri_scores = {0: "upper", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}
weights1 = {"energy": 1, "sugar": 1, "satu. fat.": 1, "salt": 1, "protein": 2, "fiber": 2}

table1 = [[100, 0, 0, 0, 100, 100],
          [1550, 11, 0.8, 0.3, 10, 11],
          [1650, 14, 1, 0.4, 7, 8],
          [1750, 17, 1.7, 0.5, 4, 5],
          [1850, 20, 4, 0.6, 3, 2.5],
          [10000, 100, 100, 100, 0, 0]]

tresholds = [0.5, 0.6, 0.7]


def pessimisticMajoritySorting(inputFile, outputFile, weights, table, treshold):
    total_voters = 0
    for value in weights1.values():
        total_voters += value
    foods_df = pd.read_excel(inputFile)
    foods_df = foods_df.rename(columns={"energy100g": "energy", "sugars100g": "sugar",
                                            "saturatedfat100g": "satu. fat.", "sodium100g": "salt",
                                            "proteins100g": "protein", "fiber100g": "fiber"})
    foods_df = foods_df[["energy", "sugar", "satu. fat.", "salt", "protein", "fiber", "nutriscoregrade"]]
    columns = foods_df.columns
    true_score = foods_df["nutriscoregrade"].values.tolist()
    predicted_score = []

    for prod in range(len(foods_df)):
        for row in range(len(table)):
            p, r = 0, 0
            for i in range(len(table[0])):
                if i < 4:
                    if foods_df.loc[prod][i] <= table[row][i]:
                        p += 1 * weights.get(columns[i])
                    else:
                        r += 1 * weights.get(columns[i])
                else:
                    if foods_df.loc[prod][i] >= table[row][i]:
                        p += 1 * weights.get(columns[i])
                    else:
                        r += 1 * weights.get(columns[i])
            if p >= total_voters*treshold:
                predicted_score.append(nutri_scores.get(row))
                break

    foods_df["predicted nutri score"] = predicted_score
    foods_df.to_excel(outputFile)

    pairs = []
    for i in range(len(true_score)):
        pair = (true_score[i], predicted_score[i])
        pairs.append(pair)
    return pairs


def optimisticMajoritySorting(inputFile, outputFile, weights, table, treshold):
    total_voters = 0
    for value in weights1.values():
        total_voters += value
    foods_df = pd.read_excel(inputFile)
    foods_df = foods_df.rename(columns={"energy100g": "energy", "sugars100g": "sugar",
                                            "saturatedfat100g": "satu. fat.", "sodium100g": "salt",
                                            "proteins100g": "protein", "fiber100g": "fiber"})
    foods_df = foods_df[["energy", "sugar", "satu. fat.", "salt", "protein", "fiber", "nutriscoregrade"]]
    columns = foods_df.columns
    true_score = foods_df["nutriscoregrade"].values.tolist()
    predicted_score = []

    for prod in range(len(foods_df)):
        # print("\n")
        for row in range(len(table)-1, -1, -1):
            p, r = 0, 0
            for i in range(len(table[0])):
                if i < 4:
                    if foods_df.loc[prod][i] <= table[row][i]:
                        p += 1 * weights.get(columns[i])
                    else:
                        r += 1 * weights.get(columns[i])
                else:
                    if foods_df.loc[prod][i] >= table[row][i]:
                        p += 1 * weights.get(columns[i])
                    else:
                        r += 1 * weights.get(columns[i])
            # print(r, p, "***", row)
            if r >= total_voters*treshold > p:
                predicted_score.append(nutri_scores.get(row+1))
                break

    foods_df["predicted nutri score"] = predicted_score
    foods_df.to_excel(outputFile)

    pairs = []
    for i in range(len(true_score)):
        pair = (true_score[i], predicted_score[i])
        pairs.append(pair)
    return pairs


def calculateConfusionMatrix(pairs, size):
    indexes = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
    matrix = [[0]*size for i in range(size)]

    for pair in pairs:
        matrix[indexes.get(pair[0])][indexes.get(pair[1])] += 1

    for row in matrix:
        print(row)


# for th in tresholds:
#     pairs1 = pessimisticMajoritySorting("OpenFood_Petales.xlsx", "pessimistic_OpenFood_Petales.xlsx", weights1, table1, th)
#     print("\nFor treshold", th, "the confusion matrix is:")
#     calculateConfusionMatrix(pairs1, 5)

for th in tresholds:
    pairs2 = optimisticMajoritySorting("OpenFood_Petales.xlsx", "optimistic_OpenFood_Petales.xlsx", weights1, table1, th)
    print("\nFor treshold", th, "the confusion matrix is:")
    calculateConfusionMatrix(pairs2, 5)
