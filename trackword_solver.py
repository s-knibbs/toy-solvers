import sys

# SSolver for the trackword puzzle in the radiotimes,
# Basically an anagram solver.

def get_word_list(word_list_file: str) -> set[str]:
    words = set()
    with open(word_list_file) as words_file:
        for line in words_file:
            word = line.strip()
            if "'" not in word and len(word) == 9:
                words.add(word.lower())
    return words


def main(clue: str):
    words = get_word_list('/usr/share/dict/british-english-large')
    clue_set = set(clue)
    for word in words:
        # is anagram of word
        if set(word) == clue_set:
            print(word)
            break


if __name__ == "__main__":
    main(sys.argv[1])