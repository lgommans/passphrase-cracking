import itertools

# FUNCTIONS

# import pylev
#
# f = open('../quotes.txt')
# a = next(f)
# for line in f:
#     print(pylev.levenshtein(a, line))


def start_passphrase_generation(quotes):
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

        if 12 < len(subsentence_str) < 48:
            print(subsentence)
            permute_based_on_casing(subsentence)


def permute_based_on_casing(state):
    all_first_chars = ''
    for word in state:
        all_first_chars += word[0]
    possible_casings = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in all_first_chars)))
    print possible_casings

    for casing_permutation in possible_casings:
        print casing_permutation
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
    no_spaces = ''.join(state)
    print no_spaces
    with_spaces = ' '.join(state)
    print with_spaces


# PROGRAM

all_quotes = open('person.txt').read().strip().split('\n')
first_line = all_quotes[0]
start_passphrase_generation(all_quotes)



