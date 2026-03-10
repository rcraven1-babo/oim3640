from itertools import permutations
from collections import Counter

class SpellingBeeSolver:
    def __init__(self):
        self.words = set()
        self.load_dictionary()
    
    def load_dictionary(self):
        """Load a word list from a file or online source"""
        try:
            with open('/usr/share/dict/words', 'r') as f:
                self.words = set(word.strip().lower() for word in f)
        except FileNotFoundError:
            print("Dictionary file not found. Using minimal word list.")
            self.words = {'python', 'code', 'bee', 'help'}
    
    def find_valid_words(self, center_letter, outer_letters):
        """Find all valid words using center letter and outer letters"""
        all_letters = set(outer_letters + center_letter)
        valid_words = []
        
        for word in self.words:
            # Word must contain center letter
            if center_letter not in word:
                continue
            # All letters must be in available set
            if not set(word).issubset(all_letters):
                continue
            # Minimum 4 letters
            if len(word) < 4:
                continue
            
            valid_words.append(word)
        
        return sorted(valid_words, key=len, reverse=True)
    
    def score_words(self, words):
        """Calculate points for each word"""
        scored = []
        for word in words:
            # 4-letter words = 1 point, longer = length of word
            points = 1 if len(word) == 4 else len(word)
            scored.append((word, points))
        return scored

def main():
    solver = SpellingBeeSolver()
    
    print("=== NYT Spelling Bee Solver ===")
    center = input("Enter center letter: ").lower()
    outer = input("Enter 6 outer letters: ").lower()
    
    if len(center) != 1 or len(outer) != 6:
        print("Invalid input!")
        return
    
    words = solver.find_valid_words(center, outer)
    scored = solver.score_words(words)
    
    total_points = sum(points for _, points in scored)
    print(f"\nFound {len(words)} words ({total_points} points):\n")
    
    for word, points in scored:
        print(f"{word:15} - {points} pts")

if __name__ == "__main__":
    main()