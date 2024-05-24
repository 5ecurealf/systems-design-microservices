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
    
#upload route to upload file for conversion   
@server.route("/upload",methods=["POST"])
def upload():
    access,err = validate.token(request) 
    # deserialise the claims json object to a python object
    access = json.loads(access)

    #if claims property admin is true upload the file
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1: #upload only 1 file max
            return "exactly 1 file required",400
        
        for _, f in request.files.items():
            err = util.upload(f,fs,channel,access)
            if err:
                return err
            
        return "success!",200
    else:
        return "not authorised",401
    
    #endpoint to download the mp3 that was created from the video
    @server.route("/download")
    def download():
        pass


if __name__ == "__main__":
    server.run(host="0.0.0.0",port=8080)



