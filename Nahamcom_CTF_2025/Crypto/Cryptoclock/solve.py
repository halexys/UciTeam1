import time
import random

# real timestamp is 1748044846

def generate_key(length: int, seed ) -> bytes:
    if seed is not None:
        random.seed(int(seed))
    return bytes(random.randint(0, 255) for _ in range(length))

def decrypt(data: bytes, key: bytes) -> bytes:
    """Encrypt data using XOR with the given key."""
    return bytes(a ^ b for a, b in zip(data, key))


flag = bytes.fromhex("63b2c857de9f3cbd0aac6c9a9439493e58e4500839a5f7e2f995b67350399bd4c351ad78cb6a")

current_time = int(time.time())
start_time = current_time - 86400 * 2 # 48 horas
for i in range(start_time, current_time + 1):
    key = generate_key(len(flag),i)
    plain_flag = decrypt(flag,key)
    if b"flag{" in plain_flag:
             print(f"REAL timestamp {i}")
             print(plain_flag)
             break
    if i % 10000 == 0:
            print(f"timestamp: {i}", end='\r')
