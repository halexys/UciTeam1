# Parma

La bandera esta en el codigo fuente del documento:

`grep -in "class" parma.html | awk -F\> {'print $2'} | tr -d "</span"| tr -d "\n"`

`CodeViciCTF{Prm_i_the_lt_itro} `
