import sys

ffdList=[]
MaxList=[]
lineCount=0
FileList=[]
data=[]
with open(sys.argv[1]) as f:
    next(f)
    for line in f:

        # print (line)

        data=line.strip().split(",")
        FileList.append(data[1])
        ffd=(float(data[2])-float(data[3]))/float(data[2])
        ffdm=(float(data[2])-float(data[4]))/float(data[2])
        ffdmap = (float(data[2]) - float(data[5])) / float(data[2])
        minmax=(float(data[2])-float(data[6]))/float(data[2])
        mfp=(float(data[2])-float(data[7]))/float(data[2])
        ffdList.append(ffd)
        temp=[ffdm,ffdmap,minmax,mfp]
        print("Temp:",temp)
        maximum=max(temp)
        print("Maximum:",maximum)
        MaxList.append(maximum)


maxffdIndex=ffdList.index(max(ffdList))
maxffdFileName=FileList[maxffdIndex]

print(ffdList)
print(maxffdIndex)
print(maxffdFileName)

maxAllIndex=MaxList.index(max(MaxList))
print(MaxList)
print(maxAllIndex)
print(FileList[maxAllIndex])