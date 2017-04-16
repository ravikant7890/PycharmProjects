import matplotlib.pyplot as plt

dictionary = plt.figure()

D = {u'Label0':26, u'Label1': 17, u'Label2':30}

barlist=plt.bar(range(len(D)), D.values(), align='center')
plt.xticks(range(len(D)), D.keys())


barlist[0].set_color('r')

barlist[1].set_color('g')

barlist[2].set_color('c')




        # b: blue
        # g: green
        # r: red
        # c: cyan
        # m: magenta
        # y: yellow
        # k: black
        # w: white
        #


plt.show()