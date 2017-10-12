import itertools
import sys
from base64 import b64decode
import time
import pylev
# from pylev import levenshtein
import os.path


# FUNCTIONS


def start_generation_per_seed_file():
    global starttime
    processed_files = []
    starttime = time.time()
    split_lines = open(sys.argv[1]).read().strip().split('\n')
    if not fast:
        print('\ngenerating passphrases with ' + str(sys.argv[1]))
    generate_passphrases(split_lines)
    if not fast:
        print('generated everything for ' + str(sys.argv[1]))
    processed_files.append(sys.argv[1])


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
    global total
    length = len(sentence)
    if length <= 20:  # only sentences less than 20 words
        for i in range(length):  # from 0 to length - 1
            for j in range(i, length):  # from i to length - 1
                substring = sentence[i:j + 1:]  # j + 1 since the slice is exclusive

                if 15 <= sum(len(i) for i in substring) <= 53:  # range for number of characters
                    total += 2 * (2**len(substring))
                    if fast:
                        return
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

    if gen_counter % 250000 == 0:
        sys.stdout.write('Generated ' + str(gen_counter / 1e6) + 'm passphrases,\t')
        sys.stdout.write('{}m/s         \r'.format(round(gen_counter / (time.time() - starttime) / 1000) / 1000))
        sys.stdout.flush()


def check_lev_distance(mutation_result, passphrase):
    lev_distance = pylev.wfi_levenshtein(passphrase, mutation_result)
    if lev_distance < smallest_lev_distances[passphrase]:
        smallest_lev_distances[passphrase.replace(' ', '')] = lev_distance
        closest_mutations[passphrase.replace(' ', '')] = mutation_result


# PROGRAM

gen_counter = 0
phrases_cracked = 0
smallest_lev_distances = {}
closest_mutations = {}

total = 0

if '-f' in sys.argv:
    fast = True
else:
    fast = False

try:
    start_generation_per_seed_file()
except KeyboardInterrupt:
    print('\nERROR. ABORTED EARLY.')
    print('\nppgen: received KeyboardInterrupt')
    print('generated ' + str(gen_counter) + ' passphrases\n')
except Exception as e:
    print('\nERROR. ABORTED EARLY.')
    if e.args[0] != ':)':
        raise e
else:
    if not fast:
        print('\ngenerated ' + str(gen_counter) + ' passphrases')

print('Total for {}: {}'.format(sys.argv[1], total))

if not fast:
    print('did {}m/s'.format(gen_counter / (time.time() - starttime) / 1e6))

