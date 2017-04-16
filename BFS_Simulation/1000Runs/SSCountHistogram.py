import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt

import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom



df=pd.read_csv(sys.argv[1],low_memory=False)


print df.columns




mask = df['RECVD_MSG'] > 0
# print df1.head()

df1=df[mask]


print len(df)

print len(df1)


exit()

# print df.head(5)
# exit()
# df2=df.head(5)
df2=df1

# print df2

df3=  df2.groupby(['Source','Source_SG'])['Superstep'].max()

# df3= df2.groupby(['Source','Source_SG']).size().reset_index(name='Superstep')

df4=df3.reset_index(name='Superstep')

# print df3.columns

print df4.head(5)

# exit()
# pd.DataFrame.hist(df4,column='Superstep',color="green")

x=df4['Superstep']

# print x


hist={}

for ss in x:

    if ss in hist.keys():

        k=hist[ss]
        hist[ss]=k+1
    else:
        hist[ss]=1

print hist

t=sum(hist.values())

y=[]
x1=[]
for ss in hist.keys():
        k=hist[ss]
        # hist[ss]=k/float(t)
        y.append(k/float(t))
        x1.append(ss)

print hist


print x1

print y

# plt.ylim(0,1)

plt.bar(x1,y)
# fig, ax = plt.subplots(1,2, figsize=(10,4))
#
# # ax[0].hist(x, normed=True, color='grey')
#
# np.histogram(x)
# ax.bar(bins[:-1], hist.astype(np.float32) / hist.sum(), width=(bins[1]-bins[0]), color='grey')

# ax[0].set_title('normed=True')
# ax.set_title('hist = hist / hist.sum()')

# plt.show()

# exit()
# print df3
#
#
#
#
# df3.reset_index(name='Superstep')
#
# print df3


# print ncr(5,3)

#radius of metagraph
radius=int(sys.argv[2])

#daimeter of original graph
diameter=min(int(sys.argv[3]),int(sys.argv[4]))

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

plt.title(sys.argv[5])

plt.scatter(cost,x,color="r",marker='*')
# xposition = [int(sys.argv[5])]
# for xc in xposition:
#     plt.axvline(x=xc, color='k', linestyle='--')

# plt.savefig(sys.argv[6])

plt.show()