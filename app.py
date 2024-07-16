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

json_str = json.dumps(payload)
# ---------------------------------------------- FUNCOES  ---------------------------------------------- #

def main():
  
  parser = argparse.ArgumentParser(description='CLI para criação de Apps Profiles na plataforma Veracode')

  parser.add_argument('--app-name', required=True, dest='app_name', help='Application Name')
  parser.add_argument('-criticality',  dest='business_criticality', required=True, help='Business Criticality')
  parser.add_argument('--owner', required=True, dest='business_owner', help='Business Owner')
  parser.add_argument('--business-unit', required=True, dest='business_unit', help='Business Unit')
  parser.add_argument('--squad', required=True, dest='squad_responsavel', help='Squad')
  parser.add_argument('--product-owner', required=True, dest='product_owner', help='Product Owner')
  parser.add_argument('--possui-api', required=True, dest='possui_api', help='Possui API?')
  parser.add_argument('--exposed', required=True, dest='exposed_internet', help='Está exposto para Internet?')
  parser.add_argument('--description', required=True, dest='description', help='Breve Descrição do App')
  parser.add_argument('--policy', required=True, dest='policy', help='Política de segurança')
  parser.add_argument('--teams', required=True, dest='teams', help='Times responsáveis')

  args = parser.parse_args()

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

def createApp():
    pass

if __name__ == "__main__":

    main()
