# campgamesbot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Try it on telegram](https://img.shields.io/badge/try%20it-on%20telegram-0088cc.svg)](http://t.me/campgamesbot)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


👾 Telegram-bot:
https://t.me/campgamesbot


### User can:
* select games by filters


### Administration toolbar:
* ```/admin``` -> buttons menu:
    * parsing departments structure into json format
    * statistics can be requested any time and regularly send every morning,
    * push notification to all users in db,
    * set ads under schedule
* Commands:
    * __Public__:
        * ```/id``` return current chat id
        * ```/time``` return current server time


Prepare system
===============
> python --version >>> Python 3.8.5
>
> linux version >>> Ubuntu 20.0


Telegram API wrapper used: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

On a AWS Ubuntu 18.04 new machine, below installations are required:

* `sudo apt-get install gcc libpq-dev`
* `sudo apt-get install python3-dev python3-pip python3-venv python3-wheel`
* `sudo apt install git-all`
* `pip3 install wheel`


Launch project:
===============
* `git clone --recurse-submodules https://repo.url repo` - clone repo
* `cd campgames_bot` - move to project directory
* `cp .env.example .env` - create your .env file and insert your values
* `poetry install`
* `poetry shell` - run virtualenv shell
* `python3 -m bot` - run as python module from top src directory to acsess database layer

### Run with docker
* `docker volume create campgames-volume`
* `docker compose up --build`
