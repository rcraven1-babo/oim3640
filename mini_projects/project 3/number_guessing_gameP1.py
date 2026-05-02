import random


def print_welcome():
    print("\n=== Number Guessing Game with AI ===")
    print("Choose one of two modes and track your progress across rounds.")
    print("1) You guess the computer's number")
    print("2) Computer guesses your number")
    print("S) Show stats")
    print("R) Reset stats")
    print("Q) Quit")


def get_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a number <= {max_value}.")
                continue
            return value
        except ValueError:
            print("That wasn't a valid number. Try again.")


def show_stats(stats):
    print("\n=== Game Statistics ===")
    if stats["rounds_played"] == 0:
        print("No rounds played yet. Start a game to build stats.")
        return

    print(f"Rounds played: {stats['rounds_played']}")
    print(f"You guessed the computer's number: {stats['user_guess_rounds']} rounds")
    print(f"Computer guessed your number: {stats['computer_guess_rounds']} rounds")
    if stats["user_guess_rounds"]:
        print(f"  Best user guess attempts: {stats['best_user_attempts']}")
        print(f"  Worst user guess attempts: {stats['worst_user_attempts']}")
        print(f"  Average user guess attempts: {stats['total_user_attempts'] / stats['user_guess_rounds']:.1f}")
    if stats["computer_guess_rounds"]:
        print(f"  Best computer guess attempts: {stats['best_computer_attempts']}")
        print(f"  Worst computer guess attempts: {stats['worst_computer_attempts']}")
        print(f"  Average computer guess attempts: {stats['total_computer_attempts'] / stats['computer_guess_rounds']:.1f}")


def update_stats(stats, mode, attempts):
    stats["rounds_played"] += 1
    if mode == "user_guess":
        stats["user_guess_rounds"] += 1
        stats["total_user_attempts"] += attempts
        stats["best_user_attempts"] = (
            attempts if stats["best_user_attempts"] is None else min(stats["best_user_attempts"], attempts)
        )
        stats["worst_user_attempts"] = max(stats["worst_user_attempts"], attempts)
    else:
        stats["computer_guess_rounds"] += 1
        stats["total_computer_attempts"] += attempts
        stats["best_computer_attempts"] = (
            attempts if stats["best_computer_attempts"] is None else min(stats["best_computer_attempts"], attempts)
        )
        stats["worst_computer_attempts"] = max(stats["worst_computer_attempts"], attempts)


def reset_stats(stats):
    stats.update({
        "rounds_played": 0,
        "user_guess_rounds": 0,
        "computer_guess_rounds": 0,
        "total_user_attempts": 0,
        "total_computer_attempts": 0,
        "best_user_attempts": None,
        "worst_user_attempts": 0,
        "best_computer_attempts": None,
        "worst_computer_attempts": 0,
    })
    print("Stats have been reset.")


def user_guesses_game(stats):
    print("\nYou chose: You guess the computer's number.")
    low, high = 1, 100
    print(f"Think of a number between {low} and {high}, and I'll choose one.")
    secret = random.randint(low, high)
    attempts = 0

    while True:
        guess = get_int("Your guess: ", low, high)
        attempts += 1

        if guess == secret:
            print(f"Correct! You found it in {attempts} attempts.")
            break

        if guess < secret:
            print("Too low. Try a higher number.")
        else:
            print("Too high. Try a lower number.")

        if attempts == 3:
            print("Hint: Use the size of the remaining range to narrow faster.")

    update_stats(stats, "user_guess", attempts)


def computer_guesses_game(stats):
    print("\nYou chose: Computer guesses your number.")
    low, high = 1, 100
    print(f"Think of a number between {low} and {high}. I will guess it.")
    input("Press Enter when you're ready...")

    attempts = 0
    while low <= high:
        guess = (low + high) // 2
        attempts += 1
        print(f"I guess {guess}.")

        answer = input("Is your number higher (H), lower (L), or correct (C)? ").strip().lower()
        if answer.startswith("c"):
            print(f"Yes! I found your number in {attempts} guesses.")
            break
        if answer.startswith("h"):
            low = guess + 1
            print("Got it — I will guess higher.")
        elif answer.startswith("l"):
            high = guess - 1
            print("Got it — I will guess lower.")
        else:
            print("Please enter H, L, or C.")
            attempts -= 1
            continue

        if low > high:
            print("Hmm, that doesn't match the answers. Let's try again more carefully.")
            low, high = 1, 100
            attempts = 0
            input("Think of a number again and press Enter.")

    update_stats(stats, "computer_guess", attempts)


def main():
    stats = {
        "rounds_played": 0,
        "user_guess_rounds": 0,
        "computer_guess_rounds": 0,
        "total_user_attempts": 0,
        "total_computer_attempts": 0,
        "best_user_attempts": None,
        "worst_user_attempts": 0,
        "best_computer_attempts": None,
        "worst_computer_attempts": 0,
    }

    while True:
        print_welcome()
        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            user_guesses_game(stats)
        elif choice == "2":
            computer_guesses_game(stats)
        elif choice == "s":
            show_stats(stats)
        elif choice == "r":
            reset_stats(stats)
        elif choice == "q":
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid choice. Please select 1, 2, S, R, or Q.")


if __name__ == "__main__":
    main()
