from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
import sys
import re


# Solver for the radio time enigma code puzzle.

# Todo this untested.

ALPHABET = "abcdefghijklmnopqrstuvxyz"


@dataclass
class Problem:
    clues: list[str]
    normalised_words: dict[str, list[str]]
    solution: dict[int, str]


def read_problem(path: str) -> list[list[int]]:
    problem_rows = []
    problem_columns = [[] for _ in range(13)]
    with open(path) as problem_file:
        for line in problem_file:
            problem_rows.append(line)
            for idx, char in enumerate(line):
                problem_columns[idx].append(line)

    problem_columns = [''.join(item) for item in problem_columns]


    clues = []
    for series in problem_rows + problem_columns:
        for clue in series.split():
            if clue != ',':
                clues.append([int(x) for x in clue.strip(',').split(',')])
    return clues


def normalise_word(word: str | list[int]) -> str:
    char_map = {}
    char_idx = 0
    new_word = []
    for char in word:
        new_char = char_map.get(char, ALPHABET[char_idx])
        new_word.append(new_char)
        if char not in char_map:
            char_map[char] = new_char
            char_idx += 1
    return ''.join(new_word)


def check_candidate(candidate: str, clue: list[int], solution: dict[int, str]) -> bool:
    return re.match(''.join(solution.get(char, '.') for char in clue), candidate) is not None


def common_letters(candidates: list[str]) -> str:
    common_cand = list(candidates[0])
    for cand in candidates[1:]:
        for idx, char in enumerate(cand):
            if common_cand[idx] != char:
                common_cand[idx] = '.'
    return ''.join(common_cand)


def solve(prob: Problem) -> dict[int, str]:
    num_solved = 0
    for clue in prob.clues:
        norm_clue = normalise_word(clue)
        candidates = []
        for cand in prob.normalised_words[norm_clue]:
            if check_candidate(cand, clue, prob.solution):
                candidates.append(cand)
        common_candidate = common_letters(candidates)
        for clue_char, word_char in zip(clue, common_candidate):
            if word_char != '.' and clue_char not in prob.solution:
                prob.solution[clue_char] = word_char
                num_solved += 1
    if len(prob.solution) == 26 or num_solved == 0:
        return prob.solution
    else:
        return solve(prob)


def get_word_list(word_list_file: str) -> set[str]:
    words = set()
    with open(word_list_file) as words_file:
        for line in words_file:
            word = line.strip()
            if "'" not in word:
                words.add(word.lower())
    return words


def main():
    clues = read_problem(sys.argv[1])
    words = get_word_list('/usr/share/dict/british-english-large')
    normalised_words = defaultdict(list)
    for word in words:
        normalised_words[normalise_word(word)].append(word)



if __name__ == "__main__":
    main()

