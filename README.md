personal discord bot

build docker image: `docker build -t catbot ./`

## compose.yml
```yaml
services:
    catbot:
        stdin_open: true
        tty: true
        environment:
            - DISCORD_BOT_TOKEN=
            - KOITO_APIKEY=
            - KOITO_BASEURL=
        image: catbot:latest
```
