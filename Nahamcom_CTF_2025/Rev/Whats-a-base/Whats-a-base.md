# Whats-a-base

Es un binario escrito en Rust. Con Ghidra buscamos "Enter the password" en cadenas formeatadas, encontramos un puntero referenciado a una funcion en la que ocurre el flujo principal del programa:

Comencé a renombrar cosas pero en resumen el programa:
- Toma la entrada del usuario y la modifica
- Usa `bcmp` para comparar la entrada transformada con una cadena hardcodeada

La funcion en mi decompilador en ese momento lucia asi:
``` C

void FLUJO_PRINCIPAL(void)

{
  byte bVar1;
  code *pcVar2;
  int iVar3;
  byte *pbVar4;
  ulong uVar5;
  byte *pbVar6;
  byte *pbVar7;
  uint uVar8;
  uint uVar9;
  byte *pbVar10;
  byte *pbVar11;
  ulong uVar12;
  byte bVar13;
  undefined auVar14 [16];
  long local_120;
  byte *local_118;
  long local_110;
  undefined **local_108;
  undefined8 uStack_100;
  undefined ***local_f8;
  undefined8 uStack_f0;
  undefined8 uStack_e8;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  undefined4 local_d8;
  undefined4 uStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  long local_b0;
  void *local_a8;
  long len;
  undefined **local_98;
  code *pcStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined8 local_48;
  undefined *local_40 [2];
  
  local_108 = &PTR_DAT_00157d18;
  uStack_100 = 1;
  local_f8 = (undefined ***)0x8;
  uStack_f0 = 0;
  uStack_e8 = 0;
  PRINTER(&local_108);
  local_120 = 0;
  local_118 = &DAT_00000001;
  local_110 = 0;
                    /* try { // try from 00107a0d to 00107ce9 has its C atchHandler @ 00107f25 */
  local_98 = (undefined **)FUN_00125930();
  auVar14 = FUN_00125960(&local_98,&local_120);
  if ((auVar14 & (undefined  [16])0x1) != (undefined  [16])0x0) {
                    /* try { // try from 00107ee3 to 00107f07 has its C atchHandler @ 00107f0a */
    local_108 = auVar14._8_8_;
    FUN_00107570(&DAT_001493b0,0x2b,&local_108,&PTR_FUN _00157cf8,&PTR_DAT_00157d28);
                    /* WARNING: Does not return */
    pcVar2 = (code *)invalidInstructionException();
    (*pcVar2)();
  }
  pbVar4 = local_118 + local_110;
  if (local_110 == 0) {
    pbVar10 = (byte *)0x0;
    pbVar11 = (byte *)0x0;
    pbVar7 = local_118;
joined_r0x00107b9b:
    do {
      do {
        pbVar6 = pbVar4;
        if (pbVar7 == pbVar6) {
          if (local_110 == 0) goto LAB_00107cce;
          goto LAB_00107cd3;
        }
        uVar8 = (uint)(char)pbVar6[-1];
        if ((int)uVar8 < 0) {
          bVar13 = pbVar6[-2];
          if ((char)bVar13 < -0x40) {
            bVar1 = pbVar6[-3];
            if ((char)bVar1 < -0x40) {
              pbVar4 = pbVar6 + -4;
              uVar9 = bVar1 & 0x3f | (pbVar6[-4] & 7) << 6;
            }
            else {
              pbVar4 = pbVar6 + -3;
              uVar9 = bVar1 & 0xf;
            }
            uVar9 = bVar13 & 0x3f | uVar9 << 6;
          }
          else {
            pbVar4 = pbVar6 + -2;
            uVar9 = bVar13 & 0x1f;
          }
          uVar8 = uVar8 & 0x3f | uVar9 << 6;
        }
        else {
          pbVar4 = pbVar6 + -1;
        }
      } while ((uVar8 - 9 < 5) || (uVar8 == 0x20));
      if (uVar8 < 0x80) break;
      uVar9 = uVar8 >> 8;
      if (uVar9 < 0x20) {
        if (uVar9 == 0) {
          bVar13 = (&DAT_0014e857)[(ulong)uVar8 & 0xff];
        }
        else {
          if (uVar9 != 0x16) break;
          bVar13 = uVar8 == 0x1680;
        }
      }
      else if (uVar9 == 0x20) {
        bVar13 = (byte)(&DAT_0014e857)[(ulong)uVar8 & 0xff] > > 1;
      }
      else {
        if (uVar9 != 0x30) break;
        bVar13 = uVar8 == 0x3000;
      }
    } while ((bVar13 & 1) != 0);
    pbVar11 = pbVar6 + ((long)pbVar11 - (long)pbVar7);
  }
  else {
    pbVar6 = local_118;
    pbVar10 = (byte *)0x0;
    do {
      bVar13 = *pbVar6;
      uVar12 = (ulong)bVar13;
      if ((char)bVar13 < '\0') {
        uVar8 = bVar13 & 0x1f;
        if (bVar13 < 0xe0) {
          pbVar7 = pbVar6 + 2;
          uVar12 = (ulong)(uVar8 << 6 | pbVar6[1] & 0x3f);
        }
        else {
          uVar9 = pbVar6[2] & 0x3f | (pbVar6[1] & 0x3f) << 6;
          if (bVar13 < 0xf0) {
            pbVar7 = pbVar6 + 3;
            uVar12 = (ulong)(uVar9 | uVar8 << 0xc);
          }
          else {
            pbVar7 = pbVar6 + 4;
            uVar12 = (ulong)(pbVar6[3] & 0x3f | uVar9 << 6 | (bVar 13 & 7) << 0x12);
          }
        }
      }
      else {
        pbVar7 = pbVar6 + 1;
      }
      pbVar11 = pbVar10 + ((long)pbVar7 - (long)pbVar6);
      uVar8 = (uint)uVar12;
      if ((4 < uVar8 - 9) && (uVar8 != 0x20)) {
        if (uVar8 < 0x80) goto joined_r0x00107b9b;
        uVar9 = (uint)(uVar12 >> 8);
        if (uVar9 < 0x20) {
          if ((uVar12 & 0xffffff00) == 0) {
            bVar13 = (&DAT_0014e857)[uVar12 & 0xff];
          }
          else {
            if (uVar9 != 0x16) goto joined_r0x00107b9b;
            bVar13 = uVar8 == 0x1680;
          }
        }
        else if (uVar9 == 0x20) {
          bVar13 = (byte)(&DAT_0014e857)[uVar12 & 0xff] >> 1;
        }
        else {
          if (uVar9 != 0x30) goto joined_r0x00107b9b;
          bVar13 = uVar8 == 0x3000;
        }
        if ((bVar13 & 1) == 0) goto joined_r0x00107b9b;
      }
      pbVar6 = pbVar7;
      pbVar10 = pbVar11;
    } while (pbVar7 != pbVar4);
LAB_00107cce:
    pbVar10 = (byte *)0x0;
    pbVar11 = (byte *)0x0;
  }
LAB_00107cd3:
  uVar12 = (long)pbVar11 - (long)pbVar10;
  pbVar10 = local_118 + (long)pbVar10;
  Modificar_Entrada(&local_b0,pbVar10,uVar12);
                    /* COMPARACION PRINCIPAL DE VICTORIA
                        */
  if ((len == 88) &&
     (iVar3 = bcmp(local_a8,
                   "m7xzr7muqtxsr3m8pfzf6h5ep738ez5ncftss7d1cftsk z49qj4zg7n9cizgez5upbzzr7n9cjosg45wqjosg3mu"
                   ,0x58), iVar3 != 0)) {
    local_68 = 0;
    uStack_60 = 0;
    local_78 = 0;
    uStack_70 = 0;
    local_88 = 0;
    uStack_80 = 0;
    local_98 = (undefined **)0x0;
    pcStack_90 = (code *)0x0;
    local_48 = 0;
    local_58 = 0x67452301;
    uStack_54 = 0xefcdab89;
    uStack_50 = 0x98badcfe;
    uStack_4c = 0x10325476;
    if (uVar12 != 0) {
      do {
        uVar5 = 0xffffffff;
        if (uVar12 < 0xffffffff) {
          uVar5 = uVar12;
        }
                    /* try { // try from 00107dfc to 00107e07 has its Ca tchHandler @ 00107f2a */
        FUN_001080f0(&local_98,pbVar10,uVar5);
        pbVar10 = pbVar10 + uVar5;
        uVar12 = uVar12 - uVar5;
      } while (uVar12 != 0);
    }
    local_b8 = local_48;
    local_c8 = CONCAT44(uStack_54,local_58);
    uStack_c0 = CONCAT44(uStack_4c,uStack_50);
    local_d8 = (undefined4)local_68;
    uStack_d4 = local_68._4_4_;
    uStack_d0 = (undefined4)uStack_60;
    uStack_cc = uStack_60._4_4_;
    uStack_e8 = local_78;
    uStack_e0 = (undefined4)uStack_70;
    uStack_dc = uStack_70._4_4_;
    local_f8 = (undefined ***)local_88;
    uStack_f0 = uStack_80;
    local_108 = local_98;
    uStack_100 = pcStack_90;
                    /* try { // try from 00107e5e to 00107ecd has its C atchHandler @ 00107f1f */
    FUN_00108000(local_40,&local_108);
    pcStack_90 = FUN_00108920;
    local_108 = &Congratulations!_PTR;
    uStack_100 = 2;
    uStack_e8 = 0;
    local_f8 = &local_98;
    uStack_f0 = 1;
    local_98 = local_40;
    PRINTER(&local_108);
  }
  else {
    local_108 = &Invalid_Password_PTR;
    uStack_100 = 1;
    local_f8 = (undefined ***)&DAT_00000008;
    uStack_f0 = 0;
    uStack_e8 = 0;
                    /* try { // try from 00107d3c to 00107d46 has its C atchHandler @ 00107f1f */
    PRINTER(&local_108);
  }
  if (local_b0 != 0) {
    thunk_FUN_00129b30(local_a8,local_b0,1);
  }
  if (local_120 != 0) {
    thunk_FUN_00129b30(local_118,local_120,1);
  }
  return;
}
```

Si entramos en la funcion que modifica la variable vemos que es una base32 con un alfabeto modificado.

**¿Cómo saber esto?**

Las bases tienen formas de trabajar similares:
- Extraen n bytes y los convierten en m bytes usando una tabla de conversion (por ejemplo base64 toma 3 bytes(24 bits) y los convierte en 4 bytes(6 bits se mapean a la vez)
- Usan algun padding porque la longitud de su texto cifrado debe ser un multiplo de n

En nuestro caso:
- Se toman grupos de 5 bytes
``` C
      local_40 = 5;
      if (param_3 < 5) {
        local_40 = param_3;
      }
```
- Se usa un alfabeto fijo para hacer operaciones
``` C
cVar2 = "ybndrfg8ejkmcpqxot1uwisza345h769"[bVar1 >> 3 ];
cVar2 = "ybndrfg8ejkmcpqxot1uwisza345h769"[(byte)((bVar 1 & 7) << 2 | bVar11 >> 6)];
cVar2 = "ybndrfg8ejkmcpqxot1uwisza345h769"[(byte)((bVar 1 & 7) << 2 | bVar11 >> 6)];
cVar2 = "ybndrfg8ejkmcpqxot1uwisza345h769"[bVar11 >> 1 & 0x1f];
```
- Se calcula un relleno
``` C
fVar13 = ceilf((fVar13 * 8.0) / 5.0);
uVar6 = uVar10 - uVar7; 
```

![2025-05-25-235826_1339x591_scrot](https://github.com/user-attachments/assets/0969e2bf-4f9c-4477-88d8-f09a4c7cd346)

Si introducimos `__rust_begin_short_backtrace__rust_end_short_backtraces` obtenemos la flag.


