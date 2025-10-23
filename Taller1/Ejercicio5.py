# Ejercicio propuesto 2
# Un productor de leche lleva el registro de lo que produce en litros, pero
# cuando entrega le pagan en galones. Realice un algoritmo, y represéntelo
# mediante un diagrama de flujo y el pseudocódigo, que ayude al productor
# a saber cuánto recibirá por la entrega de su producción de un día (1 galón
# =3.785 litros).

litros_vendidos = float(input("Ingrese la cantidad de litros vendidos: "))
valor_galon = float(input("Ingrese el valor por galón: "))

litros_a_galones = litros_vendidos / 3.785
total_pagar = litros_a_galones * valor_galon

print("Las ganancias son:", total_pagar)