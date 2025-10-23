# Ejercicio propuesto 4
# “La langosta ahumada” es una empresa dedicada a ofrecer banquetes; sus
# tarifas son las siguientes: el costo de platillo por persona es de $95.00,
# pero si el número de personas es mayor a 200 pero menor o igual a 300,
# el costo es de $85.00. Para más de 300 personas el costo por platillo es de
# $75.00. Se requiere un algoritmo que ayude a determinar el presupuesto
# que se debe presentar a los clientes que deseen realizar un evento.
# Mediante pseudocódigo, diagrama de flujo y un diagrama N/S represente su
# solución.

cantidad_personas = int(input("Ingrese la cantidad de personas en el banquete: "))
if 0 < cantidad_personas < 200:
    costo_por_persona = 95
elif cantidad_personas <= 300:
    costo_por_persona = 85
else:
    costo_por_persona = 75
costo_total = cantidad_personas * costo_por_persona

print("El costo total del banquete es:", costo_total)