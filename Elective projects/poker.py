import itertools
import random
from collections import Counter

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUITS = {'S', 'H', 'D', 'C'}

HAND_RANKS = {
    'High Card': 1,
    'One Pair': 2,
    'Two Pair': 3,
    'Three of a Kind': 4,
    'Straight': 5,
    'Flush': 6,
    'Full House': 7,
    'Four of a Kind': 8,
    'Straight Flush': 9,
    'Royal Flush': 10
}


def build_deck():
    return [rank + suit for rank in RANK_ORDER for suit in SUITS]


def parse_card(card_str):
    card_str = card_str.strip().upper()
    if len(card_str) != 2:
        raise ValueError(f"Invalid card format: {card_str}")
    rank, suit = card_str[0], card_str[1]
    if rank not in RANK_ORDER or suit not in SUITS:
        raise ValueError(f"Invalid card: {card_str}")
    return rank + suit


def parse_hand(hand_str):
    cards = hand_str.replace(',', ' ').split()
    if len(cards) != 2:
        raise ValueError("A Texas Hold'em hand must contain exactly 2 cards.")
    parsed = [parse_card(card) for card in cards]
    if len(set(parsed)) != 2:
        raise ValueError("Duplicate cards are not allowed.")
    return parsed


def is_flush(cards):
    return len({card[1] for card in cards}) == 1


def is_straight(ranks):
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False, None
    if ranks[-5:] == [2, 3, 4, 5, 14]:
        return True, 5
    for i in range(len(ranks) - 4):
        window = ranks[i:i + 5]
        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]
    return False, None


def hand_value(cards):
    ranks = sorted([RANK_ORDER[c[0]] for c in cards])
    rank_counts = Counter(ranks)
    flush = is_flush(cards)
    straight, high_straight = is_straight(ranks)

    counts = sorted(rank_counts.values(), reverse=True)
    ordered_ranks = sorted(rank_counts.items(), key=lambda x: (-x[1], -x[0]))
    rank_list = [rank for rank, _ in ordered_ranks]

    if straight and flush:
        if high_straight == 14:
            return (HAND_RANKS['Royal Flush'], 14)
        return (HAND_RANKS['Straight Flush'], high_straight)
    if counts == [4, 1]:
        return (HAND_RANKS['Four of a Kind'], rank_list[0], rank_list[1])
    if counts == [3, 2]:
        return (HAND_RANKS['Full House'], rank_list[0], rank_list[1])
    if flush:
        return (HAND_RANKS['Flush'],) + tuple(sorted(ranks, reverse=True))
    if straight:
        return (HAND_RANKS['Straight'], high_straight)
    if counts == [3, 1, 1]:
        return (HAND_RANKS['Three of a Kind'], rank_list[0], rank_list[1], rank_list[2])
    if counts == [2, 2, 1]:
        return (HAND_RANKS['Two Pair'], rank_list[0], rank_list[1], rank_list[2])
    if counts == [2, 1, 1, 1]:
        kicker = sorted([r for r in ranks if r != rank_list[0]], reverse=True)
        return (HAND_RANKS['One Pair'], rank_list[0]) + tuple(kicker)
    return (HAND_RANKS['High Card'],) + tuple(sorted(ranks, reverse=True))


def best_hand_from_seven(cards):
    best_value = None
    for combo in itertools.combinations(cards, 5):
        value = hand_value(combo)
        if best_value is None or value > best_value:
            best_value = value
    return best_value


def compare_values(value1, value2):
    if value1 > value2:
        return 1
    if value1 < value2:
        return -1
    return 0


def simulate_holdem(player_hand, opponents, trials=1000):
    wins = ties = losses = 0
    for _ in range(trials):
        deck = build_deck()
        for card in player_hand:
            deck.remove(card)

        random.shuffle(deck)
        community = deck[:5]
        remaining = deck[5:]

        player_best = best_hand_from_seven(player_hand + community)

        opponent_results = []
        for i in range(opponents):
            opp_hand = remaining[i*2:(i+1)*2]
            opponent_best = best_hand_from_seven(opp_hand + community)
            opponent_results.append(compare_values(player_best, opponent_best))

        if all(result == 1 for result in opponent_results):
            wins += 1
        elif any(result == -1 for result in opponent_results):
            losses += 1
        else:
            ties += 1
    return wins, ties, losses


def format_percentage(count, total):
    return f"{count} ({count / total * 100:.1f}%)"


def input_card(card_number):
    while True:
        suit = input(f"Enter suit for card {card_number} (S/H/D/C): ").strip().upper()
        if suit not in SUITS:
            print("Invalid suit. Use S, H, D, or C.")
            continue
        rank = input(f"Enter rank for card {card_number} (2-9, T, J, Q, K, A): ").strip().upper()
        if rank not in RANK_ORDER:
            print("Invalid rank. Use 2-9, T, J, Q, K, or A.")
            continue
        card = rank + suit
        return card


def input_hole_cards():
    print("Enter your hole cards by suit then rank.")
    first_card = input_card(1)
    second_card = input_card(2)
    if first_card == second_card:
        raise ValueError("Duplicate cards are not allowed.")
    return [first_card, second_card]


def main():
    print("Texas Hold'em Hand Tester")
    print("You will choose two hole cards by suit first, then rank.")

    while True:
        try:
            player_hand = input_hole_cards()
            break
        except ValueError as exc:
            print(f"Error: {exc}")

    while True:
        try:
            opponents = int(input("How many opponents? "))
            if opponents < 1 or opponents > 8:
                print("Choose between 1 and 8 opponents.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number.")

    print("Running 1,000 Texas Hold'em simulations...")
    wins, ties, losses = simulate_holdem(player_hand, opponents, trials=1000)

    print("\n--- Simulation Results ---")
    print(f"Your hole cards: {' '.join(player_hand)}")
    print(f"Opponents: {opponents}")
    print(f"Wins: {format_percentage(wins, 1000)}")
    print(f"Ties: {format_percentage(ties, 1000)}")
    print(f"Losses: {format_percentage(losses, 1000)}")

    print("\nThank you for using the Texas Hold'em hand tester.")


if __name__ == '__main__':
    main()
