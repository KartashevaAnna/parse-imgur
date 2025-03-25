# parse-imgur
- Clone the project: ```git clone```
- Activate virtual environment: ``poetry shell```
- Install dependencies: ```poetry install```
- Register an app at imgur.
- Specify "https://www.getpostman.com/oaoth2/callback" as the callback there.
- Get Client ID and Client Secret from Imgur after registering your app with your account.
- Go to Postpan, select OAoth2 in the Authorization section, specify Client ID and Client Secret. Authorize via browser. 
- Create a "bearer_token.py". Write Access Token as TOKEN from and CLIENT_ID there.
Run python with: ```poetry run python run.py```
