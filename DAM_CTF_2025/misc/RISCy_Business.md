# RISCy Business

Encontramos la string "dam{" que esta siendo referenciada en la funcion `build_flag_task`:

![2025-05-12-211806_708x133_scrot](https://github.com/user-attachments/assets/53246671-1130-479f-93d0-8c84c7bded92)

En la funcion podemos ver uso de otras cadenas como "_on_the_" y "esp32c6"

![2025-05-12-211510_288x569_scrot](https://github.com/user-attachments/assets/91f83b52-bbf1-4342-8c12-cf7c74e721b7)

![2025-05-12-211806_708x133_scrot](https://github.com/user-attachments/assets/fff8a311-2c9a-48b4-9ab9-fb22d61aead9)

Asumimos que esta reconstruyendo la flag y quedaria

"dam{" + sharedString + "_on_the_" + "esp32c6"

`sharedString` es un array sin inicializar de 16 caracteres. Hay referencias a este en la funcion "esp_zb_app_signal_handler", donde se inicializa concatenando 4 strings: "Fr33" "R705" "_51_" "C001"

![2025-05-12-212535_1347x403_scrot](https://github.com/user-attachments/assets/7df12f89-1de4-464a-b455-f62a24b99ddf)

`dam{Fr33R705_51_C001_on_the_esp32c6}`
