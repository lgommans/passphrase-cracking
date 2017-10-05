import Levenshtein

f = open('../quotes.txt')
a = next(f)
for line in f:
    print(Levenshtein.distance(a, line))


