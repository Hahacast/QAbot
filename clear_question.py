import ijson  # or choose a faster backend if needed
from itertools import islice

#
with open("Question.json",encoding='utf-8') as f:
    objects = ijson.items(f, 'item')
    o = list(islice(objects,0,200))


將quesion轉換成clear_quesion
with open("Clear_question.json",'a',encoding='utf-8') as f:
    for i in o:
        f.write(str(i)+'\n')  
