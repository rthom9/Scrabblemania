import requests

url = "http://127.0.0.1:5000"
req = {"email": "thomrobert9@gmail.com",
       "subject": "Test Email",
       "content": "The email service is working!! Hurrah"}

test = requests.post(url, json=req)

print(test.text)