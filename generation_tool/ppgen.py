import itertools
import sys

phrases_to_crack = []
gen_counter = 0


# FUNCTIONS

def check_argument_validity():
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv: 
        print('\nUsage:\t\tpypy ppgen.py <passphrases_to_crack> <seed1> <seed2> ...')
	print('Example usage:\tpypy ppgen.py ./pp_file.txt ./quotes/*/albert_einstein.txt ./quotes/Celebrity/*\n')        
	sys.exit()


def generate_passphrases(quotes):
    for quote in quotes[1:]:
        quote_sections = quote[:-1:].strip().replace('.', ',').split(',')

        for section in quote_sections:
            temp = section.split(' ')
            to_permute_str = ' '.join(temp).strip()
            to_permute = to_permute_str.split(' ')
            split_up_sentence(to_permute)


def split_up_sentence(sentence_to_permute):
    for length in range(len(sentence_to_permute)):
        subsentence = sentence_to_permute[:(length + 1):]
        subsentence_str = ' '.join(subsentence)

        if 8 < len(subsentence_str) < 48:
            permute_based_on_casing(subsentence)


def permute_based_on_casing(state):
    all_first_chars = ''
    for word in state:
        all_first_chars += word[0]
    possible_casings = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in all_first_chars)))

    for casing_permutation in possible_casings:
        case_permuted_subsentence = []
        
	for i in range(len(state)):
            current_word = state[i]
            
	    if len(current_word) == 1:
                cased_word = casing_permutation[i]
            else:
                cased_word = casing_permutation[i] + state[i][1::]
	    case_permuted_subsentence.append(cased_word)
	
	permute_based_on_spacing(case_permuted_subsentence)


def permute_based_on_spacing(state):
    no_whitespace = ''.join(state)
    with_whitespace = ' '.join(state)
    permute_special_chars(no_whitespace)
    permute_special_chars(with_whitespace)    


def permute_special_chars(state):
    if "'" in state:
    	alternative_state = state.replace("'", '')
	cmp_phrase_with_input_phrases(alternative_state)
    # add additional rules
    cmp_phrase_with_input_phrases(state)       
  
 
def cmp_phrase_with_input_phrases(state):
    global gen_counter, phrases_to_crack 
    gen_counter += 1
    if gen_counter % 250000 == 0:
	print('generated ' + str(gen_counter) + ' passphrases')
    
    for passphrase in phrases_to_crack:
        if passphrase == state:
            print('Passphrase cracked: ')
    	    print(passphrase + '\n')
	    print('generated ' + str(gen_counter) + ' passphrases\n')
	    sys.exit(1)


# PROGRAM

check_argument_validity()
phrases_to_crack = open(sys.argv[1]).read().strip().split('\n')

for arg in sys.argv[2:]:
    all_lines = open(arg).read().strip().split('\n')
    metadata = all_lines[0]
    generate_passphrases(all_lines)
    print('generated everything for ' + arg)

print('generated ' + str(gen_counter) + ' passphrases')
print('No success')
