# Una empresa constructora vende terrenos con la forma A de la figura 2.2.
# Realice un algoritmo y represéntelo mediante un diagrama de flujo y el
# pseudocódigo para obtener el área respectiva de un terreno de medidas
# de cualquier valor.

# Para resolver este problema se debe identificar que la forma A está
# compuesta por dos figuras: un triángulo de base B y de altura (A - С);
# y por otro lado, un rectángulo que tiene base B y altura C. Con estas
# consideraciones se puede establecer la tabla 2.6 con las variables que se
# requieren para implementar el algoritmo de solución.


base_mayor = float(input("Ingrese la base mayor del trapecio: "))
base_menor = float(input("Ingrese la base menor del trapecio: "))
altura = float(input("Ingrese la altura del trapecio: "))

area_trapecio = (base_menor * altura) + ((base_mayor - base_menor) * altura) / 2

print("El área del trapecio es:", area_trapecio)