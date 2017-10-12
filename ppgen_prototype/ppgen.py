import itertools
import sys
from base64 import b64decode
import time
from pylev import levenshtein


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
        case_permuted_word = ''
        for i in range(len(words_list)):
            case_permuted_word += ' ' + casing_permutation[i] + words_list[i][1:]

        check_results(case_permuted_word[1:])
        check_results(case_permuted_word.replace(' ', ''))


def check_results(mutation_result):
    global gen_counter, phrases_cracked
    gen_counter += 1
    if gen_counter % 1e5 == 0:
        print('generated ' + str(gen_counter/1e6) + 'm passphrases')
        print('{}m/s'.format(round(gen_counter / (time.time() - starttime) / 1000) / 1000))
        for index, passphrase in enumerate(minlev):
            print('Minimum for passphrase {} had a distance of {} with: "{}"'.format(index, minlev[passphrase], best[passphrase]))

    for passphrase in phrases_to_crack:
        if mutation_result == passphrase:
            print('\nPassphrase cracked: ')
            print(mutation_result + '\n')
            print('generated ' + str(gen_counter/1e6) + 'm passphrases\n')
            phrases_cracked += 1
            if phrases_cracked == len(phrases_to_crack):
                print('Done!')
                sys.exit(0)

        distance = levenshtein(passphrase, mutation_result)
        if distance < minlev[passphrase]:
            minlev[passphrase] = distance
            best[passphrase] = mutation_result


# PROGRAM

phrases_cracked = 0
minlev = {}
best = {}
starttime = time.time()
gen_counter = 0
check_argument_validity()
phrases_to_crack_b64 = open(sys.argv[1]).read().strip().split('\n')
phrases_to_crack = []
for b in phrases_to_crack_b64:
    x = b64decode(b)
    if b.strip() == '' or x.strip() == '':
        continue
    phrases_to_crack.append(x)
    minlev[x] = 1e9
    best[x] = ''

try:
    start_generation_per_input_file()
except KeyboardInterrupt:
    print('\nppgen: received KeyboardInterrupt')
    print('generated ' + str(gen_counter) + ' passphrases\n')
else:
    print('generated ' + str(gen_counter) + ' passphrases')
    print('{}m/s'.format(gen_counter / (time.time() - starttime) / 1e6))
    print('No success')

