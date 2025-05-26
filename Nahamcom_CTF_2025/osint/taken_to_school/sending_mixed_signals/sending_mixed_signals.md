# Sending Mixed Signals

En [esta publicacion](https://micahflee.com/heres-the-source-code-for-the-unofficial-signal-app-used-by-trump-officials/) se encuentran las primeras respuestas, la cadena hardcodeada y el correo del que escribio el codigo:

**1**: enRR8UVVywXYbFkqU#QDPRkO

**2**: moti@telemessage.com

Para encontrar la tercer parte:
- `git clone --mirror https://github.com/micahflee/TM-SGNL-Android.git`: Descargar completo el [repositorio de la app para Android](https://github.com/micahflee/TM-SGNL-Android/)
- `first_commit=$(git log --all -S'enRR8UVVywXYbFkqU#QDPRkO' \
  --pretty=format:%H --reverse | head -n1)`: Encontrar el primer commit que contiene la cadena.
- `git describe --tags --contains $first_commit`: Encontrar el tag mas  cercano a ese commit.

**3**: Release_5.4.11.20
