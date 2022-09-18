import os
import sys

def load_score_file(filepath_postfix):
    filepath = "data/score_%s.txt" % filepath_postfix
    if os.path.exists(filepath):
        ret = None
        with open(filepath, mode='r', encoding="utf-8") as f:
            lines = f.readlines()
            users = lines[0].strip().split(",")
            rounds = []
            for score_info in lines[1:]:
                round_score = []
                parts = score_info.strip().split(".")
                multi = int(parts[0])
                for i in range(0, len(users)):
                    round_score.append(multi*int(parts[1][i*3:i*3+3]))
                rounds.append(round_score)
            ret = (users, rounds)
        print("[INFO] %s loaded" % filepath)
        return ret
    else:
        print("[WARNING] file %s not exist." % filepath)
        raise Exception("File not exist. %s" % (filepath, ))


def parse_round(round):
    profit = sum(round)
    score_report = [0-x for x in round]
    winner_idx = 0
    for i in range(0, len(round)):
        if round[i] == 0:
            winner_idx = i
            break
    score_report[winner_idx] = profit
    return score_report


def print_rounds(users, rounds):
    for round in rounds:
        scores = parse_round(round)
        user_scores = list(zip(users, scores))
        user_scores.sort(key=lambda item: item[1], reverse=True)
        print(user_scores)


def gen_net_profit(rounds):
    profit = [0] * len(rounds)
    for round in rounds:
        scores = parse_round(round)
        for i in range(0, len(scores)):
            profit[i] += scores[i]
    return profit


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Need exactly one param as file postfix!")
    id = sys.argv[1]
    users, rounds = load_score_file(id)
    print_rounds(users, rounds)
    net_profit = gen_net_profit(rounds)
    print("Top list of net profit for %s rounds in %s:" % (len(rounds), id))
    sorted_net_profit = list(zip(users, net_profit))
    sorted_net_profit.sort(key=lambda item: item[1], reverse=True)
    for item in sorted_net_profit:
        print("%s: %s" % (item[0], item[1]))
    # send to output report file
    filepath = "output/report_%s.md" % id
    with open(filepath, mode='w', encoding="utf-8") as f:
        f.write("# Glare-In-Vain Score Report\n")
        f.write("### Total %s rounds on %s\n" % (len(rounds), id))

        for item in sorted_net_profit:
            f.write("- %s: %s\n" % (item[0], item[1]))
