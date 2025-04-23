# Snaeky

Debiamos hacerle ingenieria inversa a un juego del snake para GBA, para la tarea necesitamos un emulador con herramientas de depuracion como mGBA o bgb

![2025-04-06-193006_640x695_scrot](https://github.com/user-attachments/assets/5cbd6d37-f38e-4576-b659-328e02b91d44)

Lo primero que hacemos es ver si podemos encontrar el contador de puntos, podemos usar la herramienta `Tools/Game state views/ Search Memory...`

Comenzamos con el valor en 0 y actualizamos hasta encontrar el/los bytes que cambian a medida que obtenemos puntos

Aqui podemos ver que la direccion `0xc313` cambia:

![2025-04-06-192147_1352x713_scrot](https://github.com/user-attachments/assets/5444008d-4752-4223-adb7-8b44a9757fa1)

Si usamos la herramienta `Tools/Game state views/ View Memory...` y vamos a la direccion especificada podemos cambiarla a un numero grande, maximo 127:

![2025-04-06-181125_1351x708_scrot](https://github.com/user-attachments/assets/91287afb-2968-4c75-8b0f-698056bbe2e2)

Si capturamos la comida con un puntuaje alto, nos genera un corazon en la esquina superior izquierda del mapa:

![2025-04-06-181136_1351x716_scrot](https://github.com/user-attachments/assets/bfffac6b-a7ea-4ac0-b618-869800496907)

No podemos acceder a esa posicion sin colisionar, pero si probamos el juego multiples veces mirando a direcciones cercanas a la del puntuaje podemos percatarnos que (`0xc306`,`0xc307`) son las coordenadas de la cabeza de la serpiente y (`0xc30b`,`0xc30c`) son las coordenadas de la comida

Si cambiamos las coordenadas de la comida a una posicion a la que alcancemos con la serpiente el juego comprueba que se esta colisionando con la comida y nos suelta el mensaje de victoria:

![2025-04-06-181158_1353x720_scrot](https://github.com/user-attachments/assets/d92214db-be8d-400d-834f-d22bb5f8db84)

![2025-04-06-181438_1350x703_scrot](https://github.com/user-attachments/assets/56127d32-2eab-42bd-abbf-e74422d6177d)

`Breach{M0M-1-H4CK3D-5N4K3}`



