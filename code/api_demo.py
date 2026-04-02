import requests

response = requests.get(
    'https://oim.108122.xyz/words/random',
    headers={'x-token': 'RobRob'},
)
print(response.json())