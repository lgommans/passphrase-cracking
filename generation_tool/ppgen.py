import itertools
import sys

phrases_to_crack = []
gen_counter = 0


# FUNCTIONS

def check_argument_validity():
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv: 
        print('\nUsage:\t\tpypy ppgen.py <passphrases_to_crack> <seed1> <seed2> ...\n')
	
        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./quotes/*/albert_einstein.txt ./quotes/Celebrity/*\n')
        print('Example usage:\tpypy ppgen.py ./to_crack.txt ./lyrics/*/Anouk.txt ./lyrics/Metal/*\n')
	sys.exit()


def start_generation_per_input_file():
    for input_file in sys.argv[2:]:
        split_lines = open(input_file).read().strip().split('\n')
        generate_passphrases(split_lines)
	print('generated everything for ' + str(input_file))


def generate_passphrases(split_lines):
    for line in split_lines:
	while ',' in line or "'" in line or ':' in line or ';' in line:
	    line = line.strip().replace(',','.').replace("'",'').replace(':','.').replace(';','.')
        split_line = line.split('.')
	
	while '' in split_line: 
	    split_line.remove('')
	if len(split_line) == 0:
	    continue
	
        for sentence in split_line:
            get_all_substrings(sentence)


def get_all_substrings(sentence):
    length = len(sentence)
    if length <= 24:
        for i in xrange(length):
	    for j in xrange(i, length):
	        substring = sentence[i:j+1:]
	        joined_substring = ' '.join(substring)
	    
	        if 16 < len(joined_substring) < 48:
                    permute_based_on_casing(substring)


def permute_based_on_casing(words_list):
    all_first_chars = ''
    for word in words_list:
	if len(word) != 0:
            all_first_chars += word[0] 
    
    casing_permutations = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in all_first_chars)))
    for casing_permutation in casing_permutations:
	case_permuted_words = []
	
	for i in xrange(len(words_list)):
            current_word = words_list[i]
	    if len(current_word) == 1:
                cased_word = casing_permutation[i]
            else:
                cased_word = casing_permutation[i] + words_list[i][1::]
	    case_permuted_words.append(cased_word)
	
	permute_based_on_spacing(case_permuted_words)


def permute_based_on_spacing(words):
    no_whitespace = ''.join(words)
    with_whitespace = ' '.join(words)
    cmp_phrase_with_input_phrases(no_whitespace)
    cmp_phrase_with_input_phrases(with_whitespace)
 

def cmp_phrase_with_input_phrases(mutation_result):
    global gen_counter, phrases_to_crack 
    gen_counter += 1
    if gen_counter % 10000000 == 0:
	print('generated ' + str(gen_counter) + ' passphrases')
    
    for passphrase in phrases_to_crack:
        if passphrase == mutation_result:
            print('Passphrase cracked: ')
    	    print(passphrase + '\n')
	    print('generated ' + str(gen_counter) + ' passphrases\n')
	    sys.exit(1)


# PROGRAM

check_argument_validity()
phrases_to_crack = open(sys.argv[1]).read().strip().split('\n')
start_generation_per_input_file()
print('generated ' + str(gen_counter) + ' passphrases')
print('No success')



