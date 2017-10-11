import itertools
import sys


# FUNCTIONS

def check_argument_validity():
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print('\nUsage:\t\tpypy ppgen.py <passphrases_to_crack> <seed1> <seed2> ...\n')

        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./quotes/*/albert_einstein.txt ./quotes/Aviator/*')
        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./lyrics/*/Anouk.txt ./lyrics/Metal/*\n')
        sys.exit()


def start_generation_per_input_file():
    for input_file in sys.argv[2:]:
        split_lines = open(input_file).read().strip().split('\n')
        print('\ngenerating passphrases with ' + str(input_file))
        generate_passphrases(split_lines)
        print('generated everything for ' + str(input_file))


def generate_passphrases(split_lines):
    for line in split_lines:
        while ',' in line or "'" in line or ':' in line or ';' in line:
            line = line.strip().replace(',', '.').replace("'", '').replace(':', '.').replace(';', '.')
        split_line = line.split('.')

        while '' in split_line:
            split_line.remove('')
        if len(split_line) == 0:
            continue

        for sentence in split_line:
            generate_all_substrings(sentence.strip().split())


def generate_all_substrings(sentence):
    length = len(sentence)
    if length <= 20:  # only sentences less than 20 words
        for i in range(length):  # from 0 to length - 1
            for j in range(i, length):  # from i to length - 1
                substring = sentence[i:j + 1:]  # j + 1 since the slice is exclusive

                if 12 <= sum(len(i) for i in substring) <= 64:  # only in the range of 12 to 64 characters
                    permute_based_on_casing(substring)


def permute_based_on_casing(words_list):
    all_first_chars = ''
    for word in words_list:
        if len(word) != 0:
            all_first_chars += word[0]
    casing_permutations = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in all_first_chars)))

    for casing_permutation in casing_permutations:
        case_permuted_words = []
        for i in range(len(words_list)):
            current_word = words_list[i]
            cased_word = casing_permutation[i] + current_word[1:]
            case_permuted_words.append(cased_word)

        permute_based_on_spacing(case_permuted_words)


def permute_based_on_spacing(words):
    no_whitespace = ''.join(words)
    with_whitespace = ' '.join(words)
    check_results(no_whitespace)
    check_results(with_whitespace)


def check_results(mutation_result):
    global gen_counter, phrases_to_crack
    gen_counter += 1
    if gen_counter % 2500000 == 0:
        print('generated ' + str(gen_counter) + ' passphrases')

    for passphrase in phrases_to_crack:
        if mutation_result == passphrase:
            print('\nPassphrase cracked: ')
            print(mutation_result + '\n')
            print('generated ' + str(gen_counter) + ' passphrases\n')
            sys.exit()


# PROGRAM

gen_counter = 0
check_argument_validity()
phrases_to_crack = open(sys.argv[1]).read().strip().split('\n')

try:
    start_generation_per_input_file()
except KeyboardInterrupt:
    print('\nppgen: received KeyboardInterrupt')
    print('generated ' + str(gen_counter) + ' passphrases\n')
    sys.exit()
print('generated ' + str(gen_counter) + ' passphrases')
print('No success')



