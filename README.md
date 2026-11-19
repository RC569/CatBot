`docker build -t catbot ./`

`compose.yml`

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

if using docker to run the bot and koito use `docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' koito` to get the IP for the koito container
