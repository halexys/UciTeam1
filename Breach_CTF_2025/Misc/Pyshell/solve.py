from pwn import *
import hashlib
import time

# Generate hashes
prehashes = [hashlib.sha256(str(i).encode()).hexdigest()[:6] for i in range(1, 10001)]

# Brute-force
io = remote("challs.breachers.in", 1340)

commit_time = int(time.time())
io.sendlineafter(b"/$ ", b"git commit")

for i,hash_val in enumerate(prehashes):
    payload = b"git snapshot " 
    payload += str(commit_time).encode()
    payload += f"-{hash_val}".encode()
    print(f"{i} -- ", payload)
    io.sendlineafter(b"/$ ", payload)
    line = io.recvline()
    if not b"Error: Commit ID not found" in line:
        break

success(io.recv())
