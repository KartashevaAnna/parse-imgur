# parse-imgur
Проект собирает список всех альбомов автора по API и выдаёт ссылки на них не через API.

Этот же код отдельно собирает список всех альбомов со списком ссылок на все фотографии в них.
Изначально стояла задача собрать список ссылок на все фотографии, но в ходе выполнения оказалось, что в дальнейшем пользователю удобнее работать со списком альбомов.

- Clone the project: ```git clone```
- Activate virtual environment: ``poetry shell```
- Install dependencies: ```poetry install```
- Register an app at imgur.
- Specify "https://www.getpostman.com/oaoth2/callback" as the callback there.
- Get Client ID and Client Secret from Imgur after registering your app with your account.
- Go to Postpan, select OAoth2 in the Authorization section, specify Client ID and Client Secret. Authorize via browser. 
- Create a "bearer_token.py". Write Access Token as TOKEN from and CLIENT_ID there.
Run python with: ```poetry run python run.py```
