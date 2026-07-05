# RU
## Fastapi сервис

### Описание
Данный продукт предсказывает произойдет отток клиентов или нет

### Структура проекта
```
project:.
|   .gitignore
|   app.py
|   Dockerfile
|   README.md
|   requirements.txt
|   test.ipynb
|   
+---Analysis_solution
|   |   Cohort_analysis_of_churn.ipynb
|   |   EDA.ipynb
|   |   Pipeline.ipynb
|   |   
+---auxiliary_elements
|   |   _transformer_function.py
|   |   __init__.py   
|           
+---model
|       model.joblib

```

### Стек
- FastAPI
- scikit-learn / catboost (classic Ml)
- optuna
- Docker

### Как запустить
- docker buildx build -t churn-predictor:v1 .
- docker run -d -p 8000:8000 --name apiname churn-predictor:v1 

# EN
## Fastapi service

### Description
This product predicts whether there will be an outflow of customers or not

### Project structure
```
project:.
|   .gitignore
|   app.py
|   Dockerfile
|   README.md
|   requirements.txt
|   test.ipynb
|   
+---Analysis_solution
|   |   Cohort_analysis_of_churn.ipynb
|   |   EDA.ipynb
|   |   Pipeline.ipynb
|   |   
+---auxiliary_elements
|   |   _transformer_function.py
|   |   __init__.py   
|           
+---model
|       model.joblib

```

### Stack
- FastAPI
- scikit-learn / catboost (classic Ml)
- optuna
- Docker

### How to run
- docker buildx build -t churn-predictor:v1 .
- docker run -d -p 8000:8000 --name apiname churn-predictor:v1