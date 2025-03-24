# Alien Encryption 1

![2025-03-22-173742_798x538_scrot](https://github.com/user-attachments/assets/087c3447-d841-4ba1-89f3-dff82450785d)

Las contraseñas son hashes MD5, usamos https://crackstation.net/ para crackearlos:

```
echo -ne "mars\nsaturn94\n4neptune\n" | nc alien-encryption.ctf.ritsec.club 32190
We found some hard drives on an alien ship that we think contains important data, but they seem to be encrypted. can you crack the passwords?
password 1: password 2: password 3:
password 1: correct
password 2: correct
password 3: correct
flag 1: RS{a_c0smic_adv3ntur3}
```

`RS{a_c0smic_adv3ntur3}`
