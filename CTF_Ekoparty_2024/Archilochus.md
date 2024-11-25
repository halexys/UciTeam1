Tenemos un texto en griego antiguo supuestamente, pero traducirlo o buscar informacion en https://lexilogos.com no llevó a nada

```
>> cat archilochus.papyrus 
ἔιιεο λον,ἰυτειι δρη κ ὅέανμαατν  ο ὐιαεπυγτ ιίρ οῷἃ.νόεῦ   ακλντμτιλλ οὴο ηητύ  ησνοτομ ηιύῳἶόσ,κτ δνη άοσαομκ υο  αρε φοπίάκγώὐοατοετδυ η{ εὲ γσβσρ ξιέεμοοέα σιςἴρ ττκ οωαη_ρεμ υνεῷἶαστ κ νιίήφοτα γνί}
```

Para resolver el reto hay que usar una escítala, por ejemplo en https://www.dcode.fr/scytale-cipher, y hacer fuerza bruta. En 33x7 podemos encontrar la flag

![flag3](https://github.com/user-attachments/assets/8629abc1-8d77-4118-98cc-5f28cb6c82c0)

Hay que transcribirlo de griego antiguo a latin en mayusculas, podemos hacer eso con https://www.lexilogos.com/keyboard/greek_conversion.htm

![lexi](https://github.com/user-attachments/assets/0bbe30de-4501-4081-a1ed-9a4146af56c5)

`EKO{BEST_EKO}`
