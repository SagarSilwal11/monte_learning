import requests

url = 'https://montessori.website/common/gettoken/'
data = {
    'username': 'admin',
    'password': 'admin'
}

response = requests.post(url, json=data, verify="/Users/sagarsilwal/certs/montessori.website+2.pem")

print(response.status_code)
print(response.json())