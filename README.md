# Fastapi service
1. Данный продукт предсказывает произойдет отток клиентов или нет|
2. Полный анализ, когортный анализ оттока и построение паплайна приведены в директории приведены в директории Analysis_solution|
3. Директория Auxiliary_elements содержит две вспомогательные функции для паплайна|
4. Основная логика самого api сервиса приведена в файле app.py
5. Также предлагается обертка в докер|

1. This product predicts whether customer churn will occur or not.
2. A full analysis, cohort analysis of churn, and the construction of a pipeline are provided in the Analysis_solution directory.
3. The Auxiliary_elements directory contains two auxiliary functions for the pipeline.
4. The main logic of the api service itself is provided in the app.py file.
5. A docker wrapper is also offered.

## Stack
- FastAPI
- scikit-learn / catboost (classic Ml)
- optuna
- Docker

## How to run
- docker buildx guild -t churn-predictor:v1 .
- docker run -d -p 8000:8000 --name apiname churn-predictor:v1 