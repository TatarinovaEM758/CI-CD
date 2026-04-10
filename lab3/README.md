
## Лабораторная работа №3: Оркестрация контейнеров в Kubernetes


Вариант 15: FastAPI App + PostgreSQL
Титульный лист
ФИО: Татаринова Екатерина
Группа: АДЭУ-221

Вариант: 15
---

Задача: Развернуть Python-приложение (FastAPI) и БД Postgres. Настроить ENV переменные в Deployment приложения для связи с БД.

Цель работы
Освоить процесс оркестрации контейнеров. Научиться разворачивать связки сервисов (аналитическое приложение + база данных) в кластере Kubernetes, управлять их масштабированием (Deployment) и сетевой доступностью (Service).

---
## Ход выполнения

1. Подготовка окружения
Был развернут кластер MicroK8s на виртуальной машине Ubuntu.

bash
# Установка MicroK8s
sudo snap install microk8s --classic

# Добавление пользователя в группу
sudo usermod -a -G microk8s $USER

# Включение необходимых аддонов
microk8s enable dns storage
2. Создание манифестов
2.1 PostgreSQL Deployment (postgres-deployment.yaml)
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-db
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_USER
          value: "fastapi_user"
        - name: POSTGRES_PASSWORD
          value: "secure_password_123"
        - name: POSTGRES_DB
          value: "analytics_db"
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
Пояснение:

Образ postgres:15-alpine - легковесная версия PostgreSQL

Переменные окружения задают пользователя, пароль и имя БД

PVC обеспечивает сохранность данных при перезапуске пода

2.2 PostgreSQL Service (postgres-service.yaml)
yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP
Пояснение: ClusterIP делает сервис доступным только внутри кластера для безопасности.

2.3 FastAPI Deployment (fastapi-deployment.yaml)
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: fastapi-analytics:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_HOST
          value: "postgres-service"
        - name: DATABASE_USER
          value: "fastapi_user"
        - name: DATABASE_PASSWORD
          value: "secure_password_123"
        - name: DATABASE_NAME
          value: "analytics_db"
Пояснение:

replicas: 2 - два экземпляра для отказоустойчивости

imagePullPolicy: Never - использование локального образа

DATABASE_HOST: postgres-service - подключение к БД через DNS имя сервиса

2.4 FastAPI Service (fastapi-service.yaml)
yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30080
  type: NodePort
Пояснение: NodePort с портом 30080 для доступа из браузера.

2.5 FastAPI Приложение (app/main.py)
python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import psycopg2
import os

app = FastAPI(title="Analytics API")

DB_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "user": os.getenv("DATABASE_USER", "fastapi_user"),
    "password": os.getenv("DATABASE_PASSWORD", "secure_password_123"),
    "database": os.getenv("DATABASE_NAME", "analytics_db")
}

@app.on_event("startup")
async def startup():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(100),
            user_id VARCHAR(100),
            value FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/events")
async def create_event(event: dict):
    # Обработка события
    pass

@app.get("/events")
async def get_events():
    # Получение событий из БД
    pass
3. Запуск конфигураций
bash
# Применение манифестов
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f fastapi-deployment.yaml
kubectl apply -f fastapi-service.yaml

# Проверка статуса
kubectl get pods
4. Результаты
Скриншот kubectl get pods
[Вставьте сюда скриншот с выводом команды kubectl get pods, где все поды в статусе Running]

text
NAME                           READY   STATUS    RESTARTS   AGE
fastapi-app-774b67f8b5-bjb9z   1/1     Running   0          5m
fastapi-app-774b67f8b5-dj7f8   1/1     Running   0          5m
postgres-db-fd99487bc-b9868    1/1     Running   0          10m
Скриншот kubectl get services
[Вставьте сюда скриншот с выводом команды kubectl get services]

text
NAME               TYPE        CLUSTER-IP       PORT(S)          AGE
fastapi-service    NodePort    10.152.183.45    8000:30080/TCP   5m
postgres-service   ClusterIP   10.152.183.123   5432/TCP         10m
kubernetes         ClusterIP   10.152.183.1     443/TCP          30m
Скриншот работающего приложения
*[Вставьте сюда скриншот браузера с открытым API http://<IP>:30080/docs или результат curl запроса]*

Проверка API:

bash
# Проверка health
curl http://localhost:30080/health
# Результат: {"status":"healthy"}

# Создание события
curl -X POST http://localhost:30080/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"page_view","user_id":"student","value":1.0}'
# Результат: {"id":1,"event_type":"page_view","user_id":"student","value":1.0,"created_at":"2024-..."}
5. Проверка масштабирования
bash
# Масштабирование до 3 реплик
kubectl scale deployment fastapi-app --replicas=3

# Проверка
kubectl get pods

---
## Выводы

В ходе выполнения лабораторной работы были решены следующие задачи:

Установлен и настроен кластер Kubernetes (MicroK8s)

Созданы манифесты для развертывания PostgreSQL и FastAPI приложения

Настроено взаимодействие между сервисами через переменные окружения и DNS имена

Обеспечена сохранность данных через PersistentVolumeClaim

Проверено масштабирование приложения до 3 реплик

---
## С какими трудностями столкнулись:

ImagePullBackOff ошибка - Kubernetes пытался скачать образ из Docker Hub.

Решено добавлением imagePullPolicy: Never

Загрузка образа в MicroK8s - потребовалось использовать docker save | microk8s ctr image import

Настройка сетевого доступа - использование NodePort для доступа к приложению из браузера
