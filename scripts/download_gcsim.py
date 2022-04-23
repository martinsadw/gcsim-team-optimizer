import requests
import sys

api_response = requests.get('https://api.github.com/repos/genshinsim/gcsim/releases/latest')
if api_response.status_code != 200:
    sys.exit(1)

api_data = api_response.json()
asset_uri = api_data['assets'][0]['browser_download_url']

asset_response = requests.get(asset_uri)
if asset_response.status_code != 200:
    sys.exit(1)

with open('./gcsim.exe', 'wb') as f:
    f.write(asset_response.content)
