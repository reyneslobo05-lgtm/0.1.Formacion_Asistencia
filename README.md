Este proyecto es una automatización para pasar lista en una academia. 

Dentro del directorio data/ se encuentra:
- data_faker.py : un generador de Mock Data, para garantizar que no se usan datos sensibles reales 
- models.py : script con las clases Alumno, Grupo y RegistroAsistencia.
- lectura.py : con la función leer_alumnos, obtiene cada fila de alumnos csv, verifica que el formato de los datos (email) sean correctos y devuelve una lista con los datos de los alumnos o un código explicativo del error. 