# Misc / Git 2: Github Actions

Necesitamos hacer una peticion a https://actions.ctf.cert.unlp.edu.ar/ desde un endpoint dentro de la red de Github Actions. Creamos un repositorio y en el la ruta .github/workflows/ci.yaml

El archivo ci.yaml luciria al final algo asi:

``` yaml
name: CI Workflow

on:
  push:
    branches:
      - main

jobs:
  call-action:
    runs-on: ubuntu-latest
    
    steps:
      - name: Check out the repository
        uses: actions/checkout@v2

      - name: Make a request to the specified URL
        id: request
        run: |
          response=$(curl -s -w "%{http_code}" -o response.txt -H "Content-Type: application/json" -H "X-CERTUNLP: flag" https://actions.ctf.cert.unlp.edu.ar/)
          echo "HTTP Status Code: $response"
          echo "Response Body:"
          cat response.txt

      - name: Display response
        run: |
          echo "Response from the URL:"
          cat response.txt
```

Se puede notar que contiene las cabeceras  "Content-Type: application/json" y "X-CERTUNLP: flag", pues el servidor respondio en el primer y segundo intento que necesitaba esas cabeceras con esos valores. Actualizamos el repositorio y revisamos la accion:

![callaction](https://github.com/user-attachments/assets/4077ec43-05a1-4abb-ab83-47cb280e21cb)

`flag{gh_act10n5_unlock_secrets}`



