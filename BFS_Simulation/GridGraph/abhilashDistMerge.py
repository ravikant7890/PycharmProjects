import sys
import matplotlib.pyplot as plt
import os

parent_folder=sys.argv[1]

cmd="ls -1 "+parent_folder

out_dir_list=["abhilash_livj_Meta.txt","abhilash_ORKT_Meta.txt","abhilash_USRN_Meta.txt"]



#for out_dir in os.popen(cmd).read().split("\n"):
#    if out_dir:
#       out_dir_list.append(out_dir)


print out_dir_list

# exit()

color=['b','r','g']

k=0
hd=[]

for log_dir in out_dir_list:

    x=[]
    y=[]


    with open(parent_folder+log_dir, "r") as ins:

        for line in ins:

            if "#" in line:
                pass
            else:
                degree=line[:-1].split('\t')[0]
                count=line[:-1].split('\t')[1]
                if(int(degree)!=0):
                    x.append(int(degree))
                    y.append(float(count))



    # print x

    # print y


    sum_val=sum(y)

    # print sum_val


    for i in range(0,len(y)):
        y[i]=y[i]/float(sum_val)


    for i in range(1,len(y)):
        y[i]=y[i]+y[i-1]

    max_degree=max(x)

    # plt.xlim(1,14)

    # plt.ylim(0,1.1)
    # plt.title("CDF of Degree Distribution "+sys.argv[2])
    plt.xlabel("Degree",fontsize=20)
    plt.ylabel("Percentage",fontsize=20)

    ax = plt.gca()

    # ax.set_xscale('log',basex=2)
    # ax.set_xscale('log')

    plt.yticks([0,0.2,0.4,0.6,0.8,1.0],('0','20%','40%','60%','80%','100%'),fontsize=20)

    plt.xticks(fontsize=20)

    if log_dir=='abhilash_livj_Meta.txt':
        plt.scatter(x,y, s=80,c=color[k],label="LIVJ",marker='+')
    if log_dir=='abhilash_ORKT_Meta.txt':
        plt.scatter(x,y, s=80,c=color[k],label="ORKT",marker='>')
    if log_dir=='abhilash_USRN_Meta.txt':
        plt.scatter(x,y, s=80, c=color[k],label="USRN")
#    if log_dir=='outDeg.eurn.tab':
#        plt.scatter(x,y, s=100,c=color[k],label="EURN",marker='>')
#    if log_dir=='outDeg.usaroad.tab':
#        plt.scatter(x,y, s=100, c=color[k],label="USRN")
    # hd.append(h)
    k=k+1


# plt.bar(x,y)


# plt.legend()
# plt.legend(bbox_to_anchor=(1, 0.5),prop={'size':25})
plt.ylim(0,1.1)
# plt.legend(loc='upper center', bbox_to_anchor=(0.5,1.0))
# ncol=3)
plt.legend(loc='right',prop={'size':20})
# Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

fig = plt.gcf()
fig.set_size_inches(12, 6)


# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':16})
# plt.show()


plt.savefig(sys.argv[2],bbox_inches='tight')