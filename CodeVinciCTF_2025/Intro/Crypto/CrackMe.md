# Crackme

Nos dan un grupo de hashes, los primeros son sha256 que parecen seguir el formato de la flag (probamos crackearlos en [crackstation](https://crackstation.net/))

![2025-03-30-220341_1335x539_scrot](https://github.com/user-attachments/assets/bd8b38c0-82d0-4335-a49d-f88c0bd920f9)

Probamos por ejemplo obtener el hash sha256 de "CodeVinciCTF{"
```
echo -n "CodeVinciCTF{" | sha256sum
01c968e9652748cf37b711d515a401d51b566809c57a5d843094c458bc6231a8  -
```

Coincide con el 13-imo hash, aqui nos percatamos de que podemos ir probando el siguiente caracter por fuerza bruta desde este hash hasta el ultimo, que eventualmente será la flag:

``` python
import string
import hashlib

hashes = [
    "01c968e9652748cf37b711d515a401d51b566809c57a5d843094c458bc6231a8",
    "4eeff9a9bc18d1b2176bfa5f64b0f460267a612dc908d0043999c9cde2b41faa",
    "147d01bf5af81bae4a5a9184e4c4e8ec9f2a0928d0a0d2a76f7144bcbea54f1a",
    "67a40b5f9d967594b8713c8614d55caeba3b1f5666a210cca6dda7ab6d27be1f",
    "b913c0d40b1ede702ee0b745f44140558982bb77697342a90de32a86b3129031",
    "ee432c331a08f42077c78907dbbc7fc2a423430805984a1f9dc44a74fbaad1ca",
    "eebf91be160e598893f8899f48f21aa0442844961aebb9573e4b041e6147fca4",
    "39d3e1b91f24fb54e2225d199242a2aae00bb202e08b2f1871c9da0653a12ee9",
    "edbe94a924ddaecb1760874ecd452bf67bcfecc6ce7ef6c4858432644371b545",
    "560c03aea4b9cb0e21ce7b5e1f74db3db95b3f7ed20436e5e7f378d8827e6f54",
    "edf52322484f8ccab4563e30acc4a68a5f22dd193d946043d95d85fb66e60569",
    "d966a627ec71e423b3d6c48b84a4226127555a90733bc70e75d81a1e1a3689be",
    "a2aaa7ea01732b49595a3f105fd9b44e1557b94dd0c935a07acfdd921af4be59",
    "5e0b298b4543760a3dabc83fed77f7c2549617bf35c4fc445c8943ee89c1a41f",
    "c04220a3ca084ce2d917ea726580ab0b890bd42a7aa54f1ef8d156d88360fdcd",
    "c91f6e7027ee0367e6775fbe2ba4d2af4a9bdb7ee0ae9d9c8a6507a20eb728e9",
    "c4609be515ddfa7711db83465899a12d36e04e113069d020f4da0fcd3e3fbe17",
    "94900549c3861db3b1cf9e02eb2fe01169683a0f420080d89f8e2426f92ebe6b",
    "4ec3c7a709dc3a184bba510554f75bd2ecba826d619b45b75cf914bf5aebfdff",
    "d7369b0b255c854b38ec14886853e84fa216989539d55d340f2c533832d7f395",
    "48ed85cf77afb31c706b9caa1c4dba8f163394191450dceda5fdefaf1dd2735c",
    "1ef5ba497c9b198b22599146f2321b6d155c81ec91ba0f53ef3f36667ab7b70e",
    "3823c5eff483e56bde21373559d2aa6edd477c6b2c1faa1a0bd9fbd293973319",
    "9e9db79613780f36a1d7bd880a0d11edb863ac94d6088f358e8c5fba11acedab",
    "5bcf4344a577dfef3f2cf58301bc292aa24ef372ccac10e4d43abae05e83cee7",
    "02fa4e418677b63367ad5d5fb5736b66b8d31611df2517929515c9af5ed295e1",
    "64bd2813e6f26a1244f6cb4d61c79741cbe083684edb857ae44029e0528e1522",
    "23b8f34fad37b46e85a0d90a34b17beee368fe72f9631213d2c2a6390a27624a",
    "3b631a824708b4c6a012cd7d4007768a8d357ec4eda38a0aa0a284814c377d90",
    "99d694775673a922492681c199099e3d8cd1c75c78e04f8eea92a2860c60cc03",
    "09b22af8a62a9f86bfe33e05b2ac0bcf4c6b66bb915a0c5e895f87aabe21d71a",
    "3c8feb97225482ba84acf548ba8410452cce3659e9c958230ff3ef1701b52f8b",
    "c9515fd46a74765616ca1e1111e3aa3bb250cab2ba164a9d8392fb9d34385b53",
    "9ccc4a3fa59a60f496f614c50db2d9adbe3bb65384e28a729da183dea7cecded",
    "b692e7a5563fc45350448e6b9d97610b8ab257cdeb0b6387c91fe35500768dfd",
    "38b7d869b8792fc3be1a567910b200e6751e5538c455f523b254e4249dbae9e8",
    "38e98eea1bbd93b1ae202a92af4744fea4ea137d895d626e4b0ee285d77c4c9b",
    "7ab8d2f64680ee73ebf3b970f53731cd01cd13b86869b8d51a0934ef5cdfe680",
    "ab0cc0cbb5cf27480f603054ffd9dcf0acf11ccb799ce545697cc2ac0987929c",
    "f1c0a68803e49066a925c250d71ca5a5c9ea8062bffc72198b04a1d481b77e62",
    "b79b777a05c2a302167ed8e6152a7517331019c0507ea3a8e7a3e1faa8f77487",
    "541eaf08cda549a338d0fc6430bc7de77a7cc38332f4017ed7f80ab689ac002c",
    "5416617fe88d923118395a349c832c72fa678f4874deeae506c9b2a7b5b3695b"
]

book = string.printable
flag="CodeVinciCTF{"

for h in hashes:
    for c in book:
        hash = hashlib.sha256((flag+c).encode()).hexdigest()
        if hash == h:
           flag += c
           break

print(flag)
```

`CodeVinciCTF{bruteforced_like_bike_keylock_pins_0e3cw7}`
