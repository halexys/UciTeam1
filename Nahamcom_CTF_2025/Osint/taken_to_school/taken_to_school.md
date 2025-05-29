# Taken to School

Buscar en Google "a student tried to hack a school's computer system" y filtrar por los datos de la ultima semana da varios resultados de un joven que se declara culpable de un hackeo a PowerSchool.

Luego si buscamos "powerschool hacking incident" nos lleva a https://www.powerschool.com/security/sis-incident/

PowerSchool contrató a Crowdstrike y estos hicieron un reporte del incidente: https://www.powerschool.com/wp-content/uploads/2025/03/PowerSchool-CrowdStrike-Final-Report.pdf:

![2025-05-26-153550_1349x610_scrot](https://github.com/user-attachments/assets/917fba31-e651-4dea-b0d4-8e3d8e4f6d59)

En "Appendix A: Indicators of Compromise" se muestra una tabla con IPs asociadas al hecho:

![2025-05-26-153746_898x575_scrot](https://github.com/user-attachments/assets/7f51e8f1-04c3-491b-a5dd-216a0465fd57)

La primera IP es la ip de origen de uno de los eventos:
```
 grep "91.218.50.11" network-log.cef
2024-12-22T15:07:40 CEF:0|PaloAltoNetworks|PAN-OS|8.3|44985|Trojan Signature Match|9|src=91.218.50.11 dst=192.168.113.2 spt=27660 dpt=443 proto=HTTPS act=allowed fileName=chemistry_notes.pdf eventHash=5b16c7044a22ed3845a0ff408da8afa9 cs1Label=threatType cs1=trojan
```
