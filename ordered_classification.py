import copy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

nutri_scores = {0: "upper", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e"}

weights1 = {"energy": 1, "sugar": 1, "satu. fat.": 1, "salt": 1, "protein": 2, "fiber": 2}

w0 = {"energy": 1, "sugar": 1, "satu. fat.": 1, "salt": 1, "protein": 2, "fiber": 2}
w1 = {"energy": 1, "sugar": 1, "satu. fat.": 1, "salt": 2, "protein": 1, "fiber": 2}
w2 = {"energy": 1, "sugar": 1, "satu. fat.": 2, "salt": 1, "protein": 1, "fiber": 2}
w3 = {"energy": 1, "sugar": 2, "satu. fat.": 1, "salt": 1, "protein": 1, "fiber": 2}
w4 = {"energy": 2, "sugar": 1, "satu. fat.": 1, "salt": 1, "protein": 1, "fiber": 2}
w5 = {"energy": 1, "sugar": 1, "satu. fat.": 1, "salt": 2, "protein": 2, "fiber": 1}
w6 = {"energy": 1, "sugar": 1, "satu. fat.": 2, "salt": 1, "protein": 2, "fiber": 1}
w7 = {"energy": 1, "sugar": 2, "satu. fat.": 1, "salt": 1, "protein": 2, "fiber": 1}
w8 = {"energy": 2, "sugar": 1, "satu. fat.": 1, "salt": 1, "protein": 2, "fiber": 1}
w9 = {"energy": 1, "sugar": 1, "satu. fat.": 2, "salt": 2, "protein": 1, "fiber": 1}
w10 = {"energy": 1, "sugar": 2, "satu. fat.": 1, "salt": 2, "protein": 1, "fiber": 1}
w11 = {"energy": 2, "sugar": 1, "satu. fat.": 1, "salt": 2, "protein": 1, "fiber": 1}
w12 = {"energy": 1, "sugar": 2, "satu. fat.": 2, "salt": 1, "protein": 1, "fiber": 1}
w13 = {"energy": 2, "sugar": 1, "satu. fat.": 2, "salt": 1, "protein": 1, "fiber": 1}
w14 = {"energy": 2, "sugar": 2, "satu. fat.": 1, "salt": 1, "protein": 1, "fiber": 1}

all_experiential_weights = [w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14]


table1 = [[100, 0, 0, 0, 100, 100],
          [1550, 11, 0.8, 0.3, 10, 11],
          [1650, 14, 1, 0.4, 7, 8],
          [1750, 17, 1.7, 0.5, 4, 5],
          [1850, 20, 4, 0.6, 3, 2.5],
          [10000, 100, 100, 100, 0, 0]]


thresholds = [0.5, 0.6, 0.7]


def pessimisticMajoritySorting(inputFile, outputFile, weights, table, threshold, write_output):
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
                        p += weights.get(columns[i])
                    else:
                        r += weights.get(columns[i])
                else:
                    if foods_df.loc[prod][i] >= table[row][i]:
                        p += weights.get(columns[i])
                    else:
                        r += weights.get(columns[i])
            if p >= total_voters * threshold:
                predicted_score.append(nutri_scores.get(row))
                break

    foods_df["predicted nutri score"] = predicted_score
    if write_output:
        foods_df.to_excel(outputFile)

    pairs = []
    for i in range(len(true_score)):
        pair = (true_score[i], predicted_score[i])
        pairs.append(pair)
    return pairs


def optimisticMajoritySorting(inputFile, outputFile, weights, table, threshold, write_output):
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
        for row in range(len(table) - 1, -1, -1):
            p, r = 0, 0
            for i in range(len(table[0])):
                if i < 4:
                    if foods_df.loc[prod][i] <= table[row][i]:
                        p += weights.get(columns[i])
                    else:
                        r += weights.get(columns[i])
                else:
                    if foods_df.loc[prod][i] >= table[row][i]:
                        p += weights.get(columns[i])
                    else:
                        r += weights.get(columns[i])
            if r >= total_voters * threshold and not (p >= total_voters * threshold):
                predicted_score.append(nutri_scores.get(row + 1))
                break

    foods_df["predicted nutri score"] = predicted_score
    if write_output:
        foods_df.to_excel(outputFile)

    pairs = []
    for i in range(len(true_score)):
        pair = (true_score[i], predicted_score[i])
        pairs.append(pair)
    return pairs


def calculateAccuracy(pairs):
    accuracy = 0
    for pair in pairs:
        if pair[0] == pair[1]:
            accuracy += 1

    return accuracy / len(pairs)


def calculateConfusionMatrix(pairs, size):
    indexes = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
    matrix = [[0] * size for i in range(size)]

    for pair in pairs:
        matrix[indexes.get(pair[0])][indexes.get(pair[1])] += 1

    for row in matrix:
        print(row)

    df_cm = pd.DataFrame(matrix, range(size), range(size))
    sn.set(font_scale=1.4)
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, xticklabels=["A", "B", "C", "D", "E"],
               yticklabels=["A", "B", "C", "D", "E"], cmap="Blues")
    plt.show()


def improvedPessimistic(inputFile, weights, table, threshold, div, conv):
    start_pairs = pessimisticMajoritySorting(inputFile, "pessimistic_OpenFood_Petales.xlsx", weights, table,
                                             threshold, False)
    accuracy = calculateAccuracy(start_pairs)

    best_accuracy = accuracy
    best_table = copy.deepcopy(table)
    for row in range(1, len(table[0]) - 1):
        for col in range(0, len(table)):
            new_table1 = copy.deepcopy(table)
            if col < 4:
                new_table1[row][col] -= round((new_table1[row][col] - new_table1[row - 1][col]) / div, 2)
            else:
                new_table1[row][col] += round((new_table1[row - 1][col] - new_table1[row][col]) / div, 2)
            pairs1 = pessimisticMajoritySorting(inputFile, "pessimistic_OpenFood_Petales.xlsx", weights, new_table1,
                                                threshold, False)
            accuracy1 = calculateAccuracy(pairs1)

            new_table2 = copy.deepcopy(table)
            if col < 4:
                new_table2[row][col] += round((new_table2[row + 1][col] - new_table2[row][col]) / div, 2)
            else:
                new_table2[row][col] -= round((new_table2[row][col] - new_table2[row + 1][col]) / div, 2)
            pairs2 = pessimisticMajoritySorting(inputFile, "pessimistic_OpenFood_Petales.xlsx", weights, new_table2,
                                                threshold, False)
            accuracy2 = calculateAccuracy(pairs2)

            if accuracy1 > accuracy2 and best_accuracy < accuracy1:
                best_accuracy = accuracy1
                best_table[row][col] = new_table1[row][col]
            elif accuracy1 <= accuracy2 and best_accuracy < accuracy2:
                best_accuracy = accuracy2
                best_table[row][col] = new_table2[row][col]

    best_pairs = pessimisticMajoritySorting(inputFile, "pessimistic_OpenFood_Petales.xlsx", weights, best_table,
                                            threshold, False)

    best_accuracy = calculateAccuracy(best_pairs)
    print("accuracy", best_accuracy)
    for row in best_table:
        print(row)

    if best_accuracy == accuracy:
        conv = True

    return best_table, best_pairs, conv


def improvedOptimistic(inputFile, weights, table, threshold, div, conv):
    start_pairs = optimisticMajoritySorting(inputFile, "optimistic_OpenFood_Petales.xlsx", weights, table,
                                            threshold, False)
    accuracy = calculateAccuracy(start_pairs)

    best_accuracy = accuracy
    best_table = copy.deepcopy(table)
    for row in range(1, len(table[0]) - 1):
        for col in range(0, len(table)):
            new_table1 = copy.deepcopy(table)
            if col < 4:
                new_table1[row][col] -= round((new_table1[row][col] - new_table1[row - 1][col]) / div, 2)
            else:
                new_table1[row][col] += round((new_table1[row - 1][col] - new_table1[row][col]) / div, 2)
            pairs1 = optimisticMajoritySorting(inputFile, "optimistic_OpenFood_Petales.xlsx", weights, new_table1,
                                               threshold, False)
            accuracy1 = calculateAccuracy(pairs1)

            new_table2 = copy.deepcopy(table)
            if col < 4:
                new_table2[row][col] += round((new_table2[row + 1][col] - new_table2[row][col]) / div, 2)
            else:
                new_table2[row][col] -= round((new_table2[row][col] - new_table2[row + 1][col]) / div, 2)
            pairs2 = optimisticMajoritySorting(inputFile, "optimistic_OpenFood_Petales.xlsx", weights, new_table2,
                                               threshold, False)
            accuracy2 = calculateAccuracy(pairs2)

            if accuracy1 > accuracy2 and best_accuracy < accuracy1:
                best_accuracy = accuracy1
                best_table[row][col] = new_table1[row][col]
            elif accuracy1 <= accuracy2 and best_accuracy < accuracy2:
                best_accuracy = accuracy2
                best_table[row][col] = new_table2[row][col]

    best_pairs = optimisticMajoritySorting(inputFile, "optimistic_OpenFood_Petales.xlsx", weights, best_table,
                                           threshold, False)
    best_accuracy = calculateAccuracy(best_pairs)
    print("accuracy", best_accuracy)
    for row in best_table:
        print(row)

    if best_accuracy == accuracy:
        conv = True

    return best_table, best_pairs, conv


def runImprovedPessimistic(inputFile, weights, table, thresholds):
    div = 2
    for threshold in thresholds:
        for wghts in weights:
            new_table = copy.deepcopy(table)
            print("\n\nweights", wghts)
            i = 1
            convergence = False

            while not convergence:
                print("\nIteration", i)
                new_table, pairs, convergence = improvedPessimistic(inputFile, wghts, new_table, threshold, div,
                                                                    convergence)
                i += 1
            calculateConfusionMatrix(pairs, len(nutri_scores.keys()) - 1)


def runImprovedOptimistic(inputFile, weights, table, thresholds):
    div = 2
    for threshold in thresholds:
        for wghts in weights:
            new_table = copy.deepcopy(table)
            print("\n\nweights", wghts)
            i = 1
            convergence = False

            while not convergence:
                print("\nIteration", i)
                new_table, pairs, convergence = improvedOptimistic(inputFile, wghts, new_table, threshold, div,
                                                                   convergence)
                i += 1
            calculateConfusionMatrix(pairs, len(nutri_scores.keys()) - 1)


def find_best_weights_pessimistic(inputFile, weights, table, threshold):
    accuracies = []
    for wghts in weights:
        pairs = pessimisticMajoritySorting(inputFile, "pessimistic_OpenFood_Petales.xlsx", wghts, table,
                                           threshold, False)
        accuracy = calculateAccuracy(pairs)
        accuracies.append(accuracy)

    best_weights = []
    res = sorted(range(len(accuracies)), key=lambda sub: accuracies[sub])[-5:]
    for r in res:
        best_weights.append(weights[r])

    return best_weights


def find_best_weights_optimistic(inputFile, weights, table, threshold):
    accuracies = []
    for wghts in weights:
        pairs = optimisticMajoritySorting(inputFile, "optimistic_OpenFood_Petales.xlsx", wghts, table,
                                          threshold, False)
        accuracy = calculateAccuracy(pairs)
        accuracies.append(accuracy)

    best_weights = []
    res = sorted(range(len(accuracies)), key=lambda sub: accuracies[sub])[-5:]
    for r in res:
        best_weights.append(weights[r])

    return best_weights


print("\nPESSIMISTIC MAJORITY SORTING:")
for th in thresholds:
    pairs1 = pessimisticMajoritySorting("OpenFood_Petales.xlsx", "pessimistic_OpenFood_Petales.xlsx",
                                        weights1, table1, th, True)
    print("\nFor treshold", th, "the confusion matrix is:")
    calculateConfusionMatrix(pairs1, len(nutri_scores.keys())-1)
    accuracy1 = calculateAccuracy(pairs1)
    print("The accuracy is:", accuracy1)


print("\nOPTIMISTIC MAJORITY SORTING:")
for th in thresholds:
    pairs2 = optimisticMajoritySorting("OpenFood_Petales.xlsx", "optimistic_OpenFood_Petales.xlsx",
                                       weights1, table1, th, True)
    print("\nFor treshold", th, "the confusion matrix is:")
    calculateConfusionMatrix(pairs2, len(nutri_scores.keys())-1)
    accuracy2 = calculateAccuracy(pairs2)
    print("The accuracy is:", accuracy2)


all_best_weights_pes = find_best_weights_pessimistic("OpenFood_Petales.xlsx", all_experiential_weights, table1,
                                                     thresholds[0])
runImprovedPessimistic("OpenFood_Petales.xlsx", all_best_weights_pes, table1, thresholds)

all_best_weights_opt = find_best_weights_optimistic("OpenFood_Petales.xlsx", all_experiential_weights, table1,
                                                    thresholds[0])
runImprovedOptimistic("OpenFood_Petales.xlsx", all_best_weights_opt, table1, thresholds)


runImprovedPessimistic("OpenFood_Petales.xlsx", [w1], table1, thresholds)
runImprovedOptimistic("OpenFood_Petales.xlsx", [w6], table1, thresholds)
