import matplotlib.pyplot as plt
import sys
import math

data = []

f=open(sys.argv[1],"r")

for line in f:
    if line:
        data.append(int(line[:-1]))
        

print len(data)

bins =len(set(data))


plt.xlim([min(data)-5, max(data)+5])

plt.hist(data, bins=bins, alpha=0.5)
# plt.title('Random Gaussian data (fixed number of bins)')
# plt.xlabel('variable X (20 evenly spaced bins)')
plt.ylabel('count')

plt.show()
