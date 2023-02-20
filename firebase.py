import firebase_admin
from firebase_admin import db

cred = firebase_admin.credentials.Certificate("NetLab12-privateKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://netlab12-e05af-default-rtdb.europe-west1.firebasedatabase.app/"})
ref = firebase_admin.db.reference("/")


def stream_handler_creator(message_handler):
    def stream_handler(incomingData) :
        if incomingData.event_type == "put":
            if incomingData.path == "/":
                if incomingData.data is not None:
                    for key in incomingData.data:
                        message = incomingData.data[key]
                        message_handler(message)
            else:
                message = incomingData.data
                message_handler(message)
    return stream_handler


messages = ref.child("messages")


