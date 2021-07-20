from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from gridapp.models import Response
from datetime import datetime

import json
import subprocess
import sys

def run_item(password,username,server,port):
    command = f'sshpass -p {password} ssh {username}@{server} -p {port} python < script.py'
    process = subprocess.Popen(f'{command}',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #result = ssh.stdout.readlines()
    #if result == []:
    #   error = ssh.stderr.readlines()
    #	print(sys.stderr, "ERROR: %s" % error)
    #else:
    #   print(result)
    (out,err) = process.communicate()
    if process.returncode == 0:
        sout = out.decode("utf-8")
        d = json.loads(sout)
        d["Asset_Name"] = server
        d["Status"] = "UP"
        print(json.dumps(d))
        return json.dumps(d)
    else:
        errd = {'Asset_Name':server,'IP':'','MAC':'','Hostname':'','OS':''}
        serr = err.decode("utf-8")
        index = serr.rfind(":")
        errd['Status'] = serr[index+2:-2]
        print(json.dumps(errd))

    print('\n')

@method_decorator(csrf_exempt, name='dispatch')
class SubmitOneRequest(View):
    def post(self, request):
        data = json.loads(request.body)
        server = data['server']
        username = data['ssername']
        password = data['password']
        port = data['port']
        try:
            obj = Response.objects.get(Server=server, Username=username, Password=password, Port=port)
            dict = run_item(password, username, server, port)
            #TODO: check if error
            if dict['Status']=='UP':
                Assetname = dict['Asset_name'],
                ip = dict['IP']
                mac = dict['MAC']
                os = dict['OS']
                hostname = dict['Hostname']
                obj.AssetName = Assetname
                obj.IP = ip
                obj.MAC = mac
                obj.OS = os
                obj.Hostname = hostname
                obj.Status = True
                obj.LastUpdated = datetime.now()
                obj.updatefields(['AssetName', 'IP', 'MAC', 'OS', 'Hostname', 'Status', 'LastUpdated'])
            else:
                obj.Status = False
                obj.LastUpdated = datetime.now()
                obj.updatefields(['Status', 'LastUpdated'])
        except Exception as e:
            print(e)
        return
        
@method_decorator(csrf_exempt, name='dispatch')
class SubmitAllRequest(View):
    def post(self, request):
        lines = []
        count=1
        all_items = Response.objects.all()
        for item in all_items:
            print(f"Asset {count}\n")
            if item['Port'] is not None:
                port = 22
            else:
                port = item['Port']
            server = item['Server']
            username = item['Username']
            password = item['Password']
            dict = run_item(password, username, server, port)
            #TODO: check if error
            if dict['Status']=='UP':
                Assetname = dict['Asset_name'],
                ip = dict['IP']
                mac = dict['MAC']
                os = dict['OS']
                hostname = dict['Hostname']
                item.AssetName = Assetname
                item.IP = ip
                item.MAC = mac
                item.OS = os
                item.Hostname = hostname
                item.Status = True
                item.LastUpdated = datetime.now()
                item.updatefields(['AssetName', 'IP', 'MAC', 'OS', 'Hostname', 'Status', 'LastUpdated'])
            else:
                item.Status = False
                item.LastUpdated = datetime.now()
                item.updatefields(['Status', 'LastUpdated'])
            count=count+1
@method_decorator(csrf_exempt, name='dispatch')
class CreateResponse(View):
    def post(self, request):
        data = json.loads(request.body)
        server = data['server']
        username = data['username']
        password = data['password']
        port = data['port']
        try:
            Response.objects.create(Server=server, Username=username, Password=password, Port=port)
            return HttpResponse({"Status":"success"})
        except:
            return HttpResponse({"Status":"failed"})