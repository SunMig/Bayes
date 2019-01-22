from array import array
from math import log

from numpy import *
from numpy.ma import zeros


def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 代表侮辱性文字, 0 not
    return postingList,classVec

def createVocaList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)

    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print('the word: %s is not in my Vocabulary!'%(word))
    return returnVec

#朴素贝叶斯词袋模型
def bagOfWordsVecMn(vocablist,inputSet):
    returnVec=[0]*len(vocablist)
    for word in inputSet:
        if word in vocablist:
            returnVec[vocablist.index(word)]+=1

    return returnVec

# 朴素贝叶斯分类器训练函数
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    #避免因为一个概率值0而出现的最终概率为零的情况
    p0Num=ones(numWords);p1Num=ones(numWords)
    p0Denom=2.0;p1Denom=2.0;
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
    #连续的小数相乘会造成程序下溢，为避免此情况出现可通过求对数来避免这种情况的出现
    p1Vect=log(p1Num/p1Denom) #对每个元素除以该类别中的总词数
    p0Vect=log(p0Num/p0Denom)
    print(p1Num)
    print(p0Num)
    print(p1Denom)
    print(p0Denom)
    return p0Vect,p1Vect,pAbusive

#朴素贝叶斯分类函数（这是个0-1的二值问题）
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

#此函数是一个测试函数，便于主程序的实现
def testingNB():
    listOPosts,listClasses=loadDataSet()
    myVocabList=createVocaList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
    print(trainMat)
    p0V,p1V,pAb=trainNB0(array(trainMat),array(listClasses))
    testEntry=['love','my','dalmation']
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
    print(str(testEntry)+' classified as: '+str(classifyNB(thisDoc,p0V,p1V,pAb)))
    testEntry=['stupid','garbage']
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
    print(str(testEntry) + ' classified as: ' + str(classifyNB(thisDoc, p0V, p1V, pAb)))

#使用朴素贝叶斯进行交叉验证
def textParse(bigString):
    import re
    listOfTokens=re.split(r'\w*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamTest():
    docList=[];classList=[];fullText=[];
    #导入并解析文本文件
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt'% i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(open('email/ham/%d.txt'% i).read()) #文件有乱码，要注意这一点
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocaList(docList)
    trainingSet=list(range(50));testSet=[]
    #随机选择10个文件作为测试集，剩下的文件作为交叉验证的依据
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])#python3不返回range对象，因此要把trainingSet定义成list

    trainMat=[];trainClass=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClass.append(classList[docIndex])

    p0V,p1V,pSpam=trainNB0(array(trainMat),array(trainClass))
    errorCount=0
    for docIndex in testSet:
        wordVector=setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print('the error rate is : ',float(errorCount/len(testSet)))

def calMostFreq(vocalList,fulltext):
    import operator
    freqDict={}
    for token in vocalList:
        freqDict[token]=fulltext.count(token)
    sortedFreq=sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]

def localWords(feed1,feed0):
    import  feedparser
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'[i]['summary']])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList=createVocaList(docList)
    top30words=calMostFreq(vocabList,fullText)
    for pairW in top30words:
        if pairW[0] in vocabList:vocabList.remove(pairW[0])

    trainingSet=range(2*minLen);testSet=[]
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWordsVecMn(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    p0V,p1V,pSpam=trainNB0(array[trainMat],array[trainClasses])
    errorCount=0

    for docInex in testSet:
        wordVector=bagOfWordsVecMn(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docList]:
            errorCount+=1

        print('the error rate is :'+str(float(errorCount/len(testSet))))
        return vocabList,p0V,p1V