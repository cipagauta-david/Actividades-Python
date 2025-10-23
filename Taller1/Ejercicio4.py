import math

# Se requiere obtener el área de la figura 2.3 de la forma A. Para resolver
# este problema se puede partir de que est formada por tres figuras: dos
# tri+ángulos rectángulos, con H como hipotenusa y R como uno de los cate-
# tos, que también es el radio de la otra figura, una semicircunferencia que
# forma la parte circular (ver forma B). Realice un algoritmo para resolver el
# problema y represéntelo mediante el diagrama de flujo y el pseudocodigo.


# Por lo tanto, para poder resolver el problema, se tiene que calcular
# el cateto faltante, que es la altura del triángulo, con ésta se puede
# calcular el área del triángulo, y para obtener el área total triangular se multi-
# plicara por dos. Por otro lado, para calcular el área de la parte circular,
# se calcula el área de la circunferencia y luego se divide entre dos, ya que
# representa solo la mitad del circulo. De este análisis se puede obtener la
# tabla 2.7, que contiene las variables requeridas para plantear el algoritmo
# con la solución respectiva.

radio_semicirculo = float(input("Ingrese el radio del semi círculo: "))
hipotenusa = float(input("Ingrese la hipotenusa del triángulo: "))

area_semicirculo = (3.1416 * radio_semicirculo**2) / 2
area_triangulo = math.sqrt(hipotenusa**2 - radio_semicirculo**2) * radio_semicirculo
area_total = area_semicirculo + area_triangulo

print("El área total de la figura es:", area_total)
