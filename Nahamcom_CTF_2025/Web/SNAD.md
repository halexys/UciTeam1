# SNAD

En script.js:

- La funcion `draw()` genera particulsas al hacer clic
- Con `injectSand(x,y,color)` se pueden insertar particulas en posiciones especificas
- Debemos insertar siete particulas en las posiciones objetivo y luego llamar a `checkFlag()`

Podemos hacer eso automaticamente en la consola del navegador:
```javascript
targetPositions.forEach(tp=>{
 injectSand(tp.x,tp.y,tp.colorHue)
})
checkFlag()
```

![2025-05-25-171550_1336x582_scrot](https://github.com/user-attachments/assets/9331740e-ec1e-4e05-8fd3-7dce8ccd59c5)
