# Beginner / Echoes of Wisdom

Cada byte de datos de ICMP representa un caracter de la flag, los extraemos y convertimos para obtener la bandera

`tshark -r traffic.pcap -T fields -Y 'icmp' -e data | while read line; do echo $line | xxd -r -p;done`

`flag{ICMP_c0berT_Ch4nN3|}`
