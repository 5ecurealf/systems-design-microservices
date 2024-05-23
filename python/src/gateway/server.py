import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)
server.config["MONGO_URI "] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server) # abstracts the mongodb connection to the flask app

fs = gridfs.GridFS(mongo.db)

#configue rabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq")) # string references the rabbitmq host 

# communicates with Auth service to log the user in and assign a token to the user
@server.route("/login",methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err