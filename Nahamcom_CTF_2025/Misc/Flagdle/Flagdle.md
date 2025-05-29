# Flagdle

![2025-05-25-172119_874x452_scrot](https://github.com/user-attachments/assets/5989208e-43b6-429b-a6c4-e22c1523c590)

Hacemos la peticion como nos especifican, usamos fuerza bruta hasta hallar la flag completa con este script:
```python
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
```
