import matplotlib.pyplot as plt
import pandas as pd
import sys
import matplotlib


df=pd.read_csv(sys.argv[1])

x=df['SS']

y=df['MSG']

plt.scatter(x,y)


font = {'family' : 'normal',
        'weight' : 'normal', #bold
        'size'   : 20}

matplotlib.rc('font', **font)


axes = plt.gca()
axes.set_xlim([0,1000])
axes.set_ylim([0,9000])


plt.xlabel('Superstep')
plt.ylabel('Messages Sent')
plt.title('Messaging Cost for 2D grid [n=1001]')

plt.grid(True)

plt.tick_params(axis='both', which='major', labelsize=14)

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(12, 6)

# plt.figure(figsize=(8,20))
# plt.show()
plt.savefig(sys.argv[2])