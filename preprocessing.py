#What this file do? 
#This file reads the docs , tokenize them into tokens
#  , stem the tokens , lowercase those tokens , sort them and 
#  store them in terms.txt file.

from operator import itemgetter
from nltk.stem.porter import PorterStemmer
from markupsafe import re


stopwords=[]

#assign stopwords list from Stopword-List.txt
def initialize_stopwords():  
    f=open("Stopword-List.txt","r")
    for line in f:
        for word in line.split():
            stopwords.append(word)
    f.close()


#read the documents one by one and tokenize them into tokens
def tokenize():
    count=0
    tokens=[]
    docId=[]
    pos=[]
    for i in range(448):
        j=i+1
        f=open("Abstracts/"+str(j)+".txt","r",encoding="latin1")
        k=0
        for line in f:
           for word in re.findall(r"[\w']+",line):            
            word=word.replace("'","")
                
            #In the if block we check if the word is in the stopword list
            if(word not in stopwords):
                tokens.append(word)
                pos.append(k)
                docId.append(j)
                k=k+1
            count=count+1
        f.close()   
    return {"tokens":tokens,"docId":docId,"pos":pos}

def linguistics(tokens):
    stemmer=PorterStemmer()  #does the stemming as well as lowercasing.
    terms=[] #tokens after stemming and normalization
    index=0
    for token in tokens["tokens"]:
        terms.append([stemmer.stem(token),tokens["docId"][index],tokens["pos"][index]])
        index=index+1
    return terms



initialize_stopwords()
tokens=tokenize()
terms=linguistics(tokens)
sorted_terms=sorted(terms,key=itemgetter(0))
sf=open("terms.txt","w")   
sf.write(str(sorted_terms)) 
