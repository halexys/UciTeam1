import requests
import string

payload=["_"]*32
guess={"guess": "flag{" + "".join(payload)+"}"}
x = requests.post('http://challenge.nahamcon.com:31582/guess',json=guess,headers={'Content-Type':'application/json'})
data = x.json()['result']
correct="🟩"

book = string.digits + string.ascii_lowercase
for i in range(32):
    for c in book:
        payload[i]=c
        guess={"guess": "flag{"+"".join(payload)+"}"}
        print(guess)
        x = requests.post('http://challenge.nahamcon.com:31582/guess',json=guess,headers={'Content-Type':'application/json'})
        response = x.json()['result']
        print(response)
        if response[i] == correct:
            break
print(guess)
