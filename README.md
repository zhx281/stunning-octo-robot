# Video

---

service file format

Create this file `myapp.service` in `/etc/systemd/system` with `nano` or `vim`

```
[Unit]
Description=My Simple App
After=network.target

[Service]
User="Replace User name"
Group="Replace Group name"
WorkingDirectory=/path/to/stunning-octo-robot
ExecStart=/path/to/stunning-octo-robot/.venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
ExecReload=/bin/kill -s HUP $MAINPID

[Install]
WantedBy=multi-user.target
```
