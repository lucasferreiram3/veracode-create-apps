from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import Applications 
from veracode_api_py import Policies
from veracode_api_py import BusinessUnits
from veracode_api_py import Teams
import requests
import json
import sys

# ---------------------------------------------- VARIAVEIS  ---------------------------------------------- #
appName = "verademo-dotnetcore"
api_base = "https://api.veracode.com/appsec/v1"
headers = {"User-Agent": "Python HMAC Example"}
policy = ''
app_profiles = []
guid_profiles = []
default_policy = ['Veracode Recommended Low', 'Veracode Recomended Medium', 'Veracode Recomended High']
#teams_default = ["DevSecOps", "CDE Projetos e Arquitetura de Segurança", "API-Services", "Auditoria Interna", "Cyber Security"]
business_unit = 'M3_PreVendas'
teams_default = ['Showroom_Lucas', 'Showroom Pré-Vendas']
squad = ''
lider = ''
po = ''
possui_api = ['yes', 'no']
exposed = ['yes', 'no']
owner = 'example@exe.com.br'
custom_fields = []

# ---------------------------------------------- FUNCOES  ---------------------------------------------- #

def main():
    #getPolicyGuid('Veracode Recommended Low')
    #getBuGuid(business_unit)
    #getTeamsGuid('Showroom_Lucas')
    checkAppProfile(appName)
    #print(getAppGuid(appName))

# Retorna o GUID da política
def getPolicyGuid(p):
    data = Policies.get_all(policy)
    for i in data:
        if i["name"] == "Veracode Recommended Low":
            #print(f'{i["name"]} : {i["guid"]}')
            return i["guid"]

# Retorna o GUID da Business Unit
def getBuGuid(b):
    data = BusinessUnits().get_all()
    for i in data:
        if i["bu_name"] == "M3_PreVendas":
            #print(f'{i["bu_name"]} : {i["bu_id"]}')
            return i["bu_id"]

# Retorna o GUID dos times
def getTeamsGuid(t):
    data = Teams().get_all(teams_default)
    for i in data:
        if i["team_name"] in teams_default:
            #print(f'{i["team_name"]} : {i["team_id"]}')
            return i["team_id"]
        
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

if __name__ == "__main__":

    main()
