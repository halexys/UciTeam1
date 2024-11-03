# Forensic / Lsass crackdown

Tenemos un Mini DuMP crash report (DUMP). Obtenemos su informacion con pypykatz:

![dump](https://github.com/user-attachments/assets/a5da861c-5d90-4770-af45-c8a612c89ffc)

Encontramos el hash NTLM del usuario 'Consortium' dentro del dump y lo crackeamos con https://crackstation.net/

![nt](https://github.com/user-attachments/assets/3ae7c0fa-d2cc-4ed9-baff-0160614eccfc)

![crack](https://github.com/user-attachments/assets/13b7e09a-927f-4222-8769-0086582d0a1d)

`NICC{1987evilovekoen}`
