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
       service_instances=[]
       service_nodes=[]
       for service_instance in range(len(servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances'])):
           service_instances.append(servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances'][service_instance]['Id'])
           node_ip=servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances'][service_instance]['Attributes']['AWS_INSTANCE_IPV4']
           node_port=servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances'][service_instance]['Attributes']['AWS_INSTANCE_PORT']
           service_nodes.append(node_ip+":"+node_port)
       host, port = servers[0]
       print("host-"+str(host)+":"+str(port))
       service = {
           'name': service_obj[0]['Name'],
           'addr': socket.gethostbyname(host),
           'port': str(port),
           'num_hosts': len(servicediscovery.list_instances(ServiceId=service_obj[0]['Id'])['Instances']),
           'service_instances': service_instances,
           'service_nodes':service_nodes,
           'text': requests.get("http://"+str(host)+":"+str(port)+"/").content.decode("utf-8")
       }
       print(str(service))
       return render_template("index.html", service=service)
    except Exception as e:
       print("backend: Something went terribly wrong!\n"+str(e))
       return render_template("index.html", service={'text': 'Something went terribly wrong!'+str(e)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=80)