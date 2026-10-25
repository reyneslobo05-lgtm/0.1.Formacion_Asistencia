Este proyecto es una automatización para pasar lista en una academia. 

Dentro del directorio data/ se encuentra:
- data_faker.py : un generador de Mock Data, para garantizar que no se usan datos sensibles reales 
- models.py : script con las clases Alumno, Grupo y RegistroAsistencia.
- lectura.py : con la función leer_alumnos, obtiene cada fila de alumnos csv, verifica que el formato de los datos (email) sean correctos y devuelve una lista con los datos de los alumnos o un código explicativo del error. 


RGPD:
- Todos los datos usados son falsos
- Los correos de contacto son para el alumno si este es mayor de edad y para el tutor legal en caso de que este sea menor de edad. 

Futuro desarrollo:

- pasar lista a los grupos seleccionados, no a todos los del día.
- mejorar el buscador para ver las ausencias. Muy simple por ahora. Faltaría saber a quién se le ha enviado ya el mensaje de ausencias. Actualmente el conteo se hace por registro, no por días diferentes. Mejora pendiente para next steps. 

