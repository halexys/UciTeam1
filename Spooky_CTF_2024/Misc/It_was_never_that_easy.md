# Misc / It was never that easy

Tenemos un pcapng capture file, usamos capinfos para imprimir informacion de la captura y al final de la seccion de comentarios se encuentra una cadena en base64:

![line](https://github.com/user-attachments/assets/680cb530-8b27-4fa1-973d-12919b93ee26)

Borramos los espacios y la decodificamos con `echo "TklDQ3tkM3ZpbF9rbjB3c19oMHdfdDBfaDFkM190aDFuZ3N9" | base64 -d` o https://cyberchef.io:

![finalpcap](https://github.com/user-attachments/assets/9a018951-a15b-4dff-b0a6-84726d587959)

`NICC{d3vil_kn0ws_h0w_t0_h1d3_th1ngs}`
