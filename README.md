Gestor de Activos de Cómputo

Bienvenido al Gestor de Activos de Cómputo, una aplicación web desarrollada con Django, Bootstrap, Python, JavaScript, HTML y CSS. Esta aplicación proporciona una solución integral para gestionar y mantener un inventario de activos de cómputo en una empresa.

CARACTERISTICAS PRINCIPALES

-Gestión de Activos: Registra y realiza un seguimiento de todos los activos de cómputo, incluyendo información detallada como modelo, marca, número de serie, estado y más.

-Relación Usuario-Activo: Asocia cada activo con un usuario específico, facilitando la asignación y seguimiento de activos a empleados.

-Licencias Asociadas: Administra las licencias de software relacionadas con cada activo, manteniendo un control detallado de las licencias y sus estados.

-Generación de Documentos PDF: Crea automáticamente documentos PDF personalizados con datos específicos del usuario, proporcionando un registro firmado para la asignación de activos.

-Almacenamiento de Archivos: Permite almacenar documentos PDF generados y otros archivos relevantes para cada activo y usuario.

-Compatibilidad con Bases de Datos: Admite bases de datos Postgres, SQL Server y otras, brindando flexibilidad en la elección de la plataforma de base de datos.

\\Configuración del Proyecto\\

REQUISITOS PREVIOS
-Python 3.12
-Django 5.0.1
-Bootstrap
-Otros requisitos en el archivo requirements.txt

\\Instalación\\
Clona este repositorio a tu máquina local.
En git bash
Copy code
git clone https://github.com/tu_usuario/gestor-activos.git
cd gestor-activos

\\Instala las dependencias.\\
-Dentor de la carpeta que guarda el repositorio ejecute el siguiente comando
-pip install -r requirements.txt


BASE DE DATOS
-Configura la base de datos en el archivo settings.py.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite',
        'NAME': 'nombre_base_de_datos',
    }
}

PARA CORRER LA APLICACION

-Dentro de powershelll ejecuta los comandos:
python manage.py makemigration
python manage.py migrate

-Inicia el servidor.
python manage.py runserver
Accede a la aplicación en tu navegador: http://localhost:8000
