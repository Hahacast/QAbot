# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:05:05 2020

@author: user
"""

import pickle
import ijson  # or choose a faster backend if needed
import winsound
import jieba
from itertools import islice
    

standard = ["an","d","f","m","mg*","n","ng","nr","nrfg*","nrt*","ns","nt","nz","s","tg","vn","eng" ]

wiki = {}
blank=0
j = 0
count = 0

#  example = {"title1":"[{},{}]"    }


with open("2020WIKI.json",encoding='utf-8') as f:
    objects = ijson.items(f, 'item')

#    for i in o[0]['tokens']:
        
#        print(i)
    

    for idd in range( 0,1126680):
        if idd %10000 == 0:
            print(idd)
        o = list(islice(objects,0,1))    
        data_title = o[0]['title']
        wiki[data_title] = {}
#        print(idd,data_title ,o[0]['id']  )
        for sentence in o[0]['tokens']:  #sentence = [['稱為', 'v'], ['千禧年大獎難題', 'n']]
            for word in sentence: #['稱為', 'v']
                if word[1] in standard: #有在詞性標準
                    words = jieba.lcut( word[0], cut_all=False, HMM=True) #words =[ 千禧年,, 大獎 , 難題 ]
                    for cut_word in words:
                        if len(cut_word)>1:
                            if  cut_word not in wiki[data_title]:
                                wiki[data_title][cut_word] = 1
                            else:
                                wiki[data_title][cut_word] += 1

            
            
with open('2020wiki+m+eng.pickle', 'wb') as f:
    pickle.dump(wiki, f, protocol=pickle.HIGHEST_PROTOCOL)
    
winsound.Beep(600,1000)