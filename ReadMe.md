# I. API
## I.1. Dependences et environnement virtuel
- python -m venv venv
- .\venv\Scripts\activate
- pip install numpy
- pip install fastapi
- pip install matplolib
- pip install uvicorn
## I.2. Lancement du REST API (SANS ORCHESTRATION)
- uvicorn main:app

## I.3. Affichage du resultat de chaque web service
- ### Affichez la score de performance du modele SVM
```
curl -X GET "http://127.0.0.1:8000/show_perf_as_number" -H "accept: application/json"
```

- ### Faire une prediction
```
curl -X POST "http://127.0.0.1:8000/predict" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"mot\": \"veste\"}"
```

- ### Afficher la performance du modele SVM (sous forme de graph)
```
curl -X GET "http://127.0.0.1:8000/show_perf_as_graph" -H "accept: application/json" -o graph_svm.png
```

# II. TEMPORAL (API ORCHESTRATION)
## II.1. Installation
- Lien: https://temporal.io/setup/install-temporal-cli

## II.2. Lancement
- [CMD](CMD): temporal server start-dev
- [Server](Server): http://localhost:7233
- [WebUI](WebUI): http://localhost:8233

## II.3. Install temporalio Library
- pip install temporalio

## II.4. Lancement avec orchestration
#### a. [CMD1](CMD1): 
```
temporal server start-dev
```

#### b. [CMD2](CMD2): 
```
.\venv\Scripts\activate
uvicorn main:app --reload
```

#### c. [CMD3](CMD3): 
```
.\venv\Scripts\activate
python worker.py
```

### Test d'orchestration
```
curl -X POST "http://127.0.0.1:8000/orchestrate"  -H "accept: application/json" -H "Content-Type: application/json" -d "{\"mot\": \"robe\"}"
```

# III - SECURITE AVEC API MANAGER
## III.1. Installation APIM
https://apim.docs.wso2.com/en/4.3.0/

## III.2. Installation JDK 21
https://jdk.java.net/archive/ (choisir le release 21)

## Creatation REST API FROM SCRATCH DANS APIM
- a) Se connecter dans APIM publisher (login: admin et password: admin) https://localhost:9443/publisher

- b) Cliquer Rest API puis Start From Scratch (Name: SVM_API, Contexte: /svm, version: 1.0.0, EndPoint: http://127.0.0.1:8000, Display Name: SVM_API)

## Test d'API
a) Faire une prediction de maniere securisé avec WSO2 API MANAGER
curl -k -X POST "https://localhost:8243/svm/1.0.0/predict" -H "accept: */*" -H "Content-Type: application/json" -H "Authorization: Bearer BEARER_TOKEN" -d "{\"mot\": \"robe\"}"

b)  Afficher la performance du modele SVM de maniere securisé avec API MANAGER
curl -k -X GET "https://localhost:8243/svm/1.0.0/show_perf_as_number" -H "accept: */*" -H "Authorization: Bearer BEARER_TOKEN"

c) Afficher la performance du modele SVM, à tant que graph, de maniere securisé
curl -k -X GET "https://localhost:8243/svm/1.0.0/show_perf_as_graph" -H "accept: */*" -H "Authorization: Bearer BEARER_TOKEN" -o svm_graph.png

d) Faire une orchestration d'API avec TEMPORAL
curl -k -X POST "https://localhost:8243/svm/1.0.0/orchestrate" -H "accept: */*" -H "Content-Type: application/json" -H "Authorization: Bearer BEARER_TOKEN" -d "{\"mot\": \"robe\"}"