FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY auxiliary_elements/_transformer_function.py auxiliary_elements/
COPY auxiliary_elements/__init__.py auxiliary_elements/__init__.py
COPY model model

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
