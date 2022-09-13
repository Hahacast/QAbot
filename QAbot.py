# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 02:02:44 2020

@author: user
"""


import jieba
import pickle
import json
import wikipedia
from zhconv import convert


wikipedia.set_lang("zh")

with open('2020wiki+m+eng.pickle', 'rb') as handle:
    wiki = pickle.load(handle)







with open('Question.json', 'rb') as handle:
    Question = json.load(handle)
answer = {}
may_error = []
answer_json = []
ans_score = {'A':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0},
             'B':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0}, 
             'C':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0} }  

wordInABC = {'A':0,'B':0,'C':0}   


 
for i in range (0,200):

    
    abc = {'A','B','C'}
    
    #遍歷選項，若選項不再wiki裡 則替換成wiki search的第一筆
    for x in abc : #
        
        if Question[i][x] not in wiki:
            a = wikipedia.search(Question[i][x], results=5, suggestion=False)
            for search in a:
                search_tw = convert(search, 'zh-hant') #再將a進行簡繁轉換
                if  search_tw == Question[i][x]:
                    break
                elif  search_tw in wiki:
#                    print(i," "+Question[i][x]+"->"+search_tw)   
                    Question[i][x] = search_tw
                 
                    ans_score[x]["wiki_down"] = ans_score[x]["wiki_down"] -1
                    break
    
#    print(Question[i]['A']+" "+Question[i]['B']+" "+Question[i]['C'])

    # words = 題目經jieba斷詞後的斷詞們(List)
    words = jieba.lcut(Question[i]['Question'], cut_all=False, HMM=True)
    if   str.isdigit(Question[i]['A']) and str.isdigit(Question[i]['B']) and str.isdigit(Question[i]['C']):
        may_error.append(i+1)
    # 遍歷每個斷詞
    for word in words:
        for j in abc :
           
           if Question[i][j] in wiki and  word in wiki[ Question[i][j] ] : #如果Question的選項有在wiki裡 且 word有在選項中的詞頻表
               ans_score[j]["Q_appear"] += 1
               wordInABC[j] = wiki[ Question[i][j] ] [word] #那就把ans_wordcount 等於 該選項的word出現數量
#               print(word , j , wordInABC[j])
         #得到三個選項的單字wordcount了，開始算wordcount分數，即'wordcount':0。最高的得2分，第二高的得1分，最後0分 
#        if wordInABC['A'] != 0 and wordInABC['B'] != 0 and wordInABC['C'] != 0:
#          print("wordcount: ",wordInABC['A'] , wordInABC['B'] ,wordInABC['C'])

        ABCcount_sort = sorted(wordInABC.items(), key=lambda x:x[1], reverse=True)

#        print(ABCcount_sort)

        #看起來很複雜，其實只是根據誰的wordcount高來加ans_score["wordcount"]而已
        if ABCcount_sort[0][1] != ABCcount_sort[1][1] != ABCcount_sort[2][1]:
            ans_score [ABCcount_sort[0][0]]['wordcount'] += 2
        elif ABCcount_sort[0][1] == ABCcount_sort[1][1] ==  ABCcount_sort[2][1]:
            ans_score [ABCcount_sort[0][0]]['wordcount'] += 0
        elif ABCcount_sort[0][1] == ABCcount_sort[1][1] and ABCcount_sort[1][1] != ABCcount_sort[2][1]:
            ans_score [ ABCcount_sort[0][0]]['wordcount']+= 2
            ans_score [ ABCcount_sort[1][0]]['wordcount']+= 2
            ans_score [ ABCcount_sort[2][0]]['wordcount']+= 1
        elif ABCcount_sort[0][1] != ABCcount_sort[1][1] and ABCcount_sort[1][1] == ABCcount_sort[2][1]:
            ans_score [ ABCcount_sort[0][0]]['wordcount']+= 2
            ans_score [ ABCcount_sort[1][0]]['wordcount']+= 1
            ans_score [ ABCcount_sort[2][0]]['wordcount']+= 1
        wordInABC = {'A':0,'B':0,'C':0}  
    
    #根據ans_score來找誰是答案
    
    winner = sorted(ans_score, key=lambda x:(ans_score[x]['Q_appear'] , ans_score[x]['wordcount'] , ans_score[x]['wiki_down'] ) ,reverse=True)
    #看要不要加入may_error
    if ans_score[winner[0]]['Q_appear'] != 0 and (len(words) <= 15 and ans_score[winner[1]]['Q_appear'] /ans_score[winner[0]]['Q_appear'] >= 0.85) and ( (i+1) not in may_error)  :
        may_error.append(i+1)
        
    if ans_score[winner[0]]['Q_appear'] <= 2 and  ( (i+1) not in may_error) :
        may_error.append(i+1)
        
#    print(ans_score)

    if (i+1) in may_error:
        print("**題號: ",i+1)
    else:
        print("題號: ",i+1  )
    answer[i+1] = winner[0]
    
    ans_score = {'A':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0},
                 'B':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0}, 
                 'C':{'Q_appear':0 , 'wordcount':0 , "wiki_down":0} }  


for i in range(0,200):
    answer_json.append(answer[i+1])
    
    
with open("answer1.json", "w") as outfile: 
    json.dump(answer_json, outfile)
    
with open('answer1.json', 'rb') as handle:
    answer = json.load(handle)
    
print(answer)
print("\n")
"""    
may_error1 = []
may_error2 = []
may_error3 = []
lence = len(may_error) /3 
lence = int(lence)
may_error1.append( may_error[:lence])
may_error2.append( may_error[lence: 2*lence])
may_error3.append( may_error[2*lence : ])


print("1  = " ,may_error1)
print("2  = " ,may_error2)
print("3  = " ,may_error3)"""





    
    