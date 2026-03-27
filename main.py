import asyncio
import numpy as np
import matplotlib.pyplot as plt
from fastapi import FastAPI
from pydantic import BaseModel
import matplotlib.pyplot as plt
from temporalio.client import Client
from workflow import PredictWorkflow
from fastapi.responses import FileResponse

app = FastAPI()

class PredictData(BaseModel):
    mot: str

###############################
###### ENCODAGE DE X ##########
###############################
mots = ["robe", "fourchette", "assiette", "chemise", "cuillere", "veste", "tasse", "robe"]

vocabulaire = np.unique(mots)
word_to_index = {str(word): nbr for nbr, word in enumerate(vocabulaire)}

def one_hot(word):
    vector = np.zeros(len(vocabulaire))
    vector[word_to_index[word]] = 1
    return vector

X = np.array([one_hot(w) for w in mots])

###############################
###### ENCODAGE DE Y ##########
###############################
classements = ["vetement", "cuisine", "cuisine", "vetement", "cuisine", "vetement", "cuisine", "vetement"]
Y = np.array([1 if cl == 'cuisine' else -1 for cl in classements])

###############################
### INITIALISATION SVM ########
###############################
b = 0
lr = 0.1
epochs = 50
a = np.zeros(len(vocabulaire)) + 1

###############################
### STOCKAGE PERFORMANCE ######
###############################
loss_history = []
accuracy_history = []

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
        condition = y_i * (np.dot(a, x_i) + b)
        if condition >= 1:
            loss = 0
            a = a - lr * (2 * a)
        else:
            loss = 1 - condition
            a = a - lr * (2 * a - y_i * x_i)
            b = b - lr * (-y_i)
        total_loss += loss
        # calcul accuracy
        prediction = 1 if (np.dot(a, x_i) + b) >= 0 else -1
        if prediction == y_i:
            correct += 1
    loss_history.append(total_loss)
    accuracy_history.append(correct / len(X))

###############################
######## PREDICTION ###########
###############################
@app.post('/predict')
async def predict(preD: PredictData):
    X_input = one_hot(preD.mot)
    result = np.dot(a, X_input) + b
    return {"prediction": "cuisine" if result >= 0 else "vetement"}

###############################
### PERFORMANCE NUMERIQUE #####
###############################
@app.get("/show_perf_as_number")
async def show_perf_as_number():
    final_accuracy = accuracy_history[-1]
    error_rate = 1 - final_accuracy
    final_loss = loss_history[-1]
    return {
        "accuracy": float(final_accuracy),
        "error_rate": float(error_rate),
        "loss": float(final_loss)
    }

###############################
### PERFORMANCE GRAPH #########
###############################
@app.get("/show_perf_as_graph")
async def show_perf_as_graph():
    plt.figure()
    plt.plot(loss_history, label="Loss")
    plt.plot(accuracy_history, label="Accuracy")
    plt.plot([1 - acc for acc in accuracy_history], label="Error")
    plt.xlabel("Epochs")
    plt.ylabel("Value")
    plt.title("Performance SVM")
    plt.legend()
    file_path = "performance.png"
    plt.savefig(file_path)
    plt.close()
    return FileResponse(file_path, media_type="image/png")

@app.post("/orchestrate")
async def orchestrate(preD: PredictData):
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        PredictWorkflow.run,
        preD.mot,
        id="workflow-id-" + preD.mot,
        task_queue="ml-task-queue",
    )
    return result
