import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
# ------------- LOAD DATA -------------
url = './week-5/in-lab/2020_bn_nb_data.txt'

data = pd.read_csv(url,sep='\t')

# ------------- PREPROCESS DATA -------------
'''Converting grades to numbers'''
ordinal_enc = OrdinalEncoder(categories=[['AA','AB','BB','BC','CC','CD','DD','F']]*(data.shape[1]-1))
data.iloc[:,:-1] = ordinal_enc.fit_transform(data.iloc[:,:-1])

# ------------- SPLIT DATA -------------
X = data.iloc[:,:-1]
Y = data.iloc[:,-1]

x_train, x_test, y_train,y_test = train_test_split(X,Y, test_size = 0.25,random_state=30)

# ------------- TRAIN MODEL -------------

GNBclassifier = GaussianNB()
GNBclassifier.fit(x_train,y_train)


# ------------- ACCURACY TESTING -------------
y_test_pred = GNBclassifier.predict(x_test)
print(f"Accuracy of the model: {accuracy_score(y_test,y_test_pred)*100}%")

# ------------- PREDICT USING MODEL -------------



