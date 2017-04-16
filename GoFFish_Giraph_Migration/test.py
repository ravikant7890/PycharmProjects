from goto import with_goto

import matplotlib.pyplot as plt
import numpy  as np

import LossGainHelperFunctions as hf

@with_goto
def range(start, stop):
    i = start
    result = []

    label .begin
    if i == stop:
        goto .end

    result.append(i)
    i += 1
    goto .begin

    label .end
    return result

ind = np.arange(3)

a = np.array([3,6,9])
b = np.array([2,7,1])
c = np.array([0,3,1])
d = np.array([4,0,3])

p1 = plt.bar(ind, a, 1, color='#ff3333')
p2 = plt.bar(ind, b, 1, color='#33ff33', bottom=sum([a]))
p3 = plt.bar(ind, c, 1, color='#3333ff', bottom=sum([100, b]))
p4 = plt.bar(ind, d, 1, color='#33ffff', bottom=sum([100, 200, c]))

# plt.show()
# plt.show()

l=[681, 914, 457, 782, 764, 718, 400, 526, 417, 855, 595, 491, 743, 847, 1081, 1038, 568, 947, 522, 919, 336, 1978, 2373, 2813, 2299, 1992, 1064, 2183, 2924, 2167, 4908, 2720, 2682, 3961, 881, 1934, 3025, 2750, 2601, 3014]

print len(l)


bins=hf.load_balance(l,len(l))

for b in bins:

    print b.items