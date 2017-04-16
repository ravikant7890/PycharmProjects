import sys
import matplotlib.pyplot as plt

x=[]
y=[]

with open(sys.argv[1], "r") as ins:

    for line in ins:

        if "#" in line:
            pass
        else:
            degree=line[:-1].split('\t')[0]
            count=line[:-1].split('\t')[1]
            if(int(degree)!=0):
                x.append(int(degree))
                y.append(float(count))



print x

# print y


sum_val=sum(y)

print sum_val


for i in range(0,len(y)):
    y[i]=y[i]/float(sum_val)


for i in range(1,len(y)):
    y[i]=y[i]+y[i-1]

max_degree=max(x)

# plt.xlim(1,14)

plt.ylim(0,1.1)
plt.title("CDF of Degree Distribution "+sys.argv[2])
plt.xlabel("Degree")
plt.ylabel("Percentage")
plt.xlim(xmin=0)
plt.xlim(xmax=500)
ax = plt.gca()

# ax.set_xscale('log',basex=2)
#ax.set_xscale('log')

plt.yticks([0,0.2,0.4,0.6,0.8,1.0],('0','20%','40%','60%','80%','100%'))

plt.scatter(x,y)
# plt.bar(x,y)
# plt.show()

# plt.close()
plt.savefig(sys.argv[3]+".pdf")