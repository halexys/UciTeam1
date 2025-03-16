# Granny's Gift

Recibimos un script de python y una imagen png de un collar. La imagen nos es irrelevante. La flag esta encriptada en AES-CBC con la clave privada KEY y se nos solicita ingresar un secretocuyo hash sha256 sea igual a KEY.
``` python
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64

KEY = "8f149350416bf5a318c91a4072b4c44fe32ec03d5571412ab0dcfc6cb366574e"
FLAG = "3vQmUeUhdaV39wLvJf2OjwFLnUfx4KhGWcx/gyOnlX4lVIsRf6lAeQCCt7rp4fsCZ7iuVyfW09G7dbNEn8+MEuWzG1HbUTyILGzFGHUw6xo="

class Cipher:
    def encrypt(self, plainText, key):
        iv = os.urandom(16)
        privateKey = hashlib.sha256(key.encode("utf-8")).digest()
        cipher = AES.new(privateKey, AES.MODE_CBC, iv)
        encryptedBytes = cipher.encrypt(pad(plainText.encode(), AES.block_size))
        return base64.b64encode(iv + encryptedBytes).decode()

    def decrypt(self, encrypted, key):
        encryptedData = base64.b64decode(encrypted)
        iv = encryptedData[:16]
        privateKey = hashlib.sha256(key.encode("utf-8")).digest()
        cipher = AES.new(privateKey, AES.MODE_CBC, iv)
        try:
            decryptedBytes = unpad(cipher.decrypt(encryptedData[16:]), AES.block_size)
        except:
            exit("Decryption error")
        return decryptedBytes.decode()



pwd = input("\nI swear there's nothing in here!\nGranny's super-secret secret:   ")
h = hashlib.new('sha256')
h.update(pwd.lower().encode())
if h.hexdigest() == KEY:
    cipher = Cipher()
    print("\nI always knew you were the smartest grandchild!")
    #print(cipher.decrypt(FLAG,pwd.lower()))
    print(cipher.decrypt(FLAG,pwd.lower()))
else:
    print("\nI told you, but you wouldn't listen!")
```

``` bash
> python3 whatisthis.py

I swear there's nothing in here!
Granny's super-secret secret:   keychain

I told you, but you wouldn't listen!
```

Al final si vemos que se usa para decodificar la FLAG los bytes del hash de nuestra entrada, que debe ser igual a KEY, luego, si es correcta, la funcion decrypt toma la cadena que introducimos, le calcula el hexdump del hash sha256, lo convierte a bytes y lo usa para descifrar. Ahora bien si ya poseemos KEY en formato hexadecimal podemos convertirlo directamente a bytes y usarlo en decrypt para decodificar la flag.

``` python
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64

KEY = "8f149350416bf5a318c91a4072b4c44fe32ec03d5571412ab0dcfc6cb366574e"
FLAG = "3vQmUeUhdaV39wLvJf2OjwFLnUfx4KhGWcx/gyOnlX4lVIsRf6lAeQCCt7rp4fsCZ7iuVyfW09G7dbNEn8+MEuWzG1HbUTyILGzFGHUw6xo="

class Cipher:
    def encrypt(self, plainText, key):
        iv = os.urandom(16) 
        privateKey = hashlib.sha256(key.encode("utf-8")).digest() 
        cipher = AES.new(privateKey, AES.MODE_CBC, iv)
        encryptedBytes = cipher.encrypt(pad(plainText.encode(), AES.block_size))  
        return base64.b64encode(iv + encryptedBytes).decode()

    def decrypt(self, encrypted, key):
        encryptedData = base64.b64decode(encrypted) 
        iv = encryptedData[:16] 
        #privateKey = hashlib.sha256(key.encode("utf-8")).digest())
        cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, iv)  # Aqui usamos los bytes de KEY para descifrar la FLAG
        try:
            decryptedBytes = unpad(cipher.decrypt(encryptedData[16:]), AES.block_size)  
        except:
            exit("Decryption error")
        return decryptedBytes.decode()



pwd = input("\nI swear there's nothing in here!\nGranny's super-secret secret:   ")
h = hashlib.new('sha256')
h.update(pwd.lower().encode())
# Cambiamos aqui la condicion
if h.hexdigest() != KEY:
    cipher = Cipher()
    print("\nI always knew you were the smartest grandchild!")
    #print(cipher.decrypt(FLAG,pwd.lower()))
    print(KEY.encode())
    # Pasamos KEY como parametro en lugar de la entrada
    print(cipher.decrypt(FLAG,KEY))
else:
    print("\nI told you, but you wouldn't listen!")
``` 

``` bash
> python3 whatisthis.py

I swear there's nothing in here!
Granny's super-secret secret:   cualquiercosa

I always knew you were the smartest grandchild!
b'8f149350416bf5a318c91a4072b4c44fe32ec03d5571412ab0dcfc6cb366574e'
KSUS{W3_us3d_t0_s3nd_th3s3_w1th_p1g30ns_4t_my_t1m3_y0u_kn0w}
```

`KSUS{W3_us3d_t0_s3nd_th3s3_w1th_p1g30ns_4t_my_t1m3_y0u_kn0w}`
