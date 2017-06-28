# input csv pid,ss,wid
# output updated first loading

import pandas as pd

import os
import sys

df=pd.read_csv(sys.argv[1],header=None,names = ["PID", "SS", "WID"])

print df.head()

df=df.ix[~(df['PID'] > 40)]

df2=df.sort(['PID', 'SS'], ascending=[True, True])

df2.to_csv("test.csv")

print "=========sort by PID n SS ================="

print df2.head()



for i in range(0,40):
    print int(df2.loc[df['PID'] == i,'SS'].min())



# print "=========group by PID n SS ================="
#
# df3=df2.groupby(['PID', 'SS'])

# print df3.head()