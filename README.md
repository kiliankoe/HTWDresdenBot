# 📚 HTWDresdenBot

Telegram bot to give you current data from the [University of Applied Sciences Dresden](https://www.htw-dresden.de).

Message [@htwdresdenbot](http://telegram.me/htwdresdenbot) to get started 👌




## Usage

Just type `/` in a chat with the bot and your client will list possible commands.



## Disclaimer

**This is not an official HTW Dresden project.**

When asking the bot for your grades it unfortunately requires your login details. The telegram account [@htwdresdenbot](http://telegram.me/htwdresdenbot) is run by me, [@kiliankoe](http://telegram.me/kiliankoe). This means that you're basically trusting me to keep your login safe. Whilst I promise not to do anything nefarious with that, it is *extremely advisable* to run an instance of this bot yourself that you control and trust. Keep reading for instructions on how to do that.



## Run your own instance

All you need to run this bot is a telegram bot token (message [@botfather](http://telegram.me/botfather)) and docker on the machine you want to run this from. Once you do, run the following.

```shell
$ git pull https://github.com/kiliankoe/htwdresdenbot
$ cd htwdresdenbot
$ docker build -t htwbot .
$ docker run -d --name htwbot -v $(pwd)/htw_bot.db:/htwbot/htw_bot.db -e TELEGRAM_BOT_TOKEN='your_bot_token' htwbot
```

If you're not into using docker, you can also run the bot directly by executing `main.py` with a python interpreter of your choice (supported/tested is 3.6).
