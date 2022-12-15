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
    if letter == "A" or letter == "X":
        return Hand.ROCK
    elif letter == "B" or letter == "Y":
        return Hand.PAPER
    elif letter == "C" or letter == "Z":
        return Hand.SCISSORS
    else:
        raise Exception("Unknown hand letter.")

def play(opponent_hand, my_hand):
    if opponent_hand == my_hand:
        return Outcome.DRAW
    elif opponent_hand == Hand.ROCK:
        if my_hand == Hand.PAPER:
            return Outcome.WIN
        elif my_hand == Hand.SCISSORS:
            return Outcome.LOSE
    elif opponent_hand == Hand.PAPER:
        if my_hand == Hand.ROCK:
            return Outcome.LOSE
        elif my_hand == Hand.SCISSORS:
            return Outcome.WIN
    elif opponent_hand == Hand.SCISSORS:
        if my_hand == Hand.ROCK:
            return Outcome.WIN
        elif my_hand == Hand.PAPER:
            return Outcome.LOSE
    raise Exception("Unknown hand.")

def main():
    with open("input.txt") as f:
        total_score = 0
        for line in f:
            line = line.rstrip()
            opponent_hand = get_hand(line[0])
            my_hand = get_hand(line[2])
            total_score += int(my_hand)
            total_score += int(play(opponent_hand, my_hand))
    
    print(total_score)

if __name__ == "__main__":
    main()