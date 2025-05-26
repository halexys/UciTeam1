# DeflationGangster

El zip contiene una cadena en base64, con este one-liner se extrae la flag: `strings -n 36 gangster.zip | tr -d ";" | base64 -d`
