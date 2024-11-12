# Beginner / Packet Pursuit: The Forensic Odyssey

Si revisamos el DNS encontramos un tráfico extraño

![dns](https://github.com/user-attachments/assets/ce4c8f39-9582-477c-b645-9de2037548c2)

Filtramos por los datos que estan justo antes de 'evildomain.com' y decodificamos cada pedazo en base64

`grep evil log.txt | awk '{print $10}'| awk -F. '{print $1}' | base64 -d`

`flag{f0r3ns1c_4rt_0f_exf1ltr4ti0n}`
