# RU
## Fastapi сервис

### Описание
Данный продукт способен предсказывать на основе данных абонентов, уйдут они в отток или нет.
Модель основана на датасете [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/). Берется модель catboostClassifier,
в стеке также используется LightGBMClassifier, но в оптимальной версии продукта первая показывает себя лучше, а потому только она находится в requirements.txt

В дальнейшем планирутся добавить 2 модели на схожие тематики

В настоящий момент времени микросервис способен обрабатывать множество запросов за раз (не асинхронно, в формате dict(orient="records"))


### Структура проекта
```Project:.
│   .gitignore
│   app.py
│   Dockerfile
│   README.md
│   requirements.txt
│   test.ipynb
│   
├───.github
│   └───workflows
│           ci.yml
│           
├───analysis_solution
│       cohort_analysis_of_churn.ipynb
│       EDA.ipynb
│       pipeline.ipynb
│       
├───auxiliary_elements
│   │   _transformer_function.py
│   │   __init__.py
│       
├───model
│       model_cb.joblib
│       
├───required_data
│       tests.csv
│       
├───tests
│   │   test_.py
│   │   __init__.py
```

### Стек
- FastAPI
- scikit-learn / catboost / LightGBM (classic Ml)
- optuna
- Docker
- pytest

### Как запустить
Предостовляется несколько способов запуска в зависимости от ваших целей:
1. Вам необходимо локально собрать docker образ и запустить контейнер:
    - docker buildx build -t churn-predictor:v1 .
    - docker run -d -p 8000:8000 --name [имя api] predictor-api:[актуальная версия]
2. Вам необходимо только запустить контейнер:
    - [Устанавливаете актуальную версию образа /predictor-api](https://hub.docker.com/repositories/sdfgsgsjghjfgh)
    - docker run -d -p 8000:8000 --name [имя api] predictor-api:[акткальная версия] 
3. Вам достаточно просто запутить проект:
    - [Установить python версии 3.11 или 3.12](https://www.python.org/downloads/)
    - Далее прописать в cmd: pip install -r requirements.txt
    - После этого: uvicorn app:app --reload

# EN
## Fastapi service

### Description
This product is able to predict based on subscribers' data whether they will go to churn or not.
The model is based on the [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn/) dataset. The catboostClassifier model is taken,
LightGBMClassifier is also used in the stack, but in the optimal version of the product the first one performs better, and therefore only it is in requirements.txt

 In the future, it is planned to add 2 models on similar topics

At the moment, the microservice is capable of processing multiple requests at once (not asynchronously, in the format of dict(orient="records"))


### Project structure
```Project:.
│   .gitignore
│   app.py
│   Dockerfile
│   README.md
│   requirements.txt
│   test.ipynb
│   
├───.github
│   └───workflows
│           ci.yml
│           
├───analysis_solution
│       cohort_analysis_of_churn.ipynb
│       EDA.ipynb
│       pipeline.ipynb
│       
├───auxiliary_elements
│   │   _transformer_function.py
│   │   __init__.py
│       
├───model
│       model_cb.joblib
│       
├───required_data
│       tests.csv
│       
├───tests
│   │   test_.py
│   │   __init__.py
```

### Stack
- FastAPI
- scikit-learn / catboost (classic Ml)
- optuna
- Docker
- pytest

### How to run
There are several ways to run it, depending on your goals:
1. You need to build the docker image locally and run the container:
 - docker buildx build -t churn-predictor:v1 .
 - docker run -d -p 8000:8000 --name [apiname] predictor-api:[actual-version]
2. You only need to run the container:
 - [Install the latest version of the /predictor-api image](https://hub.docker.com/repositories/sdfgsgsjghjfgh)
 - docker run -d -p 8000:8000 --name [apiname] predictor-api:[actual-version] 
3. All you need to do is run the project:
 - [Install python version 3.11 or 3.12](https://www.python.org/downloads/)
 - Then, enter the following command in cmd: pip install -r requirements.txt
 - After that: uvicorn app:app --reload