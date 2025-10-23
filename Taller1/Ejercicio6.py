# Ejercicio propuesto 3
# Almacenes “El harapiento distinguido” tiene una promoción: a todos los
# trajes que tienen un precio superior a $2500.00 se les aplicará un descuen-
# to de 15 %, a todos los demás se les aplicará sólo 8 %. Realice un algoritmo
# para determinar el precio final que debe pagar una persona por comprar
# un traje y de cuánto es el descuento que obtendrá. Represéntelo mediante
# el pseudocódigo, el diagrama de flujo y el diagrama N/S.

valor_traje = float(input("Ingrese el valor del traje: "))
if valor_traje > 2500:
    descuento = valor_traje * 0.15
else:
    descuento = valor_traje * 0.08

valor_total = valor_traje - descuento

print("El descuento es:", descuento)
print("El precio final del traje es:", valor_total)