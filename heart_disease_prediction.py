# -*- coding: utf-8 -*-
"""Heart Disease Prediction

Automatically generated by Colaboratory.

Original file is located at
   https://colab.research.google.com/drive/1lEm7A-XYOZCWHuXKEs0AaIHz5aX3Q2nT?authuser=1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn import linear_model, tree, ensemble
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"





df = pd.read_csv("./heart.csv")
print(df)

df.info()
print(df)

df.isna().sum()

df1=df.head(10)
print(df1)

#EDA
x=df["target"]
target_1 = df.target.value_counts()
print(target_1)
plt.figure(figsize=(8, 6))
target_1.plot(kind='bar', color=['skyblue', 'orange'])
plt.title('Target Variable Counts')
plt.xlabel('Target Classes')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

percentage_without_heart_problems = (target_1[0] / len(df)) * 100
percentage_with_heart_problems = (target_1[1] / len(df)) * 100

print(f"Percentage of patients without heart problems: {percentage_without_heart_problems:.2f}%")
print(f"Percentage of patients with heart problems: {percentage_with_heart_problems:.2f}%")

df["sex"].unique()

import seaborn as sns
sns.barplot(x=df["sex"], y=df["target"])

pd.crosstab(df.age,df.target).plot(kind="bar",figsize=(20,6))
plt.title('Heart Disease Frequency for Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.savefig('heartDiseaseAndAges.png')
plt.show()

pd.crosstab(df.sex,df.target).plot(kind="bar",figsize=(20,10),color=['blue','#AA1111' ])
plt.title('Heart Disease Frequency for Sex')
plt.xlabel('Sex (0 = Female, 1 = Male)')
plt.xticks(rotation=0)
plt.legend(["Don't have Disease", "Have Disease"])
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(15,10))
sns.heatmap(df.corr(),linewidth=.01,annot=True,cmap="winter")
plt.show()
plt.savefig('correlationfigure')

df["cp"].unique()

plt.figure(figsize=(26, 10))
sns.barplot(x=df["cp"],y=x)

pd.crosstab(df.fbs,df.target).plot(kind="bar",figsize=(20,10),color=['#4286f4','#f49242'])
plt.title("Heart disease according to FBS")
plt.xlabel('FBS- (Fasting Blood Sugar > 120 mg/dl) (1 = true; 0 = false)')
plt.xticks(rotation=90)
plt.legend(["Don't Have Disease", "Have Disease"])
plt.ylabel('Disease or not')
plt.show()

df["thal"].unique()

sns.distplot(df["thal"])

sns.barplot(x=df["thal"],y=x)

from sklearn.model_selection import train_test_split
X = df.drop("target",axis=1)
y = df["target"]
X_train, X_test,y_train, y_test=train_test_split(X,y,test_size=0.25,random_state=40)

#Logistic Regression
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
lr=LogisticRegression(C=1.0, class_weight='balanced', dual=False,
                   fit_intercept=True, intercept_scaling=1, l1_ratio=None,
                   max_iter=100, multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=1234, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)
model1=lr.fit(X_train,y_train)
prediction1=model1.predict(X_test)
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,prediction1)
cm
sns.heatmap(cm, annot=True,cmap='winter',linewidths=0.3, linecolor='black',annot_kws={"size": 20})
TP=cm[0][0]
TN=cm[1][1]
FN=cm[1][0]
FP=cm[0][1]

print('Testing Accuracy for Logistic Regression:',(TP+TN)/(TP+TN+FN+FP))
print('Testing Sensitivity for Logistic Regression:',(TP/(TP+FN)))
print('Testing Specificity for Logistic Regression:',(TN/(TN+FP)))
print('Testing Precision for Logistic Regression:',(TP/(TP+FP)))

from sklearn.metrics import classification_report
print(classification_report(y_test, prediction1))

#Decision Trees
from sklearn.model_selection import train_test_split
X1 = df[["age", "cp", "trestbps", "chol", "thalach", "oldpeak", "ca"]]
y1 = df["target"]
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.25, random_state=40)
from sklearn.model_selection import RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier

tree_model = DecisionTreeClassifier(max_depth=5,criterion='entropy')
cv_scores = cross_val_score(tree_model, X, y, cv=10, scoring='accuracy')
m=tree_model.fit(X1, y1)
prediction=m.predict(X_test)
cm= confusion_matrix(y_test,prediction)
sns.heatmap(cm, annot=True,cmap='winter',linewidths=0.3, linecolor='black',annot_kws={"size": 20})
print(classification_report(y_test, prediction))

TP=cm[0][0]
TN=cm[1][1]
FN=cm[1][0]
FP=cm[0][1]
print('Testing Accuracy for Decision Tree:',(TP+TN)/(TP+TN+FN+FP))
print('Testing Sensitivity for Decision Tree:',(TP/(TP+FN)))
print('Testing Specificity for Decision Tree:',(TN/(TN+FP)))
print('Testing Precision for Decision Tree:',(TP/(TP+FP)))

#Support Vector Machine
from sklearn.svm import SVC
svm=SVC(C=12,kernel='linear')
model4=svm.fit(X_train,y_train)
prediction4=model4.predict(X_test)
cm4= confusion_matrix(y_test,prediction4)
sns.heatmap(cm4, annot=True,cmap='winter',linewidths=0.3, linecolor='black',annot_kws={"size": 20})
TP=cm4[0][0]
TN=cm4[1][1]
FN=cm4[1][0]
FP=cm4[0][1]
print('Testing Accuracy for SVM:',(TP+TN)/(TP+TN+FN+FP))
print('Testing Sensitivity for Random Forest:',(TP/(TP+FN)))
print('Testing Specificity for Random Forest:',(TN/(TN+FP)))
print('Testing Precision for Random Forest:',(TP/(TP+FP)))

#Testing our best model
input=(63,3,145,233,150,2.3,0)
input_as_numpy=np.asarray(input)
input_reshaped=input_as_numpy.reshape(1,-1)
pre1=tree_model.predict(input_reshaped)
if(pre1==1):
  print("The patient seems to be have heart disease")
else:
  print("The patient seems to be Normal")

input=(72,1,125,200,150,1.3,1)
input_as_numpy=np.asarray(input)
input_reshaped=input_as_numpy.reshape(1,-1)
pre1=tree_model.predict(input_reshaped)
if(pre1==1):
  print("The patient seems to be have heart disease")
else:
  print("The patient seems to be Normal")

input=(54,3,160,330,180,3.3,0)
input_as_numpy=np.asarray(input)
input_reshaped=input_as_numpy.reshape(1,-1)
pre1=tree_model.predict(input_reshaped)
if(pre1==1):
  print("The patient seems to be have heart disease")
else:
  print("The patient seems to be Normal")

