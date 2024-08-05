# Guía de Uso

## Descripción
Este documento proporciona instrucciones detalladas sobre cómo utilizar el software, incluyendo ejemplos prácticos y descripciones de las funcionalidades disponibles.

## Inicio Rápido
Una vez instalado el software, puedes comenzar a utilizarlo siguiendo estos sencillos pasos.

### Ejecutar la Aplicación
Para iniciar la aplicación, ejecuta el siguiente comando en la terminal:
```bash
python app.py
```
Este comando arrancará el servidor local y la aplicación estará accesible en `http://localhost:8000`.

### Interfaz Principal
Al acceder a la aplicación, te encontrarás con la interfaz principal que incluye las siguientes opciones:
- **Crear Nuevo Proyecto**: Permite iniciar un nuevo proyecto.
- **Ver Proyectos**: Lista todos tus proyectos existentes.

## Funcionalidades Detalladas

### 1. Crear Nuevo Proyecto
Para crear un nuevo proyecto, sigue estos pasos:
- Haz clic en "Crear Nuevo Proyecto".
- Completa el formulario con los detalles del proyecto, como el nombre, la descripción y la fecha de inicio.
- Haz clic en "Guardar" para almacenar la información del proyecto en la base de datos.

### 2. Ver Proyectos
- Accede a "Ver Proyectos" desde el menú principal.
- Aquí podrás ver una lista de todos los proyectos creados.
- Selecciona un proyecto para ver más detalles o para editarlo.

## Ejemplos de Comandos

### Ejemplo 1: Consultar Datos
Para consultar datos desde la línea de comando, puedes utilizar:
```bash
python query_data.py --project_id=123
```
Este comando te mostrará los datos relacionados con el proyecto con ID 123.

### Ejemplo 2: Actualizar Proyecto
Para actualizar la información de un proyecto existente:
```bash
python update_project.py --project_id=123 --new_name="Proyecto Actualizado"
```
Este comando cambiará el nombre del proyecto con ID 123 a "Proyecto Actualizado".

## Problemas Comunes y Soluciones
- **Problema**: La aplicación no carga después de ejecutar el comando.
  - **Solución**: Asegúrate de que el servidor local se esté ejecutando y que no haya errores en la consola.

## Soporte
Si tienes preguntas adicionales o necesitas soporte técnico, no dudes en contactar a nuestro equipo de soporte técnico a través de agustin.mtto.madygraf@gmail.com.