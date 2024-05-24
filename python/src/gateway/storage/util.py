import pika, json
#upload file to mongodb
#place message in the rabbitMq queue once successfully uploaded
#downstream service can pull message from queue and process it by pulling it from the mongodb
#async flow between gateway service and video processing service
 
def upload(f,fs,channel,access):
    try:
        fid = fs.put(f) # capture the file id from mongodb if successful

    except Exception as err:
        return "internal server error",500
    
    message = {
        "video_fid":str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }
    # delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE makes sure 
    # thats messages are persisted in the queue in the event that
    # the pod fails when it spins back up the messages are still there
    # we need to also make the messages within the queue to be durable
    # which mesans the mesages are retained in case of a pod crash 
    # PERSISTENT_DELIVERY_MODE makes sure the messages are persisted 
    # until the consumer removes the message from the queue

    # if the message unsuccessful on the queue, remove the file from the db

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except:
        fs.delete(fid)
        return "internal server error", 500