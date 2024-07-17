from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import Applications 
from veracode_api_py import Policies
from veracode_api_py import BusinessUnits
from veracode_api_py import Teams
import requests
import json
import sys
import argparse

# ---------------------------------------------- VARIAVEIS  ---------------------------------------------- #

api_base = "https://api.veracode.com/appsec/v1"
headers = {"User-Agent": "Python HMAC Example"}
appName = ''
criticality = ''
businessUnit = ''
ownerName = ''
ownerEmail = ''
custom_fields = []
squad = ''
lider = ''
po = ''
possuiApi = ''
exposed = ''
description = ''
policy = ''
teams = []
teams_default = ['Showroom_Lucas', 'Showroom Pré-Vendas']
bu_name = ''
bu_id = ''
app_profiles = []
#default_policy = 'Veracode Recommended Low'

# ---------------------------------------------- FUNCOES  ---------------------------------------------- #

def main():

  appName = input('Nome da aplicação: ')
  criticality = input('Criticidade para o negócio: ')
  businessUnit = input('Business Unit: ')

  while True:
      t = input('Indique os Teams ou q para sair: ')
      if t == 'q':
          break
      teams.append(t)
      
  policy = input('Indique a Policy: ')

def createApp(appName, criticality, businessUnit, teams, policy, custom_fields, ownerName, ownerEmail):
    Applications.create(app_name=appName, business_criticality=criticality, business_unit=getAppGuid(businessUnit), teams=getTeamsGuid(teams), policy_guid=getPolicyGuid(policy), custom_fields=custom_fields, bus_owner_name=ownerName, bus_owner_email=ownerEmail)

# Retorna o GUID da política
def getPolicyGuid(p):
    data = Policies.get_all(p)
    for i in data:
        if i["name"] == p:
            return i["guid"]

# Retorna o GUID da Business Unit
def getBuGuid(b):
  data = BusinessUnits().get_all()
  for i in data:
    bu_name = i["bu_name"]
    bu_id = i["bu_id"]

    # bu informada existe na plataforma?
    if b == bu_name:
        return bu_id
    else:
        return f'{bu_name} não existe'

# Retorna o GUID dos times
def getTeamsGuid(t):
    data = Teams().get_all(t)
    team_id = []
    
    for i in data:
      team_id.append(i["team_id"])
    
    return team_id

# Retorna o perfil de aplicação já existe na plataforma      
def checkAppProfile(appName):
    try:
        response = requests.get(api_base + "/applications", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)

    if response.ok:
        data = response.json()
        for app in data["_embedded"]["applications"]:
            app_profiles.append(app["profile"]["name"])

        for i in app_profiles:
            if appName in app_profiles:
                print("App profile já existe na plataforma")
                print(f'App: [{appName}] | GUID: [{getAppGuid(appName)}]')
                break
            else:
                print("App profile não existe na plataforma\n")
                break
    else:
        print(response.status_code)

# Retorna o GUID do app
def getAppGuid(a):
    try:
        response = requests.get(api_base + f"/applications?name={a}", auth=RequestsAuthPluginVeracodeHMAC(), headers=headers)
    except requests.RequestException as e:
        print("Whoops!")
        print(e)
        sys.exit(1)

    if response.ok:
        data = response.json()
        for app in data["_embedded"]["applications"]:
           return app["profile"]["business_unit"]["guid"]
    else:
        print(response.status_code)

# ---------------------------------------------- EXECUCAO  ---------------------------------------------- #

if __name__ == "__main__":

    main()
