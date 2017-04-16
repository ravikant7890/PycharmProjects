l=[0,2,8,10,32,34,40,42]

hypercubeid=0
hypercube_map={}

for i in l:

    elements=[]
    # 0
    elements.append(i)
    elements.append(i+1)
    elements.append(i+4)
    elements.append(i+16)
    elements.append(i+64)
    # 1
    elements.append(i+1+4)
    elements.append(i+1+16)
    elements.append(i+1+64)

    # 4
    # elements.append(i+4+1)
    elements.append(i+4+16)
    elements.append(i+4+64)

    # 5
    elements.append(i+1+4+16)
    elements.append(i+1+4+64)

    #16
    elements.append(i+16+64)
    # 17
    elements.append(i+1+16+64)
    #20
    elements.append(i+4+16+64)
    # 21
    elements.append(i+4+1+16+64)


    hypercube_map[hypercubeid]=elements

    hypercubeid=hypercubeid+1





for k in hypercube_map.keys():

    hypercubeid=hypercubeid+1

    l=[]
    for v in hypercube_map[k]:

        l.append(v+128)

    hypercube_map[hypercubeid]=l


for k in hypercube_map.keys():

    print (hypercube_map[k])




print  "====================================================="


# hypercube_map=[]


l=[0,2,8,10,32,34,40,42]

hypercubeid=0
hypercube_map={}

for i in l:

    elements=[]
    # 0
    elements.append(i)
    elements.append(i+1)
    elements.append(i+4)
    elements.append(i+16)
    # elements.append(i+64)
    # 1
    elements.append(i+1+4)
    elements.append(i+1+16)
    # elements.append(i+1+64)

    # 4
    # elements.append(i+4+1)
    elements.append(i+4+16)
    # elements.append(i+4+64)

    # 5
    elements.append(i+1+4+16)
    # elements.append(i+1+4+64)

    #16
    # elements.append(i+16+64)
    # 17
    # elements.append(i+1+16+64)
    #20
    # elements.append(i+4+16+64)
    # 21
    # elements.append(i+4+1+16+64)


    hypercube_map[hypercubeid]=elements

    hypercubeid=hypercubeid+1




for k in hypercube_map.keys():

    print (hypercube_map[k])



