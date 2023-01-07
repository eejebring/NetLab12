import firebase_admin
from firebase_admin import db

cred = firebase_admin.credentials.Certificate("NetLab12-privateKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://netlab12-e05af-default-rtdb.europe-west1.firebasedatabase.app/"})
ref = firebase_admin.db.reference("/")

print("hi")


def message_handler(message):
    print(message)


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


newMessage = {"name": "Emil", "text": "logged in"}
messages = ref.child("messages")

#messages.push(newMessage)

messages_stream = messages.listen(stream_handler)

