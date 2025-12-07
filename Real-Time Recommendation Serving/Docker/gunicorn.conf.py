# Gunicorn configuration for production
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
loglevel = "info"
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/errors.log"
capture_output = True
