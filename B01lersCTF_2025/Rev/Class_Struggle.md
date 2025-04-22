# Class Struggle
 
Nos dan codigo en C ofuscado, si lo trabajamos un poco el codigo desofuscaduo luce asi: 
``` C
// Codigo desofuscado
#include <stdio.h>
#include <string.h>

unsigned char cipher1(unsigned char j, int vfluhzftxror) {
  vfluhzftxror &= 7;
  return (j << vfluhzftxror) | (j >> (8 - vfluhzftxror));
}
unsigned char cipher2(unsigned char j, int vfluhzftxror) {
  vfluhzftxror &= 7;
  return (j >> vfluhzftxror) | (j << (8 - vfluhzftxror));
}
unsigned char cipher3(unsigned char jistcuazjdma, int i) {
  jistcuazjdma ^= (i * 37);
  jistcuazjdma = cipher1(jistcuazjdma, (i + 3) % 7);
  jistcuazjdma += 42;
  return jistcuazjdma;
}


int checkPassword(const char *g) {
  const unsigned char flag[] = {
      0x32, 0xc0, 0xbf, 0x6c, 0x61, 0x85, 0x5c, 0xe4, 0x40, 0xd0, 0x8f, 0xa2,
      0xef, 0x7c, 0x4a, 0x2,  0x4,  0x9f, 0x37, 0x18, 0x68, 0x97, 0x39, 0x33,
      0xbe, 0xf1, 0x20, 0xf1, 0x40, 0x83, 0x6,  0x7e, 0xf1, 0x46, 0xa6, 0x47,
      0xfe, 0xc3, 0xc8, 0x67, 0x4,  0x4d, 0xba, 0x10, 0x9b, 0x33};
  int inputLen = strlen(g);
  if (inputLen != sizeof(flag)) {
    printf("Len of the flag: %d",sizeof(flag));
    return 0;
  }
  for (int i = 0; i < inputLen; i++) {
    unsigned char z = cipher3(g[i], i);
    unsigned char e = cipher2((z & 0xF0) | ((~z) & 0x0F), i % 8);
    if (e != flag[i]) {
      printf("Expected %c\n",flag[i]);
      return 0;
    }
  }
  return 1;
}

int main(void) {
  char input[64];
  printf("Please input the flag: ");
  fgets(input, sizeof(input), stdin);
  char *nl = strchr(input, '\n');
  if (nl) {
    *nl = 0;
  }
  if (checkPassword(input)) {
    puts("Correct!");
  } else {
    puts("No.");
  }
  return 0;
}
```

Debemos invertir las operaciones que se le hacen a la entrada de usuario y aplicarselo a la flag:
``` python
def cipher1Inverse(j, input):
    input &= 7;
    return (j >> input) | (j << (8-input)) & 0xFF

def cipher2Inverse(j, input):
    input &= 7;
    return (j << input) | (j >> (8-input)) & 0xFF

def cipher3Inverse(input, i):
    input = (input - 42) & 0xFF
    input = cipher1Inverse(input, (i+3) %7)
    input ^= (i*37)
    return input & 0xFF

def crackFlag():
  flag = []
  cipher = [
      0x32, 0xc0, 0xbf, 0x6c, 0x61, 0x85, 0x5c, 0xe4, 0x40, 0xd0, 0x8f, 0xa2,
      0xef, 0x7c, 0x4a, 0x2,  0x4,  0x9f, 0x37, 0x18, 0x68, 0x97, 0x39, 0x33,
      0xbe, 0xf1, 0x20, 0xf1, 0x40, 0x83, 0x6,  0x7e, 0xf1, 0x46, 0xa6, 0x47,
      0xfe, 0xc3, 0xc8, 0x67, 0x4,  0x4d, 0xba, 0x10, 0x9b, 0x33 ]
  for i in range(len(cipher)):
      e = cipher2Inverse(cipher[i],i%8)
      z = (e & 0xF0) | (~e & 0x0F)
      c = cipher3Inverse(z,i)
      flag.append(chr(c))
    #unsigned char z = cipher3(g[i], i);
    #unsigned char e = cipher2((z & 0xF0) | ((~z) & 0x0F), i % 8);
  print("".join(flag))

crackFlag()
```

`bctf{seizing_the_m3m3s_0f_pr0ducti0n_32187ea8}`
