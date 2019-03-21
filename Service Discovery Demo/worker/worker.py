from flask import Flask
import socket
import boto3
from boto3.dynamodb.conditions import Key, Attr
app = Flask(__name__)

@app.route("/ping")
def ping():
    return "", 200

@app.route("/lp/<find>")
def do_work(find):
    print("working to find-"+find)
    try:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table('demoTable')
        print(table.creation_date_time)
        response = table.query(
            KeyConditionExpression=Key('myPrimaryKey').eq(int(find))
        )
        items = response['Items']
        print("Found IT!-"+str(items[0]['LP']))
        return str(items[0]['LP'])
    except Exception as e:
        print("Something Terrible Happened - "+str(e))
        return "I'm a worker and I Failed"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)