# Network / UH HA HA

Recibimos un archivo de captura

![Captura de pantalla de 2024-10-16 16-33-38](https://github.com/user-attachments/assets/748137bb-2d20-40ba-8a77-019ce46bf5d0)

Abrimos la traza con Wireshark y observamos el envío de dos archivos por FTP, un archivo 7-zip y una imagen PNG

![p3](https://github.com/user-attachments/assets/e47c7197-5273-4f69-a262-f87b7d1ecfb2)

Vamos a Archivos/Exportar Objetos/FTP-DATA... para obtenerlos. Vemos que r2.7z esta protegido por contraseña y la imagen muestra un codigo

![p4](https://github.com/user-attachments/assets/f8019c04-b873-46d1-9272-e84c7151ac91)
![r3](https://github.com/user-attachments/assets/7a5dcfe6-f49c-4f16-89c8-4eeca20ee4c8)

Usamos el número de la imagen para  abrir el 7-zip y encontramos la flag

![pf](https://github.com/user-attachments/assets/76c47f5e-c97e-4b07-b39d-71286339d38b)

`flagmx{cuv4v3}`
