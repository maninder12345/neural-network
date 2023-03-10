# -*- coding: utf-8 -*-
"""pythoncode.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TTbWjOcyfuYo2jIt4e2IKJGQWeKTUr43

## I. Importing essential libraries
"""

# Commented out IPython magic to ensure Python compatibility.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline

import os
print(os.listdir())

import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

"""## II. Importing and understanding our dataset """

dataset = pd.read_csv("heart.csv")

"""#### Verifying it as a 'dataframe' object in pandas"""

type(dataset)

"""#### Shape of dataset"""

dataset.shape

"""#### Printing out a few columns"""

dataset.head(5)

dataset.sample(5)

"""#### Description"""

dataset.describe()

dataset.info()

###Luckily, we have no missing values

"""#### Let's understand our columns better:"""

info = ["age","1: male, 0: female","chest pain type, 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic","resting blood pressure"," serum cholestoral in mg/dl","fasting blood sugar > 120 mg/dl","resting electrocardiographic results (values 0,1,2)"," maximum heart rate achieved","exercise induced angina","oldpeak = ST depression induced by exercise relative to rest","the slope of the peak exercise ST segment","number of major vessels (0-3) colored by flourosopy","thal: 3 = normal; 6 = fixed defect; 7 = reversable defect"]



for i in range(len(info)):
    print(dataset.columns[i]+":\t\t\t"+info[i])

"""#### Analysing the 'target' variable"""

dataset["target"].describe()

dataset["target"].unique()

"""#### Clearly, this is a classification problem, with the target variable having values '0' and '1'

### Checking correlation between columns
"""

print(dataset.corr()["target"].abs().sort_values(ascending=False))

#This shows that most columns are moderately correlated with target, but 'fbs' is very weakly correlated.

"""## Exploratory Data Analysis (EDA)

### First, analysing the target variable:
"""

y = dataset["target"]

sns.countplot(y)


target_temp = dataset.target.value_counts()

print(target_temp)

print("Percentage of patience without heart problems: "+str(round(target_temp[0]*100/303,2)))
print("Percentage of patience with heart problems: "+str(round(target_temp[1]*100/303,2)))

#Alternatively,
# print("Percentage of patience with heart problems: "+str(y.where(y==1).count()*100/303))
# print("Percentage of patience with heart problems: "+str(y.where(y==0).count()*100/303))

# #Or,
# countNoDisease = len(df[df.target == 0])
# countHaveDisease = len(df[df.target == 1])

"""### We'll analyse 'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca' and 'thal' features

### Analysing the 'Sex' feature
"""

dataset["sex"].unique()

"""##### We notice, that as expected, the 'sex' feature has 2 unique features"""

sns.barplot(dataset["sex"],y)

"""##### We notice, that females are more likely to have heart problems than males

### Analysing the 'Chest Pain Type' feature
"""

dataset["cp"].unique()

"""##### As expected, the CP feature has values from 0 to 3"""

sns.barplot(dataset["cp"],y)

"""##### We notice, that chest pain of '0', i.e. the ones with typical angina are much less likely to have heart problems

### Analysing the FBS feature
"""

dataset["fbs"].describe()

dataset["fbs"].unique()

sns.barplot(dataset["fbs"],y)

"""##### Nothing extraordinary here

### Analysing the restecg feature
"""

dataset["restecg"].unique()

sns.barplot(dataset["restecg"],y)

"""##### We realize that people with restecg '1' and '0' are much more likely to have a heart disease than with restecg '2'

### Analysing the 'exang' feature
"""

dataset["exang"].unique()

sns.barplot(dataset["exang"],y)

"""##### People with exang=1 i.e. Exercise induced angina are much less likely to have heart problems

### Analysing the Slope feature
"""

dataset["slope"].unique()

sns.barplot(dataset["slope"],y)

"""##### We observe, that Slope '2' causes heart pain much more than Slope '0' and '1'

### Analysing the 'ca' feature
"""

#number of major vessels (0-3) colored by flourosopy

dataset["ca"].unique()

sns.countplot(dataset["ca"])

sns.barplot(dataset["ca"],y)

"""##### ca=4 has astonishingly large number of heart patients"""

### Analysing the 'thal' feature

dataset["thal"].unique()

sns.barplot(dataset["thal"],y)

sns.distplot(dataset["thal"])

"""## IV. Train Test split"""

# Import libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = dataset

# Preprocess data
X = df.drop('target', axis=1)
y = df['target']
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(13,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=100, batch_size=16, validation_data=(X_test, y_test))

# Evaluate model
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test accuracy:', test_acc)