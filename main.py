import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PredictData(BaseModel):
    mot: str

###############################
###### ECNODAGE DE X ##########
###############################
mots = ["robe", "fourchette", "assiette", "chemise", "cuillere", "veste", "tasse", "robe"]
# creer vocabulaire unique
vocabulaire = np.unique(mots)
# print(vocabulaire)
# conversion de mot en nombre par emplacement de chaque mot
word_to_index = {str(word): nbr for nbr, word in enumerate(vocabulaire)}
# print(word_to_index)
# conversion de nombre en vecteur
def one_hot(word):
    vector = np.zeros(len(vocabulaire))
    vector[word_to_index[word]] = 1
    return vector
X = np.array([one_hot(w) for w in mots])
print("X: ", X)
###############################
###### ECNODAGE DE Y ##########
###############################
classements=["vetement", "cuisine", "cuisine", "vetement", "cuisine", "vetement", "cuisine", "vetement"]
Y = np.array([1 if cl == 'cuisine' else -1 for cl in classements])
print("Y: ", Y)
###############################
### INITIALISATION SVM ########
###############################
b = 0 # biais (responsable du deplacement de la droite)
lr = 0.1 # learning rate (taux d'apprentissage)
epochs = 50
a = np.zeros(len(vocabulaire)) + 1
###############################
####### ENTRAINEMENT ##########
###############################
for _ in range(epochs):
    for i in range(len(X)):
        x_i = X[i]
        y_i = Y[i]
        condition = y_i * np.dot(a, x_i) + b
        if condition  >= 1:
            a = a - lr * ( 2 * a)
        else:
            a = a - lr * ( 2 * a  - y_i * x_i)
            b = b - lr * (-y_i)
###############################
######## PREDICTION ###########
###############################
@app.post('/predict')
async def predict(preD: PredictData):
    X = one_hot(preD.mot)
    result = np.dot(a, X) + b
    return "cuisine" if result >= 1  else "vetement"
mot = "robe"
print("Input: ", mot, "Predicted category", predict(mot))
