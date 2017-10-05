import pylev

f = open('../quotes.txt')
a = next(f)
for line in f:
    print(pylev.levenshtein(a, line))


