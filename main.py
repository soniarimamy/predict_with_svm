import numpy as np
import matplotlib.pyplot as plt
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

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
loss_history = []
accuracy_history = []

for _ in range(epochs):
    total_loss = 0
    correct = 0
    for i in range(len(X)):
        x_i = X[i]
        y_i = Y[i]
        condition = y_i * np.dot(a, x_i) + b
        if condition  >= 1:
            loss = 0
            a = a - lr * ( 2 * a)
        else:
            loss = 1 - condition
            a = a - lr * ( 2 * a  - y_i * x_i)
            b = b - lr * (-y_i)
        total_loss = total_loss + loss
        prediction = 1 if (np.dot(a, x_i) + b) >= 0 else -1
        if prediction == y_i:
            correct = correct + 1
    loss_history.append(total_loss)
    accuracy_history.append(correct / len(X))
###############################
######## PREDICTION ###########
###############################
@app.post('/predict')
async def predict(preD: PredictData):
    X = one_hot(preD.mot)
    result = np.dot(a, X) + b
    return "cuisine" if result >= 1  else "vetement"

@app.get('/show_perf_as_number')
async def show_perf_as_number():
    final_accuracy = accuracy_history[-1]
    error_rate = 1 - final_accuracy
    final_loss = loss_history[-1]
    return {
        "accuracy": float(final_accuracy),
        "error_rate": float(error_rate),
        "loss": float(final_loss)
    }

@app.get('/show_perf_as_graph')
async def show_perf_as_graph():
    plt.figure()
    plt.plot(loss_history, label="Loss")
    plt.plot(accuracy_history, label="Accuracy")
    plt.plot([1 - acc for acc in accuracy_history], label = "Error")
    plt.xlabel("Epochs")
    plt.ylabel("Value")
    plt.title("Performance SVM Model")
    plt.legend()
    file_path = "svm_perf.png"
    plt.savefig(file_path)
    plt.close()
    return FileResponse(file_path, media_type="image/png")
