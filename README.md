# HASS External Ping

Tool for checking connection to your Home Assistant via external network every X minutes with sending notifies to Telegram

## Docker build & run

```
docker build -t hass-external-ping:1.0.0 .
```

```
docker run -d --name hass-external-ping --env-file .env --restart always hass-external-ping:1.0.0
```