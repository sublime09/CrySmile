from gensim.models import LdaModel
import pyLDAvis.gensim
import numpy as np
import gensim
import warnings
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns


warnings.filterwarnings("ignore")

# pyLDAvis.enable_notebook()
d = gensim.corpora.Dictionary.load('dictionary.dict')
c = gensim.corpora.MmCorpus('corpus.mm')
lda = gensim.models.LdaModel.load('topic.model')
topicWordProbMat = lda.print_topics(3)
data = pyLDAvis.gensim.prepare(lda, c, d)
pyLDAvis.save_html(data,'vis.html')

print(topicWordProbMat)

columns = ['1','2','3']

df = pd.DataFrame(columns = columns)
pd.set_option('display.width', 1000)

# 40 will be resized later to match number of words in DC
zz = np.zeros(shape=(30,3))

last_number=0
DC={}

for x in range (10):
  data = pd.DataFrame({columns[0]:"",
                     columns[1]:"",
                     columns[2]:"",                                                
                    },index=[0])
  df=df.append(data,ignore_index=True)  
    
for line in topicWordProbMat:
    
    tp, w = line
    probs=w.split("+")
    y=0
    for pr in probs:
               
        a=pr.split("*")
        df.iloc[y,tp] = a[1]
       
        if a[1] in DC:
        	print(a[1])
        	zz[DC[a[1]]][tp]=a[0]
        else:
           zz[last_number][tp]=a[0]
           DC[a[1]]=last_number
           last_number=last_number+1
        y=y+1

print(df)
print(zz)
print(DC)

zz=np.resize(zz,(len(DC.keys()),zz.shape[1]))

print(zz)

# plt.imshow(zz, cmap='hot', interpolation='nearest')
# plt.colorbar()
# plt.show()
y_labels = DC.keys()
df = pd.DataFrame(zz, columns=["topic1","topic2","topic3"])
g = sns.heatmap(df, annot=True, annot_kws={"size": 7}, xticklabels='auto', yticklabels=y_labels)
g.set_yticklabels(y_labels, rotation=45)
plt.show()



# lda = gensim.models.LdaModel.load('topic.model')
# fiz=plt.figure(figsize=(15,30))
# for i in range(3):
#     df=pd.DataFrame(lda.show_topic(i), columns=['term','prob']).set_index('term')
# #     df=df.sort_values('prob')
    
#     plt.subplot(1,3,i+1)
#     plt.title('topic '+str(i+1))
#     sns.barplot(x='prob', y=df.index, data=df, label='Cities', palette='Reds_d')
#     plt.xlabel('probability')
    

# plt.show()