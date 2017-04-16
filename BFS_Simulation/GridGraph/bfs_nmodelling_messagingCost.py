from collections import Counter
import sys
import math


def frontier_size_1d(superstep,n):

    if(superstep==0):
        return 1

    if(superstep > 0 and superstep <= int(math.floor(n/2))):
        return 2

    if(superstep >int(math.floor(n/2))):
        return 0


#params:
#d: dimension
#superstep: iteration number
#max_ss_count : maximum number of SS

def calc_frontier_size(d,superstep,max_ss,n):

    # print "calc_frontier_size("+str(d)+","+str(superstep)+","+str(max_ss)+")"
    itrCount=min(superstep,int(math.floor(n/2)))

    if(d==0):
        return 0

    if (d==1):

        return (frontier_size_1d(superstep,n))

    else:

        tmp=0
        ss=superstep-1
        for k in range(itrCount,0,-1):

           tmp = tmp + calc_frontier_size(d-1,ss , max_ss,n)
           ss=ss-1


        # print "2*tmp: "+str(2*tmp)

        return calc_frontier_size(d-1,superstep,max_ss,n)+ 2*tmp


if __name__ == '__main__':

    n = int(sys.argv[1])

    d = int(sys.argv[2])

    out_file=sys.argv[3]

    num_v = n^d

    max_ss = int(d* math.floor(n/2))

    outfile = open(out_file, 'w')

    outfile.write(str(0)+"\n")

    for i in range(0,max_ss+1):

        print calc_frontier_size(d,i,max_ss,n)*(d*2)

        outfile.write(str(calc_frontier_size(d,i,max_ss,n)*(d*2))+"\n")

    outfile.close()
    # print frontier_size_1d(3,6)
