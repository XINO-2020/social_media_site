import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from mlxtend.classifier import StackingClassifier
from sklearn.model_selection import train_test_split
import warnings
import pickle
from sklearn.tree import DecisionTreeClassifier
warnings.filterwarnings("ignore")

data = pd.read_csv("mental_health.csv")
male_str = ["male", "m", "male-ish", "maile", "mal", "male (cis)", "make", "male ", "man","msle", "mail", "malr","cis man", "Cis Male", "cis male"]
trans_str = ["trans-female", "something kinda male?", "queer/she/they", "non-binary","nah", "all", "enby", "fluid", "genderqueer", "androgyne", "agender", "male leaning androgynous", "guy (-ish) ^_^", "trans woman", "neuter", "female (trans)", "queer", "ostensibly male, unsure what that really means"]
female_str = ["cis female", "f", "female", "woman",  "femake", "female ","cis-female/femme", "female (cis)", "femail"]


for (row, col) in data.iterrows():

    if str.lower(col.Gender) in male_str:
        data['Gender'].replace(to_replace=col.Gender, value='male', inplace=True)

    if str.lower(col.Gender) in female_str:
        data['Gender'].replace(to_replace=col.Gender, value='female', inplace=True)

    if str.lower(col.Gender) in trans_str:
        data['Gender'].replace(to_replace=col.Gender, value='trans', inplace=True)

#Get rid of bullshit
stk_list = ['A little about you', 'p']
data = data[~data['Gender'].isin(stk_list)]
data['Gender']=data['Gender'].map({'male':0,'female':1, 'trans':2})
data['family_history']=data['family_history'].map({'No':0,'Yes':1})
data['self_employed']=data['self_employed'].map({'No':0,'Yes':1})
data['remote_work']=data['remote_work'].map({'No':0,'Yes':1})
data['tech_company']=data['remote_work'].map({'No':0,'Yes':1})
data['coworkers']=data['coworkers'].map({'No':0,'Yes':1,'Some of them':2})
data['wellness_program']=data['wellness_program'].map({'No':0,'Yes':1,"Don't know":2})
data['treatment']=data['treatment'].map({'No':0,'Yes':1})
data = np.array(data)

X = data[:,:-1]
y = data[:, -1]
y = y.astype('int')
X = X.astype('int64')
clf1 = KNeighborsClassifier(n_neighbors=5)
clf2 = RandomForestClassifier(random_state=5)
clf3 = GaussianNB()
clf4 = DecisionTreeClassifier(max_depth=3, min_samples_split=8, max_features=6, criterion='entropy', min_samples_leaf=7)
lr = LogisticRegression()
stack = StackingClassifier(classifiers=[clf1, clf2, clf3, clf4], meta_classifier=lr)
stack.fit(X, y)
pickle.dump(stack,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))
