# Misc / PGN_Encryption

De https://lichess.org/study/3Ky6Iam8 podemos ver el PGN (Portable Game Notation) del caso de estudio, el titulo de la pagina es 'WintrCat'. Buscamos eso en google y obtenemos un repositorio (https://github.com/WintrCat/chessencryption)

![chess1](https://github.com/user-attachments/assets/f297378f-1488-46eb-9df2-83c2a2f6bd9c)

Clonamos el repositorio o simplemente descargamos los archivos decode.py y utils.py. Usamos el PGN de la URL que nos dan como argumento para la funcion 'decode' en decode.py, o sea, añadimos estas lineas a decode.py:

``` python
string = "1. f3 f6 2. g3 h5 3. g4 Rh6 4. gxh5 g6 5. f4 b6 6. Kf2 Rh8 7. Nf3 Rh6 8. Ke3 Na6 9. Kd4 Rb8 10. Ne5 Rh8 11. Kc3 Rxh5 12. Bh3 Rf5 13. Kc4 d6 14. Nc3 Rxe5 15. Bg4 Re3 16. Bf5 Re6 17. e4 Bb7 18. d3 Rc8 19. Be3 Qd7 20. Nb5 Kf7 21. Qh5 Ba8 22. Qh7+ Bg7 23. Nxc7 Re8 24. Rhg1 Kf8 25. Bc5 Rc8 26. Bxb6 Bb7 27. Ba5 Qb5+ 28. Kd4 Qe8 29. Rg3 Nh6 30. Nb5"
print(decode(string,"output.txt"))
```

Lo ejecutamos y obtenemos la flag:

```
python3 decode.py 
successfully decoded pgn with 1 game(s), 59 total move(s)(0.013s).
None
cat output.txt 
flag{Faustino_Oro_Our_Carlsen}
```

`flag{Faustino_Oro_Our_Carlsen}`
