# Guía para Contribuyentes

## Descripción
Este documento ofrece directrices para desarrolladores y colaboradores interesados en contribuir al proyecto. Aquí encontrarás información sobre cómo hacer contribuciones efectivas y coherentes.

## Cómo Contribuir

### 1. Configurar tu Entorno de Desarrollo
Antes de contribuir, asegúrate de tener un entorno de desarrollo adecuado. Clona el repositorio del proyecto:
```bash
git clone https://tu-repositorio-aqui.git
cd nombre-del-proyecto
```
Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 2. Trabajar con Branches
Para comenzar a trabajar en una nueva característica o corrección, crea una nueva rama:
```bash
git checkout -b nombre-de-tu-rama
```
Asegúrate de que tu rama se base en la última versión del branch principal.

### 3. Estándares de Codificación
- Utiliza nombres claros y descriptivos para funciones y variables.
- Comenta tu código donde sea necesario para explicar secciones complejas.
- Sigue la guía de estilo [PEP 8](https://www.python.org/dev/peps/pep-0008/) para Python o el equivalente para otros lenguajes.

### 4. Realizar Cambios
Haz tus cambios de manera local y escribe [tests](https://link-a-documentacion-de-tests) que confirmen la funcionalidad de tu código. Asegúrate de que todos los tests pasen antes de preparar un pull request.

### 5. Committing
Cuando hagas commits de tus cambios, usa mensajes de commit claros y concisos:
```bash
git commit -m "Añadir funcionalidad X para resolver Y"
```

### 6. Enviar Pull Requests
Antes de enviar un pull request, rebase tu rama sobre la última versión del branch principal para facilitar un merge limpio:
```bash
git fetch origin
git rebase origin/main
```
Envía el pull request a través de GitHub, proporcionando una descripción clara de los cambios y cualquier otra información relevante.

### 7. Revisión de Código
Después de enviar tu pull request, otros desarrolladores revisarán tu código. Sé receptivo a la retroalimentación y realiza los ajustes necesarios.

## Reportar Issues
Si encuentras errores o problemas en el proyecto, por favor reporta los issues usando [GitHub Issues](https://link-a-github-issues). Proporciona una descripción detallada del problema, incluyendo pasos para reproducirlo y la versión del software.

## Soporte
Si necesitas ayuda con las directrices de contribución, contacta a los mantenedores del proyecto a través de agustin.mtto.madygraf@gmail.com.