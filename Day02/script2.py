from enum import IntEnum

class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Outcome(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6

def get_hand(letter):
    if letter == "A":
        return Hand.ROCK
    elif letter == "B":
        return Hand.PAPER
    elif letter == "C":
        return Hand.SCISSORS
    else:
        raise Exception("Unknown hand letter.")

def get_outcome(letter):
    if letter == "X":
        return Outcome.LOSE
    elif letter == "Y":
        return Outcome.DRAW
    elif letter == "Z":
        return Outcome.WIN
    else:
        raise Exception("Unknown outcome letter.")

def calculate_hand(opponent_hand, outcome):
    if outcome == Outcome.DRAW:
        return opponent_hand
    elif outcome == Outcome.WIN:
        if opponent_hand == Hand.ROCK:
            return Hand.PAPER
        elif opponent_hand == Hand.PAPER:
            return Hand.SCISSORS
        elif opponent_hand == Hand.SCISSORS:
            return Hand.ROCK
    elif outcome == Outcome.LOSE:
        if opponent_hand == Hand.ROCK:
            return Hand.SCISSORS
        elif opponent_hand == Hand.PAPER:
            return Hand.ROCK
        elif opponent_hand == Hand.SCISSORS:
            return Hand.PAPER
    raise Exception("Unknown hand.")

def main():
    with open("input.txt") as f:
        total_score = 0
        for line in f:
            line = line.rstrip()
            opponent_hand = get_hand(line[0])
            outcome = get_outcome(line[2])
            my_hand = calculate_hand(opponent_hand, outcome)
            total_score += int(my_hand)
            total_score += int(outcome)
    
    print(total_score)

if __name__ == "__main__":
    main()