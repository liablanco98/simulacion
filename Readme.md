#### Este programa simula el problema de la Cocina de Kojo's (ver  `Problema.md`).

Correr el comando:

``` python
py -3 simulacion.py
```

Que lleva a cabo la  simulación de este problema en un mes (30 días) y compara los resultados para dos y tres empleados (da la diferencia del porciento de consumidores que se demora más de 5 minutos en ser atendido cuando se tienen solo dos empleados y cuando se tiene un tercer empleado en los horarios picos) para tres valores de $\lambda$ diferentes (pueden ser modificados):

- $\lambda$ para horarios no pico = 0.2 y $\lambda$ para horarios pico = 0.5.
- $\lambda$ para horarios no pico = 0.5 y $\lambda$ para horarios pico = 1.
- $\lambda$ para horarios no pico = 0.5 y $\lambda$ para horarios pico = 1.5.

En `aleatorios.py` se encuentran las funciones asociadas a la generaciones de variables aleatorias que se requieren.

En `simulacion.py `  se encuentran las funciones asociadas al problema, si se requiere la simulación para un solo día y no para un mes, quitar lo comentado en la función `prin_resultados` de la clase `Cocina`.

En `resultados.txt` se pueden observar los resultados que se obtuvieron de una vez en que fue ejecutado el comando`py -3 simulacion.py`.