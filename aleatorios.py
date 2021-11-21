from math import log
import random as r

# X ∼ U(a, b)~(b − a)U + a     
def distribucion_uniforme(a,b):
    u=r.uniform(0,1)
    x = a + (b - a) * u
    return x

#X ~ −(1/λ)ln(U)
def distribucion_exponencial(l):
    u=r.uniform(0,1)
    return -(1/l)*log(u)

#Para esto como estamos en presencia de una variable aleatoria discreta donde solo 
# una de las dos opciones podemos seterminar el tipo de consumidor a partir del uso de la 
#propiedad choice de random (part del codigo comentada), o del uso de la funcion de Bernoulli
# que fue la opcion seleccionada pero ambas son igualmente validas 
def tipo_de_cliente():
    #Empleo del random uniform que ofrece python
    #return r.choice([0,1])
    
    # X ∼ Ber(p)
    u=r.uniform(0,1)
    if u<=0.5: return 0
    return 1

#Como el tiempo que demora preparar un sandwich sigue una distribucion uniforme
# en el intervalo [3,5], hacemos uso de dicha funcion "distribucion_uniforme" 
#implementada anteriormente
def tiempo_demora_sandwich():
    return distribucion_uniforme(3,5)

#Como el tiempo que demora preparar un sushi sigue una distribucion uniforme
# en el intervalo [5,8], hacemos uso de dicha funcion "distribucion_uniforme" 
#implementada anteriormente
def tiempo_demora_sushi():
    return distribucion_uniforme(5,8)

#Es un metodo que se le pasa el tipo de producto a fabricar y devuelve el tiempo que tomaria 
#teniendo en cuenta las correspondientes funciones de distribucion
def tiempo_demora_fabricar(tipo):
    if tipo:return tiempo_demora_sushi()
    return tiempo_demora_sandwich()

#Es el metodo que determina los tiempos que demorarioan en llegar los consumidores a partir
#de un determinado parametro de lambda, a partir del uso de su correspondiente
#funcion de distribucion q es la exponencial
def tiempo_llegada_cliente(l):
    return distribucion_exponencial(l)
