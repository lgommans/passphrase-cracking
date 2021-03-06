import itertools
import sys
import time
import os.path
import hashlib
import binascii
import gc


# FUNCTIONS


def binary_search(input_hash, low, high):
    if high < low:
        return -1  # no more numbers
    mid = (low + high) // 2  # midpoint in array
    if input_hash == input_hashes[mid*hashlen:(mid+1)*hashlen]:
        return mid  # number found here
    elif input_hash < input_hashes[mid*hashlen:(mid+1)*hashlen]:
        return binary_search(input_hash, low, mid - 1)  # try left of here
    else:
        return binary_search(input_hash, mid + 1, high)  # try above here


# old as fuck
def check_argument_validity():
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print('\nUsage:\t\tpypy ppgen.py <passphrases_to_crack> <seed1> <seed2> ...\n')

        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./quotes/*/albert_einstein.txt ./quotes/Aviator/*')
        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./lyrics/*/Anouk.txt ./lyrics/Metal/*\n')
        sys.exit()
    for file_path in sys.argv[2:]:
        if not os.path.isfile(file_path):
            print('\nOne of the specified files does not exist.')


def start_generation_per_seed_file():
    processed_files = []
    for file_path in sys.argv[2:]:
        if file_path not in processed_files:
            split_lines = open(file_path).read().strip().split('\n')
            sys.stderr.write('\ngenerating passphrases with ' + str(file_path) + '\n')
            generate_passphrases(split_lines)
            sys.stderr.write('generated everything for ' + str(file_path) + '\n')
            processed_files.append(file_path)
        else:
            continue


def generate_passphrases(split_lines):
    for line in split_lines:
        newline = ''
        for c in line:
            if ord(c) < 128:
                newline += c
        line = newline

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

                if 15 <= sum(len(i) for i in substring) <= 53:  # range for number of characters
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
    global gen_counter
    gen_counter += 1
    if gen_counter % 1e7 == 0:
        sys.stderr.write('Generated ' + str(gen_counter / 1e7) + 'm passphrases\n')
        sys.stderr.write('{}m/s\n'.format(round(gen_counter / (time.time() - starttime) / 1000) / 1000))

    hashed_mutation_result = hashlib.sha1(mutation_result.encode()).digest()[0:hashlen]
    search_result = binary_search(hashed_mutation_result, 0, input_hashes_length - 1)
    if search_result != -1:
        #print('\n|Passphrase cracked| \n')
        print('{} {} {}'.format(binascii.hexlify(hashed_mutation_result), search_result, mutation_result))
        #print('Hash: ' + binascii.hexlify(hashed_mutation_result) + '\n')


# PROGRAM
# RUN AS: pypy linkedincrack.py <hashes> ./lyrics/* ./quotes/*

gen_counter = 0
smallest_lev_distances = {}
closest_mutations = {}
starttime = time.time()

hashlen = 6

check_argument_validity()
f = open(sys.argv[1])
tmp = [] #open(sys.argv[1]).read().strip().splitlines()
last = None
input_hashes = ''
i = 0
for line in f:
    x = binascii.unhexlify(line.strip()[0:hashlen*2])
    if x == last:
        continue
    last = x
    tmp.append(x)
    i += 1
    if i % 1e6 == 0:
        input_hashes += ''.join(tmp)
        tmp = []

input_hashes += ''.join(tmp)
tmp = []

input_hashes_length = len(input_hashes)/hashlen

sys.stderr.write('Loaded ' + str(input_hashes_length) + ' hashes.\n')
gc.collect()

try:
    start_generation_per_seed_file()
except KeyboardInterrupt:
    print('\nppgen: received KeyboardInterrupt')
    print('generated ' + str(gen_counter) + ' passphrases\n')
else:
    print('generated ' + str(gen_counter) + ' passphrases')
    print('No success')
