from flask import Flask
import socket
import boto3
from boto3.dynamodb.conditions import Key, Attr
app = Flask(__name__)

@app.route("/ping")
def ping():
    return "", 200

@app.route("/")
def do_work():
    try:
        #your code here
        return "I'm Working fine!"
    except Exception as e:
        print("Something Terrible Happened - "+str(e))
        return "I'm a worker and I Failed"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)