# Un estudiante realiza cuatro exámenes durante el semestre, los cuales tienen
# la misma ponderación. Realice el pseudocódigo y el diagrama de flujo
# que representen el algoritmo correspondiente para obtener el promedio
# de las calificaciones obtenidas.

notas = []

for i in range(4):
    nota = float(input("Ingrese una nota: "))
    notas.append(nota)

promedio = sum(notas) / len(notas)

print("El promedio de las notas es:", promedio)