# solve.py
# Pub key
e = 65537
# Mod
n = 196603733802071409961275562212278242151
# Mod factors
p = 879421070503884397
q = 223560408541749867683
assert(p*q==n)
# Eulers phi totient
phi = (p - 1) * (q - 1)
# Ciphertext
c = 151832817966710307438243645623410737448
#Priv key
d = pow(e, -1, phi)
# Plaintext
m = pow(c, d ,n)
# Convert to bytes
byte_length = (m.bit_length() + 7) // 8
m_bytes = m.to_bytes(byte_length, byteorder='big')

print(f"m={m}")
print(f"m_bytes={m_bytes}")
