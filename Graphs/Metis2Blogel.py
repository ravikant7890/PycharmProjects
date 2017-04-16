import sys


# f1=open(sys.argv[1],'r')
f2=open(sys.argv[2],'w')
zenda=True
vertex_id=1
with open(sys.argv[1]) as f:
    for line in f:
        if zenda:
            zenda=False
            continue
        neighbours=line.split()
        print neighbours
        v_line=str(vertex_id)+"\t"+str(len(neighbours))
        for n in neighbours:
            v_line=v_line+" "+str(n)
        v_line=v_line+"\n"
        vertex_id=vertex_id+1
        print v_line
        f2.write(v_line)

