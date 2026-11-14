# Mini-orquestador de asistencia
 
## 1. Introducción
 
Este proyecto es una herramienta que se dedica a pasar lista en una academia simulada. Funciona con un motor de nodos, ya que el objetivo principal del proyecto es entender la base de lo que no se ve sobre cómo funciona n8n. Una instancia de la clase `Contexto` va pasando de nodo en nodo, añadiendo o utilizando la información que se necesita.
 
## 2. ¿Cómo ejecutarlo?
 
Para ejecutar el proyecto solo hay que descargarlo del enlace, hacer `uv sync` y copiar los campos del `.env.example` a un nuevo `.env` personal. Para ejecutar el programa hay que escribir en el terminal `uv run asistencia` y para probar los tests `uv run pytest`. Para pasar la lista, hay que especificar el día en formato AAAA-MM-DD o escribir una h para pasar lista el mismo día. 
La contraseña que se necesita para vincular Gmail con Python es una contraseña de aplicación. Para crearla tiene que estar activada la verificación en 2 pasos. 

Solo los viernes se envían los correos de ausencia a los alumnos. 

 
## 3. Diagrama de nodos
 
Todo el flujo de nodos está en una lista dentro del archivo `workflow.json`. Siguen el siguiente esquema:
 
```
LeerAlumnos
   ↓
LeerGrupos
   ↓
LeerRegistro
   ↓
FiltrarGruposPorDia
   ↓
PasarLista
   ↓
EscribirCSV
   ↓
EscribirContador
   ↓
LeerAusentes
   ↓
EnviarCorreo
```
 
## 4. Estructura del proyecto
 
- **models**: script con las clases `Alumno`, `Grupo`, `RegistroAsistencia` y `Contexto`, todas basadas en `BaseModel` de Pydantic. A continuación también se crean las excepciones propias del proyecto: la excepción base `AsistenciaError` y, basadas en ella, `VariablesError`, `DatosNoEncontradosError`, `DatosVaciosError`, `EscrituraError`, `NotificacionError`, `NodeError` y `ConfigurationError`.
- **nodos**: script en el que se define la clase `Nodo`. A continuación se programan todas las clases que se basan en `Nodo`, con su respectiva lógica importada de funciones de otros archivos. Estos nodos (clases) son: `LeerAlumnos`, `LeerGrupos`, `LeerRegistro`, `FiltrarGruposPorDia`, `PasarLista`, `EscribirContador`, `EscribirCSV`, `LeerAusentes` y `EnviarCorreo`.
  Las únicas que tienen lógica incorporada son las dos últimas, que solo se ejecutan si se pasa la lista un viernes: solo esos días se analiza si los alumnos han faltado 3 o más veces y se envía un mensaje si corresponde.
- **workflow**: script en el que se programa la clase `Workflow`, encargada de ejecutar por orden los nodos que reciba en formato lista.
- **configuracion**: script en el que se programa la clase `ConfigWorkflow`, la cual no permite que se haga todo el proceso si hay un nodo erróneo en la lista. Asimismo, también tiene la función `cargar_workflow`, encargada de transformar la información del archivo `.json` a una lista que puede ser usada por la clase `Workflow`.
- **lectura**: script con 4 funciones:
  - `leer_alumnos`: obtiene los datos de un documento CSV y devuelve una lista con los alumnos presentes en el mismo.
  - `leer_grupos`: obtiene los datos de un documento CSV y devuelve una lista con los grupos presentes en el mismo.
  - `leer_registro`: obtiene los datos de un documento CSV y valida el número de registros de asistencia que hay en un día concreto.
  - `detectar_ausencia`: obtiene los datos del registro de asistencia y devuelve los correos de los alumnos (o de los tutores si son menores) si han faltado 3 o más veces en el mes en el que se encuentran.
- **escritura**: script con 3 funciones:
  - `escribir_registro`: valida si hay un registro para el día que se quiere pasar lista; en caso de que haya, se añade el registro y, en caso contrario, primero se crea el documento y después se crea el registro.
  - `veri_doc_asistencia`: encargado de crear el documento de asistencia de un mes en caso de que aún no exista.
  - `escribir_asistencia`: encargado de escribir la asistencia que pasa un profesor.
- **notificaciones**: script con una función principal que se encarga de enviar notificaciones si detecta que un alumno ha faltado 3 o más veces a clase en el mes en el que se pasa asistencia.
## 5. Decisiones de diseño
 
- El sistema utiliza un `Contexto` común que va pasando de nodo en nodo para simular el funcionamiento de n8n.
- Se han usado excepciones propias, que especifican exactamente los errores encontrados durante la ejecución del programa. Asimismo, se ha creado la lógica para registrar en un log todos los errores y los pasos hechos en la ejecución.
- Se ha hecho una introducción a las funcionalidades de `tenacity`. Se ha creado lógica para reintentar los fallos derivados de la red, pero no los de contraseña errónea.
- Se ha hecho una introducción a las funcionalidades de `asyncio` y las corutinas: los correos se envían en paralelo, repartidos en hasta 5 lotes (cada lote con su propia conexión).
- El flujo de nodos se define en `workflow.json` y se valida con Pydantic, de modo que se puede cambiar el flujo sin tocar el código.
## 6. RGPD
 
Todos los datos usados son falsos y se han creado mediante el script `data_faker` para respetar la normativa RGPD.
 
Los correos de contacto son los del alumno si es mayor de edad y los del tutor legal en caso de que sea menor de edad. Los datos de alumnos y grupos se comparten a modo de ejemplo, pero los de asistencia y registro se han añadido al `.gitignore`. El archivo `.env` con las credenciales tampoco se sube al repositorio.
 
## 7. Limitaciones conocidas
 
- La asistencia se pasa por días, no por grupo. Esto se ha hecho para no añadir complejidad y tiempo de desarrollo al proyecto.
- Las ausencias se cuentan por registro, no por días distintos.
- El aviso de ausencia se realiza cada viernes, ya que no hay un registro de los correos a los que ya se les ha enviado el aviso durante el mes en curso.
- `PasarLista` utiliza `input()`, así que necesita a una persona delante y no se puede ejecutar de forma programada.
- Si un nodo falla, el motor lo registra en el log y se detiene, pero no devuelve ningún código de error.
- Los correos aparecen en el log.
- Quitar un nodo del JSON puede romper los que dependen de él.
- Los nodos no tienen tests propios.

## 8. Comparativa con n8n
Aunque se puede crear un programa como este sin usar herramientas extras, estas pueden aportar mucho valor. A continuación se detallan algunos de los beneficios de cada modelo.
 
**Ventajas del modelo de programación:**
- Control total sobre las funciones y funcionalidades.
- Creación de tests para confirmar el correcto funcionamiento del programa en varias situaciones.
- Sin límites ni costes de plataforma.
**Ventajas de usar herramientas extras (como n8n):**
- Interfaz visual que permite ver claramente el funcionamiento del programa.
- Integraciones fáciles con más plataformas.
- Posibilidad de añadir ejecuciones programadas mediante los "triggers" basados en el tiempo.
- Creación automática de un historial de ejecuciones completo.