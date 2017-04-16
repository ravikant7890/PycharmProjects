import pandas as pd
import sys
import os

df=pd.read_csv(sys.argv[1],header=None
               ,names = ["Superstep", "PID", "SGID", "Time"])


# print df.head()

df2 =df[[ "PID", "SGID","Superstep", "Time"]]

# print df["Superstep"].unique()
# print df2["Superstep"].unique()

df2["SS"]=df2["Superstep"]-2

# print df2
# print df2["SS"].unique()

df3 =df2[[ "PID", "SGID","SS", "Time"]]

# print df3["SS"].unique()
# df3.SS = df3.SS.astype(int)


# print df3.head()

# print

# print df3[ df3["SS"]==4]

# print df2.head()
#
#
df3.to_csv(sys.argv[2],index=False,header=False) #index=False skips the first column of row numbers
