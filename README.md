## Summary

A simple slackbot for sending Opsgenie alerts or page requests. To initiate an alert simply enter `/sendpage` in a Slack workspace where the bot has been added.

## Dependicies

```
brew install pyenv # python version manager
brew install pyenv-virtualenv # recommend using virtual environments
pyenv install 3.9.5 # installs python
pyenv virtualenv 3.9.5 slackbot # creates virtual environment slackbot
pyenv local slackbot # activates virtual environment
pip install -r requirements.txt # installs requirements
```

## Authentication

Three environement variables must be set to authenticate the bot:

- `SLACK_BOT_TOKEN` - Slack bot token
- `SLACK_APP_TOKEN` - Slack app token
- `OPSGENIE_INTEGRATION_KEY` - Opsgenie integration API key
