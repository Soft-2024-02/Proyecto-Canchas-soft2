
# DJANGO Cheatsheet

## Crear un Proyecto
Para crear un proyecto en la carpeta actual (el punto `.` indica que el proyecto se crea en la carpeta donde estás ubicado):
```bash
django-admin startproject nombre_del_proyecto .
```

## Ejecutar el Proyecto
Para ejecutar el servidor de desarrollo de Django:
```bash
python manage.py runserver
```

### Ejecutar en un Puerto Específico
Para ejecutar el servidor en un puerto específico (por ejemplo, el puerto 3000):
```bash
python manage.py runserver 3000
```

## Crear una App dentro del Proyecto
Para crear una nueva aplicación dentro del proyecto Django:
```bash
python manage.py startapp nombre_del_app
```

## Migraciones

### Crear Migraciones Globales
Para generar migraciones para todas las apps registradas:
```bash
python manage.py makemigrations
```

### Crear Migraciones para una App Específica
Si deseas generar migraciones únicamente para una app específica:
```bash
python manage.py makemigrations nombre_del_app
```

### Ejecutar las Migraciones
Para aplicar las migraciones a la base de datos:
```bash
python manage.py migrate
```
