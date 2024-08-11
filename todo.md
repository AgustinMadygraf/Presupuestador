### **ToDo List para Mejorar el Proyecto Presupuestador**


8. **Tarea: Implementar el Patrón Fábrica para la Creación de Conexiones a Base de Datos**
   - **Archivo a Crear**: `src/factories/database_connection_factory.py`
   - **Descripción**: Crear una fábrica para gestionar la creación de conexiones a bases de datos. Esto sigue el Principio de Inversión de Dependencias (DIP) y facilita la sustitución de la base de datos en el futuro.

9. **Tarea: Refactorizar `UserInterface` para Separar la Lógica de Presentación y Control**
   - **Archivo a Modificar**: `src/models/user_interface.py`
   - **Descripción**: Separar la lógica de presentación de la lógica de control en `UserInterface`, creando una clase `UserInputHandler` para manejar la entrada del usuario. Esto sigue el SRP y mejora la mantenibilidad.
