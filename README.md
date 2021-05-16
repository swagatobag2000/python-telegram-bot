# python-telegram-bot

## How to make python-telegram-bot
### 1. Registering a Telegram Bot
       
- Choose a bot name and then choose a username for your bot. It must end in `bot`
- Like : newsbuddy_bot
- Then the bot will be created 
 
### 2. Setup a Python Virtual Environment
A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.
- Create a Project Folder and run following command to create a new virtual environment inside your project folder:

```
python -m venv myvenv
```

- After running above command, a folder named myvenv will get created in your project folder. Activate the virtual environment by running following command:
   - For ubuntu and mac users:

      ```
      source myvenv/bin/activate
      ```

    - For windows users:

      ```
      myvenv\Scripts\activate
      ```
### 3. Install required Python Packages:

```
pip install python-telegram-bot
```

### 4. Start Coding

- Enable Logging

```python
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
```


- Create Updater

```python
updater = Updater(TOKEN)
```

- Create Dispatcher

```python
dp = updater.dispatcher
```

- Add handlers

```python
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(MessageHandler(Filters.text, echo_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)
```

### 5. Setting up a server

- Install Flask

```
pip install flask
```

- Setup Webhook

```python
# create telegram bot object
bot = Bot(TOKEN)
# set webhook for telegram bot
bot.set_webhook("https://protected-fjord-75558.herokuapp.com/" + TOKEN)
```

- Create view to handle webhooks

```python
@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    # create update object from json-format request data
    update = Update.de_json(request.get_json(), bot)
    # process update
    dispatcher.process_update(update)
    return "ok"
```

- Generate Public URL for Webhook using ngrok.io

> *ngrok is a free tool that allows us to tunnel from a public URL to our application running locally.*

- Download [ngrok](https://ngrok.com/download)
- Unzip it.
- Run ngrok from command line (from the location where executable is stored)
- Ports currently supported for Webhooks: 443, 80, 88, 8443
```
  ./ngrok http 8443
```
- Copy the HTTPS Forwarding URL

### 5. Introduction to Dialogflow

- Login into [dialogflow console](https://console.dialogflow.com/api-client/#/login)

- Create a new agent or import a pre-built agent

- From settings page of agent, open the service account of your project in Google Cloud Console

- Create a new service account for your project. Download private key for the service account in a JSON file


- Install Python Client for Dialogflow
- [dialogflow-python-client](https://github.com/googleapis/dialogflow-python-client-v2)
```
pip install dialogflow
```
```python
# in utils.py
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'client.json'
# Original address can be given or client.json should be present in same directory
# client.json is the key file downloaded from google cloud console

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-xsfd"
# This Project id can be found in settings page of agent
```

```python
def detect_intent_from_text(text, session_id, language_code='en'):
  session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
  text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
  query_input = dialogflow.types.QueryInput(text=text_input)
  response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
  return response.query_result
response = detect_intent_from_text("show me sports news from india in hindi", 12345)
```

```python
response.intent.display_name
```

:arrow_forward: `get_news`

```python
dict(response.parameters)
```

:arrow_forward: `{'geo-country': 'India', 'language': 'Hindi', 'topic': 'Sports'}`

### 6. Integrating dialogflow to telegram bot

```python

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()

def get_reply(query, chat_id):
	response = detect_intent_from_text(query, chat_id)

	if response.intent.display_name == 'get_news':
		return "get_news", dict(response.parameters)
	else:
		return "small_talk", response.fulfillment_text
```


- News Source

```
pip install gnewsclient
```

```python
client.location = 'India'
client.language = 'Hindi'
client.topic = 'Sports'
```

```python
client.get_config()
```
:arrow_forward: `{'language': 'Hindi', 'location': 'India', 'topic': 'Sports'}`

```python
client.get_news()
```
:arrow_forward: 
`[{'link': 'https://news.google.com/__i/rss/rd/articles/CBMijwFodHRwczovL3d3dy5hYWp0YWsuaW4vc3Bv.........?oc=5',
  
  'media': None,
  
  'title': "विराट कोहली के समर्थन में उतरे सलमान बट्ट, माइकल वॉन की ऐसे की 'बेइज्जती' - Aaj Tak"},
 
 {'link': 'https://news.google.com/__i/rss/rd/articles/CBMigwFodHRwczovL3d3dy5saXZlaGluZHVzdGFuLm........?oc=5',
  
  'media': None,
  
  'title': 'दिल्ली: मर्डर केस में पहलवान सुशील कुमार के खिलाफ गैर जमानती वारंट जारी - Hindustan'},
 
 {'link': 'https://news.google.com/__i/rss/rd/articles/CBMipwFodHRwczovL3d3dy5qYWdyYW4uY29tL2Nya..........?oc=5',
  
  'media': None,
  
  'title': 'भुवनेश्वर कुमार ने टेस्ट नहीं खेलने की खबर को नकारा, कहा- तीनों फॉर्मेट में चयन के लिए उपलब्ध हूं - दैनिक जागरण'}]`

- Integrating gnewsclient in telegram bot

```python
def fetch_news(parameters):
	client.language = parameters.get('language')
	client.location = parameters.get('geo-country')
	client.topic = parameters.get('topic')
	return client.get_news()[:5]
```

### 7. Custom Keyboard Reply Markup

```python
def news(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Choose a category", 
		reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))
```

- A keyboard is provided as a list of lists (consider it like a table)

```python
topics_keyboard = [
	['Top Stories', 'World', 'Nation'], 
    ['Business', 'Technology', 'Entertainment'], 
	['Sports', 'Science', 'Health']
]
```

### 8. Create some new files for Heroku deployment

- Procfile : A Procfile is a mechanism for declaring what commands are run by your application's dynos on the Heroku platform.

```
web gunicorn app:app
```

Also, install `gunicorn` in your virtual environment:
```
pip install gunicorn
```
- runtime.txt

To specify a particular version of Python via your app's runtime.txt

```
python-3.9.5
```

- requirements.txt

Contains all 3rd party libraries required by your app.

Simply do:
```
pip freeze > requirements.txt
```

to generate a **requirements.txt** file.

- .gitignore

.gitignore file specifies patterns which are used to exclude certain files in your working directory from your Git history.

```
myvenv/
*.pyc
```

### 9. Now, its time to create a Heroku app!


- Setup Git repository [Download](https://git-scm.com/downloads)

    - Initialize a new git repository in your project folder.
    ```
    git init
    ```

    - Add all untracked files to git repository by:
    ```
    git add .
    ```

    - Commit the changes to git repository by:
    ```
    git commit -m "YOUR_COMMIT_MESSAGE_HERE"
    ```
    
- Create a new [heroku account](https://signup.heroku.com/)

- Download [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

- Create a new Heroku app.
```
heroku create <your-app-name>
```

- Edit `app.py` and set webhook URL as your Heroku app's URL

```python
bot.set_webhook("https://protected-fjord-75558.herokuapp.com/" + TOKEN)
```

- Finally, you are ready to deploy your app by pushing your *local git repository* to the remote *heroku app's git repository* by: 
```
git push heroku master
```
    
- To check the logs of your heroku app:
```
heroku logs
```
