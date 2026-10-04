from faker import Faker
import csv
from pathlib import Path
Faker.seed(42)

RUTA = Path(__file__).parent / 'alumnos.csv'
fake = Faker()
with open(RUTA, mode='w', newline="", encoding='utf-8') as data:
    writer = csv.writer(data)
    writer.writerow(['id', 'nombre', 'apellido', 'email', 'es_menor', 'grupo_id'])
    for i in range(1, 41):
        nombre = fake.first_name()
        apellido = fake.last_name()
        email = f"{nombre.lower()}.{apellido.lower()}.{i}@example.com"
        es_menor = fake.boolean(chance_of_getting_true=70)
        grupo_id = fake.random_int(min=1, max=7)
        writer.writerow([i, nombre, apellido, email, es_menor, grupo_id])

