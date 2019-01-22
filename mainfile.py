from bayes import *
import feedparser

# # 测试
# listOPosts,listClases=loadDataSet()#加载数据
# myVocabList=createVocaList(listOPosts)#得到了一个不包含重复词的列表
# print(myVocabList)
# testingNB()
# #交叉验证测试
# spamTest()

#RSS源测试
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
vocabList,pSF,pNY=localWords(ny,sf)
