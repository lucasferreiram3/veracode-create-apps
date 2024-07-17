## descrição

Script Python que auxilia na criação de perfis de aplicações na plataforma Veracode, atribuindo campos personalizados

## setup

clone o repositorio:
```
git clone https://github.com/lucasferreiram3/veracode-create-apps.git
```
Instale as depedências:
```
cd veracode-create-apps
pip install -r requeriments.txt

```
configure suas credenciais API da Veracode no ~/.veracode/credentials ou C:\\Users\user\.veracode\credentials
```
[default]
veracode_api_key_id = <YOUR_API_KEY_ID>
veracode_api_key_secret = <YOUR_API_KEY_SECRET>
```

## run
```
python3 app.py
```