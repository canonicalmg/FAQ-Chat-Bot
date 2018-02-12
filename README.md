![picture](images/use-case.png)

# Basic FAQ chat bot (Version 1.1)

## How to install
Download Python 2.7.x - https://www.python.org/downloads/

Download pip `sudo easy_install pip`

Download Virtualenvwrapper `pip install virtualenvwrapper`

Finally,
```commandline
mkvirtualenv chatbot
pip install -r requirements.txt
python main.py
``` 

## About the bot
![picture](images/cosine.PNG)
Source[https://en.wikipedia.org/wiki/Cosine_similarity]

The bot is trained on the FAQ page for a given site and uses that as it's corpus to compare the similarity between user input and known FAQ questions. If a good match is found it will return the answer, otherwise it will let the user know there was an issue.
What determines a 'good' similarity is defined in the Bot.settings object, by default we say that anything over a score of 50% is a good match but feel free to play around with this.

## Future work
This will be turned into a back-end service which will communicate with an embeddable front-end widget that can be integrated into any website.
It will require that the admin properly configures the corpus so I will probably include a web scraper or give the ability to add your own file.

Back-end will be Django, hosted on Heroku. Using websockets to reply (See https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django)
Front-end will be js that initializes communication with the backend and indicates which corpus is to be used. (corpus indication is important because we run the risk of overfitting the data if we do not specify which FAQ page the user is referring to)
