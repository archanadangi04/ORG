from datadog import initialize, api
import csv
import requests
import re
from params import organisations

path = "https://github.com/archanadangi04/ORG.git/datadog.csv"

deflist = [["datadog_organization","name","email","handle","is_admin","is_disabled","is_verified","role","access_role"]]
with open('orgnames.txt', 'r') as readFile:
    data = readFile.readlines()

for i in range(len(data)):
    data[i] = data[i].replace('\n','')

for i in data:
    orgvalue = organisations.get(i)
    api_key = orgvalue.get('api_key')
#    print(api_key)
    app_key = orgvalue.get('app_key')
#    print(app_key)
    url = "https://api.datadoghq.com/api/v1/org?api_key=%s&application_key=%s" %(api_key,app_key)
    resp = requests.get(url)
    raworgdetails = resp.content
    raworgdetails = raworgdetails.decode('utf-8')
#    print(raworgdetails)
    orgdetails = re.search(r'"name":(.+?")', raworgdetails)
#    print(orgdetails)
    orgname = orgdetails.group().split(':')[1].strip('"')
##    print(orgname)
    initialize(**orgvalue)
    rawdata = api.User.get_all()
#    print(rawdata)
    userlist = rawdata.get('users')
    list1 = []
    list1.append(orgname)
    for i in range(len(userlist)):
       for j in ("name","email","handle","is_admin","disabled","verified","role","access_role"):
          list1.append(userlist[i].get(j))
       deflist.append(list1)
       list1 = []
    print(deflist)
    with open(path, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(deflist)
    writeFile.close()
