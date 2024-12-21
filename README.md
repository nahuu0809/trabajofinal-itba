# Stock Data Application

Esta aplicación permite obtener y almacenar datos históricos de acciones utilizando la API de Polygon.io. Los datos obtenidos se almacenan en una base de datos creada usando SQLite para su uso posterior, permitiendo seleccionar y visualizar los tickers sin necesidad de hacer una nueva consulta a la API cada vez.

## Instalación

1. Clona el repositorio a tu máquina local:

    ```bash
    git clone https://github.com/nahuu0809/trabajofinal-itba.git
    cd trabajofinal-itba
    ```

2. Crea un entorno virtual para el proyecto (opcional pero recomendado):

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa 'venv\Scripts\activate'
    ```

3. Instala las dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

4. Crea un archivo `.env` para almacenar tu clave API:

    ```plaintext
    API_KEY=tu_clave_de_api
    ```

    IMPORTANTE: Para que la aplicacion funcione correctamente, es necesario tener una API KEY de [Polygon.io](https://polygon.io/) para lo cual es requerido tener una cuenta.

5. Ejecuta el script de la aplicación:

    ```bash
    python main.py
    ```

## Uso

1. Al abrir la aplicación, se solicita que ingreses tu nombre.
2. Luego de enviar tu nombre, se muestra el ticker y el rango de fechas de las acciones que podrás seleccionar desde un menú desplegable.
3. La aplicación usa la API de Polygon.io para obtener los datos de las acciones y almacenarlos en una base de datos SQLite local (`stocks.db`).
4. Los datos de los tickers se almacenan en la base de datos y no es necesario hacer una nueva consulta a la API si ya están almacenados.

## Dependencias

- `requests`: Para realizar HTTP requests a la API de Polygon.io.
- `python-dotenv`: Para cargar las variables de entorno (Ejemplo: API KEY de Poligon) desde el archivo `.env`.
- `tkinter`: Para la creación de la interfaz gráfica de usuario.
