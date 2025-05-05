#!/usr/local/bin/python3
import random

P = [15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24]

# Construir permutación inversa
P_inv = [0] * len(P)
for i, p in enumerate(P):
    P_inv[p] = i

def unshuffle(l):
    return [l[p] for p in P_inv]

def decrypt(ct_hex):
    try:
        ct = bytes.fromhex(ct_hex)
    except ValueError:
        print(f"Invalid hex string: {ct_hex}")
        return None
    
    # Rango posible para la suma S (32*32 a 125*32)
    min_S = 32 * 32
    max_S = 125 * 32
    
    for S in range(min_S, max_S + 1):
        # Encontrar el padding correcto
        random.seed(S)
        key = random.randbytes(len(ct))
        l = bytes([ct[i] ^ key[i] for i in range(len(ct))])
        
        if sum(l) == S:
            # Deshacer el shuffle
            unshuffled = unshuffle(list(l))
            
            # Convertir a string
            try:
                decrypted = ''.join([chr(b) for b in unshuffled])
                if decrypted.startswith("UVT{"):
                    flag_len = decrypted.find("}") + 1 if "}" in decrypted else 32
                    return decrypted[:flag_len]
            except:
                continue
    return None

ct_hex = "252acb5f5b560b6344ab6c2421410eca06b63acb621edf0421f1423a18920208"
flag = decrypt(ct_hex)
print(flag)
