# Misc / Strange sightings

+ A principios del video en 0:27 se envia un mensaje "COME GET YOUR FILE"
+ A partir de 6:45 hay una pequeña lampara que envia un mensaje en código morse: .---- ...-- --... .-.-.- .---- ---.. ....- .-.-.- ..... --... .-.-.- .---- ---.. --...

![lampara](https://github.com/user-attachments/assets/594fbca4-3d48-4b47-b7f2-1ff20683d3d7)

+ El mensaje es una dirección IP: 137.184.57.187
+ Atendiendo al mensaje nos conectamos por FTP: ftp 137.184.57.187 

``` bash
Connected to 137.184.57.187.
220 Boo!
Name (137.184.57.187:kali): dir
530 This FTP server is anonymous only.
ftp: Login failed

ftp> cd
(remote-directory) cd
530 Please login with USER and PASS.

ftp> user
(username) anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> dir
229 Entering Extended Passive Mode (|||47926|)
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp            56 Oct 25 19:24 flag.txt
226 Directory send OK.

ftp> get flag.txt
local: flag.txt remote: flag.txt
229 Entering Extended Passive Mode (|||31580|)
150 Opening BINARY mode data connection for flag.txt (56 bytes).
100% |*************************************************************************************************************************************************|    56        0.13 KiB/s    00:00 ETA
226 Transfer complete.
56 bytes received in 00:00 (0.08 KiB/s)

ftp> exit
221 Goodbye.
```

`NICC{I_h0p3_whatever_is_in_the_backrooms_brought_candy}`
