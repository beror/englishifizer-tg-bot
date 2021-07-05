A Telegram bot to force a Telegram user to send English-only messages (deletes messages that are not in English). Tries to detect transliteration and, as of now, especially efficient against Slavic languages.

### How to use
## Modifying the code for your needs
You can setup the bot by searching for "# EDIT ME" comments on the right of the code that needs to be edited before a bot can be launched. These include the target's username, the bot's token etc.

## Launching the bot
# Locally
The most simple way to launch it is to change from webhooks to polling. Replace the call to set a webhook with an argumentless call to start polling (".start_webhook(...)" to ".start_polling()")

# Deploying on Heroku
Once you've modified the code for your needs, the "Procfile" and "requirements.txt" files need to be set up. Learn about them somewhere else

### How it works
## The language processing
The method, in part, works by detecting trigrams of different languages. Roughly speaking, the more trigrams of a certain language is detected, the more the probability that the text is in a certain langauge.
A dedicated thanks thanks to the [langdetect](https://github.com/Mimino666/langdetect) library, which is a port of Nakatani Shuyo's [language-detection](https://github.com/shuyo/language-detection) library to Python, which implements this method.