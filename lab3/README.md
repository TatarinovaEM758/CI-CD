
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


2. Создание манифестов
2.1 PostgreSQL Deployment (postgres-deployment.yaml)
![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab3/img/1.png)

![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab3/img/3.png)


4. Результаты

![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab3/img/6.png)
Скриншот kubectl get pods
![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab3/img/13.png)

![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab3/img/14.png)

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
