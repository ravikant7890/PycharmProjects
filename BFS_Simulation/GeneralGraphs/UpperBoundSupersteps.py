import numpy
import sys
import matplotlib.pyplot as plt

import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom



# print ncr(5,3)

#radius of metagraph
radius=int(sys.argv[1])

#daimeter of original graph
diameter=min(int(sys.argv[2]),int(sys.argv[3]))

total=[]

cost=[]

j=0

for i in range(radius,diameter+1,1):

    # total[j]=ncr(diameter+1,i)
    total.append(ncr(diameter+1,i))

    # cost[j]=i
    cost.append(i)

    j=j+1


expected_val=0

print total

x=[]
total_sum=sum(total)

for i in range(0,len(total)):

    expected_val=expected_val+(cost[i]*  total[i] / float(total_sum))
    x.append(total[i] /float( total_sum))



print
print expected_val


plt.xlabel("Expected Value of Superstep")

plt.ylabel("Probability")

plt.title(sys.argv[4])

plt.scatter(cost,x)
xposition = [int(sys.argv[5])]
for xc in xposition:
    plt.axvline(x=xc, color='k', linestyle='--')

# plt.savefig(sys.argv[6])

plt.show()