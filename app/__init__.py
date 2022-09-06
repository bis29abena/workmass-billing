from flask import Flask
from redis import Redis
from rq import Queue

app = Flask(__name__)
r = Redis()
q = Queue(connection=r)


if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views