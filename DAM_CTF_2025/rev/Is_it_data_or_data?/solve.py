from pwn import *

#p = process('./chall')
p = remote("isitdata.chals.damctf.xyz",39531)

# Token sequence to build "inagalaxyfarfaraway"
sequences = [
    (4, 6),        # i
    (10, 6, 5, 5), # n
    (7,),          # a
    # g is automatically added after the 7th token
    (7,),          # a
    (10, 5),       # l
    (7,),          # a
    (9, 5, 5),     # x
    (9, 5),        # y
    (4,),          # f
    (7,),          # a
    (10, 6, 6, 5), # r
    (4,),          # f
    (7,),          # a
    (10, 6, 6, 5), # r
    (7,),          # a
    (9, 5, 5, 5),  # w
    (7,),          # a
    (9, 5)         # y
]

for seq in sequences:
    for token in seq:
        p.sendlineafter(b'> ', str(token).encode())

p.interactive()
# Test
#p.sendlineafter(b'> ', b'00111111')
