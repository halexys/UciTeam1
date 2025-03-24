# Strike Team Biometrics

Con los datos de `pima-indians-diabetes.csv` debiamos entrenar un modelo de IA para predecir un dato en `strike_team_biometrics.csv`

![2025-03-24-125349_736x610_scrot](https://github.com/user-attachments/assets/a43f50b2-5794-40a2-8df4-c2241a046236)

### Solucion en python con pandas y sklearn

```
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Cargar los datos
train_data = pd.read_csv("pima-indians-diabetes.csv", header=None)
test_data = pd.read_csv("strike_team_biometrics.csv", header=None)

# Separar características (X) y etiquetas (y) en el conjunto de entrenamiento
X_train = train_data.iloc[:, :-1]  # Todas las columnas excepto la última
y_train = train_data.iloc[:, -1]   # Última columna (etiquetas)

# Entrenar un modelo (usaremos Random Forest)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predecir la vulnerabilidad del equipo de ataque
X_test = test_data  # Todas las columnas son características
predictions = model.predict(X_test)

# Convertir las predicciones a una cadena binaria
binary_string = "".join(str(int(pred)) for pred in predictions)

# Envolver en RS{}
result = f"RS{{{binary_string}}}"
print(result)
```

### Solucion con Orange

![2025-03-23-112641_1365x730_scrot](https://github.com/user-attachments/assets/089bef81-ad87-4b4d-8e45-c96a1b1a9523)

Designar columna de inmunes/vulnerables como columna objetivo en el `Select Columns` de arriba, el de los datos de la poblacion india:

![2025-03-23-112650_1364x724_scrot](https://github.com/user-attachments/assets/168976a7-d741-4a57-962a-97e7722ecff7)

Cliquear en `Predictions` para ver la prediccion de inmunes/vulnerables:

![2025-03-24-125948_1362x262_scrot](https://github.com/user-attachments/assets/dfa6919d-4374-4217-b388-63d263d9957a)

En ambos ejemplos el modelo utilizado fue `Random Forest` pero otros como `Neural Network` y `Gradient Boosting` tambien dieron un resultado correcto para esa muestra pequeña y una relacion no lineal de los datos. 

`RS{11010101}`


