from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import Applications 
from veracode_api_py import Policies
from veracode_api_py import BusinessUnits
from veracode_api_py import Teams
import requests
import json
import sys

# ---------------------------------------------- VARIAVEIS  ---------------------------------------------- #

api_base = "https://api.veracode.com/appsec/v1"
headers = {"User-Agent": "Python HMAC Example"}
appName = ''
criticality = ''
businessUnit = ''
ownerName = ''
ownerEmail = ''
customFields = []
squad = ''
lider = ''
po = ''
possuiApi = ''
exposed = ''
description = ''
policy = ''
teams = []
app_profiles = []

# ---------------------------------------------- FUNCAO PRINCIPAL  ---------------------------------------------- #

def main():

  appName = input('Nome da aplicação: ')
  criticality = input('Criticidade para o negócio: ')
  policy = input('Indique a Policy: ')
  businessUnit = input('Business Unit: ')

  while True:
      t = input('Indique os Teams/Squad ou q para sair: ')
      if t == 'q':
          break
      teams.append(t)
  
  ownerName = input('Nome do Business Onwer')
  ownerEmail = input('Email do Business Onwer')
  
  while True:
    print('Indique os valores dos Custom Fields\n')
    squad = input('Squad Responsável: ')
    customFields.append(squad)
    lider = input('Líder Técnico: ')
    customFields.append(lider)
    po = input('Product Owner: ')
    customFields.append(po)
    possuiApi = input('Possui API? (Sim ou Não): ')
    customFields.append(possuiApi)
    exposed =  input('Sofre exposição à internet? (Sim ou Não): ')
    customFields.append(exposed)
    break

  createApp(appName, criticality, businessUnit, teams, policy, customFields, ownerName, ownerEmail)

# ---------------------------------------------- FUNCOES  ---------------------------------------------- #

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
  bu_name = ''
  bu_id = ''
  for i in data:
    bu_name = i["bu_name"]
    bu_id = i["bu_id"]

    # bu informada existe na plataforma?
    if b == bu_name:
        return bu_id
    else:
        return f'{bu_name} não existe'

# Retorna o GUID dos times informados
def getTeamsGuid(t):
    data = Teams().get_all(t)
    team_id = []
    
    for i in data:
      team_id.append(i["team_id"])
    
    return team_id

# Retorna se o perfil de aplicação já existe na plataforma      
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
