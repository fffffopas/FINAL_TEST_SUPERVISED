import subprocess
import sys

TEST_SIZE = input("Введите необходимый размер тестовой выборки(Пример: 0.3; ввод должен быть числом с плавающей запятой): ")
N_TRIALS = input("Введите необходимое количество испытаний(Пример: 25, ввод должен быть целочисленным): ")
WANT_DUMP = input("Желаете сохранить модель в любом случае(Да/Нет): ")

steps = [
    ("data_splitting", ["--test-size", TEST_SIZE]),
    ("hyperparameters_tuning", ["--n-trials", N_TRIALS]),
    ("model_training", []),
    ("model_evaluation", []),
]
if WANT_DUMP == "Да":
    steps.append(("dumping_model", []))

for module, args in steps:
    print(f"\n{'='*50}\nRunning: {module}\n{'='*50}")
    result = subprocess.run([sys.executable, "-m",
                            f"analysis_solution.{module}", *args],
                            check=True
                        )
    

if WANT_DUMP == "Нет" and input("Желаете сохранить модель(Да/Нет, Вы можете посмотреть метрики в ui(mlflow ui)): ") == "Да":
    print(f"{'='*50}Выполняется сохранение модели{'='*50}")
    result = subprocess.run([sys.executable, "-m",
                                f"analysis_solution.dumping_model", *args],
                                check=True
                            )
    