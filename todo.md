### **ToDo List para Mejorar el Proyecto Presupuestador**

1. **Tarea: Refactorizar la Clase `PDFGenerator`**
   - **Archivo a Modificar**: `src/models/pdf_generator.py`
   - **Descripción**: Extraer la lógica de manejo de directorios en `PDFGenerator` a una nueva clase `DirectoryManager`. Esto sigue el Principio de Responsabilidad Única (SRP) y mejora la modularidad del código.

2. **Tarea: Implementar el Patrón de Inyección de Dependencias**
   - **Archivo a Modificar**: `src/models/db_manager.py`
   - **Descripción**: Refactorizar `DatabaseManager` para aceptar una conexión de base de datos inyectada en lugar de crearla internamente. Esto facilita las pruebas y la sustitución de implementaciones.

3. **Tarea: Dividir la Lógica de `BudgetService` en Múltiples Clases**
   - **Archivo a Modificar**: `src/models/budget_service.py`
   - **Descripción**: Separar la recolección de datos, validaciones, y persistencia de `BudgetService` en clases independientes. Cada clase debería manejar una responsabilidad específica para adherirse al SRP.

4. **Tarea: Crear Interfaces para `SalespersonManager`**
   - **Archivo a Crear**: `src/interfaces/salesperson_interface.py`
   - **Descripción**: Definir interfaces pequeñas y específicas (por ejemplo, `SalespersonLister`, `SalespersonCreator`) y hacer que `SalespersonManager` implemente estas interfaces para cumplir con el Principio de Segregación de Interfaces (ISP).

5. **Tarea: Aplicar el Patrón Estrategia para la Validación de Presupuestos**
   - **Archivo a Crear**: `src/strategies/budget_validation.py`
   - **Descripción**: Crear un conjunto de estrategias de validación para los presupuestos, que puedan ser fácilmente intercambiadas sin modificar la clase `BudgetService`. Esto mejorará la adherencia al Principio Abierto/Cerrado (OCP).

6. **Tarea: Refactorizar `DatabaseManager` para Mejorar la Creación de Tablas**
   - **Archivo a Modificar**: `src/models/db_manager.py`
   - **Descripción**: Mover la lógica de creación de tablas a una clase `TableManager` separada, de modo que `DatabaseManager` no tenga múltiples responsabilidades. Esto mejora la modularidad y adherencia al SRP.

7. **Tarea: Mejorar la Cobertura de Pruebas Unitarias**
   - **Archivo a Modificar**: `tests/test_budget_management.py`
   - **Descripción**: Agregar pruebas adicionales para cubrir casos extremos y asegurar que todas las ramas de código en `BudgetService` estén probadas. Esto aumentará la confianza en la estabilidad del sistema.

8. **Tarea: Implementar el Patrón Fábrica para la Creación de Conexiones a Base de Datos**
   - **Archivo a Crear**: `src/factories/database_connection_factory.py`
   - **Descripción**: Crear una fábrica para gestionar la creación de conexiones a bases de datos. Esto sigue el Principio de Inversión de Dependencias (DIP) y facilita la sustitución de la base de datos en el futuro.

9. **Tarea: Refactorizar `UserInterface` para Separar la Lógica de Presentación y Control**
   - **Archivo a Modificar**: `src/models/user_interface.py`
   - **Descripción**: Separar la lógica de presentación de la lógica de control en `UserInterface`, creando una clase `UserInputHandler` para manejar la entrada del usuario. Esto sigue el SRP y mejora la mantenibilidad.

10. **Tarea: Documentar el Código Refactorizado**
    - **Archivo a Modificar**: Todos los archivos modificados
    - **Descripción**: Asegurarse de que todas las clases y métodos refactorizados estén bien documentados, explicando claramente sus responsabilidades y cómo se relacionan con otros componentes. Esto facilita la comprensión y el mantenimiento del código.
