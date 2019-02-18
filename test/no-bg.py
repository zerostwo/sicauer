import requests

headers = {
    'X-API-Key': 'Tjwhka8aV8UMjQRyUtjgd7ti',
}

files = {
    'image_file': ('./201700193.jpg', open('./201700193.jpg', 'rb')),
}

response = requests.post('https://api.remove.bg/v1.0/removebg', headers=headers, files=files)
with open('./picture.jpg', 'wb') as file:
    file.write(response.content)
