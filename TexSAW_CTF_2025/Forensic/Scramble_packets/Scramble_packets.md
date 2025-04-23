# Scramble packets

La flag esta en los paquetes ICMP de tipo 8 que transmiten un byte de carga util, ordenados por el numero de secuencia:

```
tshark -r cap.pcap -Y "icmp.type==8 and data.len == 1" -T fields -e icmp.seq -e data | sort -n | awk '{print $2}' | tr -d "\n" | xxd -r -p
TexSAW{not_the_fake_one}
```

`TexSAW{not_the_fake_one}`
