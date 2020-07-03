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

- Instalar Git 

    ```bash
    $ sudo apt update
    $ sudo apt install git -y
    ```

    Verificamos que fue instalado correctamente.
    ```bash
    $ git --version
    ```

- Actualizar a Python3.7 y configurarlo como default - Necesario para ejecutar funciones lambda.

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


- Instalar pip para python3 
- Configurar virtual enviroment para python
- Instalar Docker. - Necesario para ejecutar SAM CLI de manera local.
- Instalar Base de datos Mysql 
- Instalar AWS SAM CLI 
- Configurar base de datos, crear usuario y base de datos para ejecutar proyecto.
- Realizar back-up de base de datos utilizando Script.sql


## Implementación

Se necesita abrir una nueva terminal

- ### Clone this repo

```bash
$ git clone https://github.com/delta575/yapp-backend-dev.git  # Clone this repo
$ cd yapp-backend-dev  # Change directory to project root folder
```

- ### Set environment variables

Edit file following this specifications:

```bash
$ cp .env.example .env  # Copy example
$ nano .env  # Edit file
```

| Variable     | Description                                                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| PYTHONPATH   | Changes python root path for SAM compatibility, must be changed to point at "yapp_backend" folder                                 |
| DATABASE_URL | MySQL URL for connection, must follow the following structure: "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}" |

**Important:** Set the same DATABASE_URL environment variable for SAM Global configs located on `template.yaml` file.

- ### Setup virtual environment and install requirements:

Install development requirements, poetry is used as the preferred package manager.
Follow the [install instructions](https://python-poetry.org/docs/#installation) for your enviroment.

Then install the project local dependencies:

```bash
$ poetry install  # Create virtual env and install dependencies
```

- ### Deploy MySQL DataBase

If you already have MySQL deployed you can skip this step, just make sure to point the DATABASE_URL env var correctly.

For easy deployment, a MySQL DataBase was containerized with a `docker-compose.yml` which also sets the needed environment variables for authentication.

```bash
$ docker-compose up --build -d  # Deploys MySQL database as a docker container
```

- ### Seed Data

Run the script `seed.py` which will create the Movie table from it's model and populate the DataBase with `data.csv` content.
data.csv follows [this Kaggle repository](https://www.kaggle.com/ruchi798/movies-on-netflix-prime-video-hulu-and-disney/data#) structure.

```bash
$ poetry shell  # activate virtual environment
$ python yapp_backend/seed.py  # run seed script
```

- ### Ejecutar SAM CLI en entorno local

```bash
$ sam build --use-container #SAM compilará el codigo fuente para su uso Serverless
$ sam local start-api --docker-network host #Este comando permite que el container de la aplicación se comunique con la base de datos en el entorno local.
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
