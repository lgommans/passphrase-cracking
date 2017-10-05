import time

starttime = time.time()
lines = open('quotes.txt').read().split('\n')
endtime = time.time()
print("Loading: " + str(endtime - starttime))

starttime = time.time()
i = 0
a = []
for line in lines:
    tmp = line.split(' ')
    i += 1
    if len(tmp) > 3:
        test = tmp[2] + tmp[0] + tmp[1]
        if i % 250 == 0:
            a.append(test)
endtime = time.time()
print("Parsing: " + str(endtime - starttime))

