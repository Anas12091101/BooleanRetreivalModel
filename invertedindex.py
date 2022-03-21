#Code written by : 19k-1534 Muhammad Anas
#Approach: Created a positional index which also works as an inverted index for simple and complex 
# queries. The queries are then classified accordingly in the process query fn and are processed 
# according to their needs.

from preprocessing import terms
from operator import itemgetter
from nltk.stem.porter import PorterStemmer
import tkinter as tk
from tkinter import *
sorted_terms=sorted(terms,key=itemgetter(0))

stemmer=PorterStemmer()

#used Mylist class as it helped me in debugging and writing code efficiently.
class Mylist:
    def __init__(self):
        self.value=''
        self.list=[]

postinglist=[]   

#As name suggest, this fn creates the positional index.(inverted index also same without the positions)
def createIndex():
    lastlist=[]
    dictionary=Mylist()
    dictionary.value=sorted_terms[0][0]
    doclist=Mylist()
    doclist.value=sorted_terms[0][1]
    doclist.list.append(sorted_terms[0][2])

    prevterm=sorted_terms[0][0]
    idx=0
    # print(len(sorted_terms))
    for term in sorted_terms:
        if idx > 0:
            if idx == len(sorted_terms)-1:
                dictionary.list.append({doclist.value:doclist.list})
                lastlist=dictionary.list
            if term[0]!=prevterm:
                dictionary.list.append({doclist.value:doclist.list})
                postinglist.append(dictionary.list)    
                dictionary=Mylist()
                dictionary.value=term[0]
                a=False
                doclist=Mylist()
                doclist.value=term[1]
                doclist.list.append(term[2])
            else:
                  if doclist.value != term[1]:
                    dictionary.list.append({doclist.value:doclist.list}) 
                    doclist=Mylist()
                    doclist.value=term[1]
                    doclist.list.append(term[2])
                  else:
                    doclist.list.append(term[2])
        prevterm=term[0]
        idx=idx+1
    postinglist.append(lastlist)

def getAllTerms():
    for t in sorted_terms:
        if t[0] not in all_terms:
            all_terms.append(t[0])

def simplequery(query_tokens):
    result_docs=[]
    #processing 1 word query
    if len(query_tokens)==1:
        query_tokens[0]=stemmer.stem(query_tokens[0])
        idx=0
        for term in all_terms:
            if term==query_tokens[0]:
                for doc in postinglist[idx]:
                    for key,items in doc.items():
                        if key not in result_docs:
                            result_docs.append(key)
            idx=idx+1
    #processing not only query
    elif len(query_tokens)==2 and query_tokens[0]=="not":
        query_tokens[1]=stemmer.stem(query_tokens[1])
        idx=0
        for term in all_terms:
            if term!=query_tokens[1]:
                for doc in postinglist[idx]:
                    for key,items in doc.items():
                        if key not in result_docs:
                            result_docs.append(key)

            idx=idx+1
    #processing and/or queries        
    elif len(query_tokens)==3:
        conj_list1=[]
        conj_list2=[]
        query_tokens[0]=stemmer.stem(query_tokens[0])
        print(query_tokens[0])
        query_tokens[2]=stemmer.stem(query_tokens[2])
        print(query_tokens[2])
        idx=0
        for term in all_terms:
            if term == query_tokens[0]:
                for doc in postinglist[idx]:
                    for key,items in doc.items():
                        conj_list1.append(key)
            
            elif term == query_tokens[2]:
                for doc in postinglist[idx]:
                    for key,items in doc.items():
                        conj_list2.append(key)
            idx=idx+1
        if query_tokens[1]=="and":
            result_docs=[value for value in conj_list1 if value in conj_list2]
        elif query_tokens[1]=="or":
            result_docs=list(set(conj_list1)|set(conj_list2))
    print(result_docs)    
    return result_docs

#for 3 terms queries
def complexquery(query_tokens):
    result_docs=[]
    term1=stemmer.stem(query_tokens[0])
    term2=stemmer.stem(query_tokens[2])
    term3=stemmer.stem(query_tokens[4])
    operator1=query_tokens[1]
    operator2=query_tokens[3]
    term_list1=[]
    term_list2=[]
    term_list3=[]
    result_doc1=[]
    idx=0
    for term in all_terms:
        if term == term1:
            for doc in postinglist[idx]:
                for key,items in doc.items():
                    term_list1.append(key)
            
        elif term == term2:
            for doc in postinglist[idx]:
                for key,items in doc.items():
                    term_list2.append(key)
            
        elif term == term3:
            for doc in postinglist[idx]:
                for key,items in doc.items():
                    term_list3.append(key)
        idx=idx+1

    if operator1=="and":
        result_doc1=[value for value in term_list1 if value in term_list2]
    elif operator1=="or":
        result_doc1=list(set(term_list1)|set(term_list2))
    if operator2=="and":
        print(result_doc1)
        result_docs=[value for value in result_doc1 if value in term_list3]
    elif operator2=="or":
        result_docs=list(set(result_doc1)|set(term_list3))
    return result_docs

#for proximity queries
def proximityquery(query_tokens,gap):
    term1=stemmer.stem(query_tokens[0])
    term2=stemmer.stem(query_tokens[1])
    term_list1=[]
    term_list2=[]
    idx=0
    for term in all_terms:
        if term == term1:
            for doc in postinglist[idx]:
                term_list1.append(doc)
        if term == term2:
            for doc in postinglist[idx]:
                term_list2.append(doc)
        idx=idx+1
    term1_doc=[]
    term2_doc=[]
    same_docs=[]
    for doc in term_list1:
        for key,item in doc.items():
            term1_doc.append(key)
    for doc in term_list2:
        for key,item in doc.items():
            term2_doc.append(key)
    
    same_docs=[value for value in term1_doc if value in term2_doc]
    term1_pi=[]
    term2_pi=[]
    for doc in term_list1:
        for key,item in doc.items():
            if key in same_docs:
                term1_pi.append(item)
    for doc in term_list2:
        for key,item in doc.items():
            if key in same_docs:
                term2_pi.append(item)
    result_doc=[]
    idx=0
    for term1 in term1_pi:
        for t1 in term1:
            for t2 in term2_pi[idx]:
                if(abs(int(t1)-int(t2))<=gap+1):
                    if same_docs[idx] not in result_doc:
                        result_doc.append(same_docs[idx])
            
        idx=idx+1

    return result_doc

#main process query fn from where queries are redirected to their relevant fn.
def processquery(query):
    query_tokens=query.split(" ")
    if "/" in query:
        gap=query_tokens[-1]
        gap=gap.replace("/","")
        gap=int(gap)
        doc_list=proximityquery(query_tokens,gap)
    elif len(query_tokens)<=3:
        doc_list=simplequery(query_tokens)
    elif len(query_tokens)==5:
        doc_list=complexquery(query_tokens)

    return doc_list



def inputqueryGUI():
    #a method to get input queries from user and passing to the main process query fn.
    def execute():
        label2["text"]=""
        query=str(entry.get())
        query=query.lower()
        doc_list=processquery(query)
        if doc_list:
            label2["fg"]="purple"
            i=0
            
            #for loop for mantaining the no of docs in one output line.
            for doc in doc_list:
                if i==20:
                    label2["text"]+="\n"+str(doc)+" "
                    i=0
                else:
                    label2["text"]+=str(doc)+" "
                i=i+1
        else:
            label2["fg"]="red"
            label2["text"]="Sorry didn't find the document. Please enter correct query"
        doc_list.clear()

    #GUI design line[242-266]
    Font_tuple = ("Comic Sans MS", 20, "bold")
    window=tk.Tk()
    window.title("Boolean Retreival Model( By 19k-1534)")
    window.geometry("1000x800")
    window.rowconfigure(0, minsize=500, weight=1)
    window.columnconfigure([0, 1, 2], minsize=500, weight=1)
    frame1=tk.Frame(master=window,width=200,height=70,bg="#4a0f61")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    label1=tk.Label(master=frame1,font=Font_tuple,text="Welcome!",bg="#4a0f61",fg="white")
    label1.pack()
    frame=tk.Frame(master=window,width=100,height=70,bg="white")
    frame.place(relx=.5, rely=.5,anchor= CENTER)
    frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    label1=tk.Label(master=frame,text="Boolean Retreival Model",bg="white",fg="purple",font=Font_tuple)
    label = tk.Label(master=frame,text="Enter your query",bg="white",fg="purple")
    entry=tk.Entry(master=frame,width=40)
    btn=tk.Button(master=frame,bg="purple",fg="white",text="Enter",command=execute)
    label1.pack()
    label.pack()
    entry.pack()
    btn.pack()
    label2 = Label(frame,font=('"Comic Sans MS" 8 bold'),width=200,bg="white",fg="purple",text="waiting for your query :)")
    label2.pack(pady=20)
    window.mainloop() 



createIndex() #creates the positional index.
all_terms=[] #list to store terms.
getAllTerms() #a method to populate all terms.
inputqueryGUI() # a tkinter GUI method for taking input queries & processing them.
