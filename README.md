# MISP bot for Matrix

This bot is based on the [nio-template](https://github.com/anoadragon453/nio-template/), you can go look at it for more details.

# Installation

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -e .
```

# Configuration

The sample configuration file is called `sample.config.yaml`.

It is recommemded to make a copy of it and update it accordingly, expecially the `matrix` section (id, password, homeserver, ...).

And of course, the MISP specific configuration in the `misp` section in order to allow the bot to
connect to your instance:

* `url`: the URL of the MISP instance
* `apikey`: the API key of the user you want ot use
* `alert_tags`: a list of tags to include to the automatic alerting (see below)
* `allowed_servers`: list of the servers where all the users are allowed to talk to the bot
* `allowed_users`: list of individual users allowed to talk to the bot

# Start the bot

`matrix-misp-bot myconfig.yaml`

# Usage

You need to open a room with this bot and the commands are as follow:

* `!c misp search <search query>`: search attributes with this key (`%` can be used as a wildcard)
* `!c misp subscribe`: Subscribe to the automatic notifications (see below)

# Alerting

If you configure the `alert_tags` key, all the users who ran `!c misp subscribe` will
be notified is an event is created/updated and has this tag set.
