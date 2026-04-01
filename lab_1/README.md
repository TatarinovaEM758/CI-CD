
**	Цель работы:**
Используя образ wordpress:
CMS (Контент-аналитика). Запустить контейнер. Проверить доступность страницы установки. (Опционально: подключить к внешней БД, если есть навыки, или просто проверить запуск сервиса).


•	Ход выполнения работы:
o	Успешное выполнения команд docker version, docker run hello-world.
 
  ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/version%20i%20helloword.png)
  
 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/work%20brouser.png)

o	 Docker ps – выводит запущенные контейнеры
o	Docker images – выводит список всех образов
 
 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/run%20i%20images.png)
 
 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/images%20i%20ps.png)
  
#Варинат 15

Используя образ wordpress:
CMS (Контент-аналитика). Запустить контейнер. Проверить доступность страницы установки. (Опционально: подключить к внешней БД, если есть навыки, или просто проверить запуск сервиса).


Создадим контейнер my-wordpress

 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/create%20wordpress.png)
 
Команда docker ps показывает нам, что контейнер my-wordpress создан и запущен

 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/run%20create.png)
 
Проверка в браузере на странице http://localhost:8080 запуск контейнера – страница доступна.
 
 ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/workwordpressbrouser.png)

Проверка работы контейнера 

  ![](https://github.com/TatarinovaEM758/CI-CD/blob/main/lab_1/images/proverka.png)
 
Выводы:
1.	Docker-контейнеризация упрощает развертывание веб-приложений. Запуск WordPress занял менее минуты и не потребовал установки PHP, MySQL или веб-сервера на хостовую систему.
2.	Контейнер изолирует приложение от хост-среды. Это гарантирует, что приложение будет работать одинаково на любой платформе с Docker.
3.	Проброс портов обеспечивает доступ к сервису извне. Благодаря параметру -p 8080:80 веб-интерфейс стал доступен по адресу http://localhost:8080.
4.	Docker является базовым инструментом для CI/CD. Умение быстро поднимать и тестировать сервисы в контейнерах — первый шаг к автоматизации развертывания в пайплайнах.
5.	Получен практический опыт. Освоены основные команды Docker для управления контейнерами: запуск, остановка, просмотр логов, проверка статуса.

