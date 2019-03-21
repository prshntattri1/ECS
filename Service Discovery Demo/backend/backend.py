from flask import Flask, render_template, request
import socket
import requests
import json
import boto3
import socket
import dns.resolver
app = Flask(__name__)

@app.route("/")
def getLP():
    try:
       find = request.args.get('find')
       print("find - "+str(find))
       if find == None:
           service = {
              'val':'1',
              'name': 'Service-Name',
              'addr': 'Service IP(Private)',
              'num_hosts': 'Number of avilable hosts',
              'text': 'Let\'s find out'
           }          
           return render_template("index.html", service=service)
       elif int(find) >= 15 or int(find) <= 0:
           service = {
              'val':'1',
              'name': 'Service-Name',
              'addr': 'Service IP(Private)',
              'num_hosts': 'Number of avilable hosts',
              'text': 'I know what you are trying to pull here!'
           }
           return render_template("index.html", service=service) 
       else:
          servicediscovery = boto3.client("servicediscovery",region_name='us-east-1')
          resp = servicediscovery.list_services(
              Filters=[{'Name': 'NAMESPACE_ID', 'Values': ['ns-ezkdkoakc5qcgbdx']}]
          )
          print("resp -"+str(resp))
          service_obj = [service for service in resp.get('Services', []) if service['Name'] == "worker"]
          print("Service Obj"+str(service_obj))
          print("\nservice_obj[0]['Name']-"+service_obj[0]['Name'])
          answers = dns.resolver.query(service_obj[0]['Name']+".demo", 'SRV')
          print("answers SRV-"+str(answers))
          servers = [(rr.target.to_text(True), rr.port) for rr in answers]
          host, port = servers[0]
          print("host-"+str(host)+":"+str(port))
          service = {
              'val':find,
              'name': service_obj[0]['Name'],
              'addr': socket.gethostbyname(host),
              'num_hosts': len(servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances']),
              'text': requests.get("http://"+str(host)+":"+str(port)+"/lp/"+str(find)).content.decode("utf-8")
          }
          print(str(service))
          return render_template("index.html", service=service)
    except Exception as e:
       print("backend: Something went terribly wrong!\n"+str(e))
       return render_template("index.html", service={'text': 'Something went terribly wrong!'+str(e)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=80)