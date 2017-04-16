import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')




axes = plt.gca()
axes.set_xlim([xmin,xmax])
axes.set_ylim([ymin,ymax])




plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()




axes = plt.gca()
axes.set_xlim([0,155])
axes.set_ylim([0,20000])


plt.tick_params(axis='both', which='major', labelsize=14)
plt.savefig(sys.argv[2])

fig=plt.gcf()
# fig.set_size_inches(20.5, 12.5)
# sns.violinplot([df1.SS,df1.Count])
plt.grid()
plt.savefig(sys.argv[2])

plt.show()
