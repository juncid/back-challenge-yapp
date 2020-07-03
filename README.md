# Back-challenge-Yapp

> Reto tecnico para el cargo de Desarrollador Backend en Yapp

El siguiente proyecto demuestra una implementación simple de una API Serverless, la cual se conecta a una  base de datos local de MySql y permite realizar operaciones CRUD, mediante endpoints, hacia esta. Para su desarrollo en un entorno local se utilizó AWS SAM CLI lo que permite simular su ejecución en este, permitiendo centrarnos en el código más que en la configuración en AWS.

## Descripción

Este proyecto contiene tanto el codigo fuente como scripts en SQL que permiten la ejecución en un entorno local, a continuación se describen estos:

- .env.example - Un template que contiene la variable de entorno para la coneccion a la base de datos Mysql.
- template.yaml - Un template que contiene toda la información necesaria para ejecutar la aplicación en un entorno serverless.
- movies_api/ - Carpeta donde se encuentra todo el codigo de la función lambda.
  - tests/ - Test unitarios para la aplicacíon. *No fueron creados en esta version
  - app.py - Aplicacion Flask-Lambda, dentro incluye tambien el modelo Movie. *resolver en siguiente version.
  - serializers.py - Serializador para el modelo Movie.
  - utils.py - Funciones comunes que se utilizan en app.py
  - Script.sql - Script SQl que permite restablecer la base de datos para su uso.
  - data.csv - Archivo que contiene todos los datos de las peliculas en formato csv.

## Requerimientos

Se utilizará como entorno una maquina virtual con XUbuntu 18.04 LTS desde cero, esto debido a que versiones mas nuevas presentan errores al instalar docker, el cual es un requisito para ejecutar AWS SAM CLI.

Se realizarán los siguientes pasos, pensando en un entorno Ubuntu/Debian, por lo cual se debe de abrir una nueva terminal, usar ctrl+alt+t como atajo:

- ### Instalar Git 

    ```bash
    $ sudo apt update
    $ sudo apt install git -y
    ```

    Verificamos que fue instalado correctamente.
    ```bash
    $ git --version
    ```

- ### Actualizar a Python3.7 y configurarlo como default - Necesario para ejecutar funciones lambda.

    Verificar version actual de python
    ```bash
    $ python3 -V
    ```
    Si esta es menor a 3.7, continuar con los siguientes pasos.

    Instalar python3.7
    ```bash
    $ sudo apt-get install python3.7 -y
    ```

    Agregar python3.6 & python3.7 a update-alternatives
    ```bash
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
    ```
    
    Actualizar como default a python3.7
    ```bash
    $ sudo update-alternatives --config python3
    ```
    Ingresar opcion 2 en consola para seleccionar python3.7

    Verificar nuevamente la version de python
    ```bash
    $ python3 -V
    ```
    Debe de indicar una version superior a 3.7


- ### Instalar pip para python3 
    ```bash
    $ sudo apt install python3-pip
    ```

    Verificar version de pip3
    ```bash
    $ pip3 --version
    ```

- ### Instalar virtual enviroment para python
    ```bash
    $ sudo apt install python3-pip
    ```


- ### Instalar Docker. - Necesario para ejecutar SAM CLI de manera local.
    
    Actualizar apt-get e instalar packages necesarios
    ```bash
    $ sudo apt-get update

    $ sudo apt-get install \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg-agent \
      software-properties-common
    ```

    Añadir llave GCP oficial de Docker
    ```bash
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

    Añadir repositorio con una version estable de Docker
    ```bash
    $ sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
    ```

    Instalar Docker Engine
    ```bash
     $ sudo apt-get update
     $ sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

    Verificar instalacion de Docker
     ```bash
     $ sudo docker run hello-world
    ```

    Configurar Docker para no usar sudo antes de cada comando
     ```bash
     $ sudo groupadd docker
    ```
    Puede indicar que el grupo ya ha sido creado

    Añadir usuario actual de linux al grupo docker
     ```bash
     $ sudo usermod -aG docker nombre_de_nuestro_usuario
    ```
    Se debe indicar el nombre que aparece antes del @ en la terminal

    Para que los cambios se ejecuten debemos cerrar la sesion de usuario mediante la interfaz grafica y volvernos a loguear.

    Probar el siguiente comando
     ```bash
     $ docker ps
    ```
    Si presenta algun error, favor de reiniciar el sistema operativo para que se ejecuten correctamente los cambios.




- ### Instalar Base de datos Mysql


    En caso de no entender algun paso, revisar este [tutorial](https://platzi.com/tutoriales/1631-java-basico/226-instalar-mysql-y-workbench-en-linux-ubuntu-1404/) que expone graficamente los mismos pasos a seguir. 

    Instalar Mysql Server
    ```bash
     $ sudo apt-get install mysql-server -y
    ```

    Verificar version Mysql
    ```bash
     $ mysql --version
    ```

    Configurar la base de datos
    ```bash
    $ sudo mysql_secure_installation
    ```
    Se ejecutara una linea de comandos interactiva donde deberemos responder Y/N a las preguntas.

    Paso 1: Seleccionar Opcion 0 para crear una contraseña debil pero facil de recordar, esta debe tener como minimo 8 caracteres alfanumericos.
    Paso 2: Seleccionar Y, para crear nuestra contraseña para el usuario root.
    Paso 3: Seleccionar Y, para eliminar los usuarios anonimos en la base de datos.
    Paso 4: Seleccionar N, para no deshabilitar el login a la base de datos de manera remota.
    Paso 5: Seleccionar Y, para remover la base de datos de prueba.
    Paso 6: Seleccionar Y, para recargar los privilegios de las tablas en la base de datos.



    Probar conexion a la base de datos
    ```bash
    $ sudo mysql -u root -p
    ```
    Se debe ingresar la contraseña creada en la actividad anterior.

    Para salir de la consola de mysql
    ```bash
    mysql> exit
    ```


- ### Instalar AWS SAM CLI 

  Para poder instalar SAM CLI necesitaremos Homebrew para linux.
  ```bash
    $ sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
  ```
  
  Añadir Homebrew a nuestro PATH
  ```bash
    $ test -d ~/.linuxbrew && eval $(~/.linuxbrew/bin/brew shellenv)
    $ test -d /home/linuxbrew/.linuxbrew && eval $(/home/linuxbrew/.linuxbrew/bin/brew shellenv)
    $ test -r ~/.bash_profile && echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.bash_profile
    $ echo "eval \$($(brew --prefix)/bin/brew shellenv)" >>~/.profile
  ```

  Verificar version Homebrew
  ```bash
    $ brew --version
  ```

  Instalar SAM CLI
   ```bash
    $ brew tap aws/tap
    $ brew install aws-sam-cli
  ```

  Verificar version SAM
  ```bash
    $ sam --version
  ```


- ### Crear usuario backend en mysql.

  Conectarnos a la base de datos.
    ```bash
    $ sudo mysql -u root -p
    ```

  Crear un nuevo usuario llamado backend con contraseñas en localhost
    ```bash
    mysql> CREATE USER 'backend'@'localhost' IDENTIFIED BY 'password';
    ```

  Otorgar privilegios al usuario creado
  ```bash
    mysql> GRANT ALL PRIVILEGES ON * . * TO 'backend'@'localhost';
    ```

  Salir de la sesion
  ```bash
    mysql> exit;
  ```


## Implementación

Se necesita abrir una nueva terminal, solo si esta ya se encuentra cerrada,
junto con cambiar de directorio a Documentos o Documents, segun sea el caso.
  ```bash
    $ cd Documentos/
  ```


- ### Clonar repositorio

Clonar repositorio e ingresar a carpeta back-challenge-yapp
```bash
$ git clone https://github.com/juncid/back-challenge-yapp.git  
$ cd back-challenge-yapp  
```

- ### Definir variables globales

Copiar el siguiente archivo dentro del directorio back-challenge-yapp, este posee la siguiente variable de entorno:

```bash
$ cp .env.example .env
```

 DATABASE_URL: URL de MySQL para conectarse, se debe seguir la siguiente estructura, "mysql+mysqlconnector://{usuario}:{contraseña}@{host}:{puerto}/{base_de_datos}".

Es importante recordar que tambien se ocupa la misma variable de entorno para la configuracion global de SAM localizada en el archivo `template.yaml`.


- ### Configurar entorno virtual e instalar requerimientos:
Para instalar los requerimientos de python se utilizara virtualenv.
```bash
$ virtualenv -p python3 .venv
```

Activar e instalar requerimientos de python.
```bash
$ source .venv/bin/activate
$ pip3 install -r movies_api/requirements.txt
```


- ### Seed Base de datos
Se correra el script Script.sql ubicado dentro de la carpeta movies_api en mysql el cual restablecera la base de datos completamente para su uso, este acercamiento se utilizo para generar dos servicios de distinta naturaleza en la misma api.

```bash
$ sudo mysql -u backend -p < movies_api/Script.sql
```

- ### Ejecutar SAM CLI en entorno local

Compilar codigo fuente usando SAM build 
```bash
$ sam build --use-container 
```

Iniciar sam en modo local
```bash
$ sam local start-api --docker-network host 
```


Nota: Los comandos anteriores, cuando son ejecutados por primera vez, se demoran mas tiempo, debido a que descargan los archivos necesarios para ejecutar el entorno de manera local, por favor, sea paciente.

Al terminal el ultimo comando de ejecutarse, se mostrarán lineas similares a estas, indicando que ya es posible conectarse a la siguiente direccion y cuales son los endpoints y metodos disponibles.

```bash
Mounting HelloWorldFunction at http://127.0.0.1:3000/movie [DELETE, POST, PUT]
Mounting HelloWorldFunction at http://127.0.0.1:3000/movie/list [GET]
You can now browse to the above endpoints to invoke your functions. You do not need to restart/reload SAM CLI while working on your functions, changes will be reflected instantly/automatically. You only need to restart SAM CLI if you update your AWS SAM template
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
2020-07-03 04:55:25  * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)

```

Se recomienda utilizar [Postman](https://www.postman.com/) para testear los endpoints de una forma más comoda.

## Movies API:

Endpoint disponibilizados:

| Metodo | Endpoint    | Descripción                                                      | Requisitos                               |
| ------ | ----------- | ------------------------------------------------------------------ | -------------------------------------- |
| GET    | /movie/list | Retorna un json con todas las peliculas en base de datos. Codigo de estado de respuesta 200 | None                                   |                  |
| POST   | /movie      | Crea una nuevo registro de una pelicula en base de datos, utilizando los datos enviados en el request. Codigo de estado de respuesta 201            | Body: Infomarción de la pelicula en formato JSON          |
| PUT    | /movie      | Actualiza un registro de una pelicula en base de datos, utilizando los datos enviados en el request, en caso de no existir registro se devuelve un codigo de estado 404. Codigo de estado 201 | Body: Información de la pelicula en formato JSON, este incluye ID y se actualizan todos los campos. |
| DELETE | /movie      | Elimina un registro de una pelicula en base de datos, se utiliza el parametro enviado por url como id para seleccionarlo.         | QueryString: id de la pelicula enviado por URL     |


## Scripts

sudo mysql -u backend -p < ../../dumps/DumpMovies.sql
CREATE SCHEMA `movies` DEFAULT CHARACTER SET utf8 ;
