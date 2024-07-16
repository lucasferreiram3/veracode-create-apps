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
appName = "verademo-dotnetcore"
criticality = ''
business_unit = 'M3_Prevendas'
owner = 'example@exe.com.br'
custom_fields = []
squad = ''
lider = ''
po = ''
possui_api = ''
exposed = ''
description = ''
policy = ''
teams = ''
app_profiles = []
guid_profiles = []
default_policy = 'Veracode Recommended Low'
teams_default = ['Showroom_Lucas', 'Showroom Pré-Vendas']

#default_policy = 'CIP Medium + SCA'
#teams_default = ["DevSecOps", "CDE Projetos e Arquitetura de Segurança", "API-Services", "Auditoria Interna", "Cyber Security"]
#business_unit = 'SAP'

# ---------------------------------------------- PAYLOAD  ---------------------------------------------- #

payload = {
    "guid": "string",
    "id": 0,
    "oid": 0,
    "organization_id": 0,
    "profile": {
      "name": f"{appName}",
      "business_criticality": f"{criticality}",
      "business_owners": [
        {
          "email": f"{owner}",
          "name": f"{owner}"
        }
      ],
      "business_unit": {
        "guid": f"{business_unit}"
      },
      "custom_field_values": [
        {
          "app_custom_field_name": {
            "name": "custom_field",
            "organization_id": 0,
            "sort_order": 0
          },
          "field_name_id": 0,
          "id": 0,
          "value": "string"
        }
      ],
      "custom_fields": [
        {
          "name": "Squad Responsável",
          "value": f"{squad}"
        },
        {
            "name": "Líder Técnico",
            "value": f"{lider}"
        },
        {
            "name": "Product Owner",
            "value": f"{po}"
        },
        {
            "name": "Possui API? (Sim ou Não)",
            "value": f"{possui_api}"
        },
        {
            "name": "Sofre exposição à internet” (Sim ou Não)",
            "value": f"{exposed}"
        }
      ],
      "description": f"{description}",
      "name": "string",
      "policies": [
        {
          "guid": f"{policy}",
          "is_default": "true"
        }
      ],
      "settings": {
        "dynamic_scan_approval_not_required": "false",
        "nextday_consultation_allowed": "true",
        "sca_enabled": "true",
        "static_scan_dependencies_allowed": "true"
      },
      "tags": "string",
      "teams": [
        {
          "guid": f"{teams}"
        }
      ]
    },
    "scans": [
      {
        "internal_status": "string",
        "status": "CREATED"
      }
    ]
}
# ---------------------------------------------- FUNCOES  ---------------------------------------------- #

def main():

    #checkAppProfile(appName)
    print(getAppGuid(appName))
    print(getPolicyGuid(default_policy))
    print(getBuGuid(business_unit))

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
        if i["bu_name"] == "M3_PreVendas":
            return i["bu_id"]

# Retorna o GUID dos times
def getTeamsGuid(t):
    data = Teams().get_all(teams_default)
    for i in data:
        if i["team_name"] in teams_default:
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
