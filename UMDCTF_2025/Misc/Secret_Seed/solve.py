import random
import time

def recover_seed(known_keystream, max_time_diff=3600):
    current_time = int(time.time())
    for possible_seed in range(current_time - max_time_diff, current_time + 1):
        random.seed(possible_seed)
        generated_keystream = bytes([random.getrandbits(8) for _ in range(len(known_keystream))])
        if generated_keystream == known_keystream:
            return possible_seed
    return None


with open("secret.bin", "rb") as f:
     cipher = f.read()
     part = b"UMDCTF{"
     part_key = bytes([cipher[i] ^ part[i] for i in range(len(part))])
     seed = recover_seed(part_key,400000)
     assert seed != None
     print("Seed:",seed)
     if seed:
        random.seed(seed)
        keystream_full = bytes([random.getrandbits(8) for _ in range(len(cipher))])
        plaintext = bytes([c ^ k for c, k in zip(cipher, keystream_full)])
        print(plaintext.decode())
