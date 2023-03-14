# codeforces_tasks_selector
App (FastAPI)  for save all tasks from codeforces and give them in telegram bot


## Motivation

Motivation to get a job opportunity and earn more experience in backend development


## Method and results

Methods were usual : to reach the goals which were defined by employer requirements. 
https://waytoa.notion.site/e82f8168db3547a08c043c691ed072ac

Results : In my view , I did a good job , but I implemented some bad practices in my code, but it is working properly.


## Repository overview

Provide an overview of the directory structure and files, for example:


![image](https://user-images.githubusercontent.com/58446568/224930709-e5547e8b-99f3-438c-90fb-73a3622e1493.png)




## Running instructions
Running postgresql and adminer in docker containers
```sh
git clone https://github.com/ELePhanT1708/codeforces_tasks_selector.git
cd codeforces_tasks_selector
docker-compose up --build 
``` 

Running fastapi_app with uvicorn

```sh
cd codeforces_tasks_selector
cd src
py .\fastapi_codeforce\__main__.py   
``` 

Running telegram bot on aiogram polling

```sh
cd codeforces_tasks_selector
cd src
py .\telegram_bot\bot.py    
``` 

Telegram bot link: https://t.me/CodeForce_tasks_bot

Add information to database:
You have to start from requesting to this endpoint
It will add all info from CodeForces API , it will take about 10 minutes
```sh
http://localhost:8000/tasks/save_all_tasks_initial 
``` 
After you can use telegram bot.




## Implementation details

Telegram bot link: https://t.me/CodeForce_tasks_bot 
In bot were included definitions of existing endpoints , and how to create request for get proper answer.

Updating of database based on fastapi_utils library with decorator @repeat_every(seconds=60 * 60) which send request to fastapi api to make update

MANY-to-MANY relations between tags and tasks implemented as temp topicInTask table which have task_id and tag_id . 

## Confines

1. During update the database , code will add only new tasks information to database and will not update old information bout existing tasks in database.
2. 
