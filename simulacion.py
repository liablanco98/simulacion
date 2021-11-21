import aleatorios as a
import sys

class Cocina:
    def __init__(self,caso,cierre,horarios_picos,l_nhp,l_hp):
        self.caso=caso #caso 0 cuando es pa dos empleados y 1 pa un extra en horarios picos
        self.t_cierre=cierre #minuto en que cierra el restaurante
        self.horarios_pico=horarios_picos #arreglo con los horarios picos
        self.l_nhp=l_nhp #es el lambda que estaremos empleando para la generacion de los tiempo de llegada de clientes en horario no pico
        self.l_hp=l_hp#es el lambda que estaremos empleando para la generacion de los tiempo de llegada de clientes en horario pico

    def inicializar_variables(self):
        self.t=0 #Tiempo general
        self.t_a=a.tiempo_llegada_cliente(self.l_nhp) #tiempo de arribo de pedidos (inicialmente como no es horario pico empleamos el valor de lambda correspondiente)
        self.t_s1=sys.maxsize   #tiempo de salidad de pedidos del empleado 1
        self.t_s2=sys.maxsize   #tiempo de salidad de pedidos del empleado 2
        self.consumidores=[] #esta lista es para almacenar a todos los clientes que son servidos en un dia
        self.n=0 #cantidad de clientes en espera a ser servidos
        self.activado_horario_pico=False # es un booleano para el caso alternativo en el que se va a activar si estamos en horario pico
        
        if self.caso:
            self.t_s3=sys.maxsize   #tiempo de salidad de pedidos del empleado 3
            self.N_s3=0   #cantidad de salidad de pedidos del empleado 3
            self.SS=[0,0,0] #( i1, i2, i3, .., in)i1 cliente en S1 (0 si no hay), i2 cliente en S2, i3, .., in la cola
        else:
            self.SS=[0,0] #( i1, i2, i3, .., in)i1 cliente en S1 (0 si no hay), i2 cliente en S2, i3, .., in la cola

        #Estas variables no se requieren en el programa solo se usan para garantizar 
        #que la cant arribos=cantidad de servidos
        self.N_a=0    #cantidad de arribo de pedidos
        self.N_s1=0   #cantidad de salidad de pedidos del empleado 1
        self.N_s2=0   #cantidad de salidad de pedidos del empleado 2

        self.current_lambda=self.l_nhp

    def intervalo_pico(self,valor):
        if valor>=self.horarios_pico[0] and valor<=self.horarios_pico[1]:
            return True,self.horarios_pico[0]
        if valor>=self.horarios_pico[2] and valor<=self.horarios_pico[3]:
            return True,self.horarios_pico[0]
        return False,None

    #DESCOMENTAR PARA VER RESULTADOS ASOCIADOS A UN DIA
    def print_resultados(self):
        #print(f'Cantidad de empleados : {3 if self.caso else 2}')
        #print(f'Lambda para horario no pico: {self.l_nhp},  Lambda para horario pico: {self.l_hp}')
        #print(f'Cantidad de consumidores que entraron : {self.N_a}')
        #print(f'Cantidad de consumidores que atendio el Primer Empleado : {self.N_s1}')
        #print(f'Cantidad de consumidores que atendio el Segundo Empleado : {self.N_s2}')
        #print(f'Cantidad de clientes que esperaron mas de 5 min en ser atendidos: {self.demora_mas_5_min}')
        print(f'Porciento de clientes que esperaron mas de 5 min en ser atendidos: {self.porciento}')

    def simulacion_cocina(self):
        self.inicializar_variables()
        #caso de 3 empledo en horario pico
        if self.caso:
            while True:
                m=min(self.t_a,self.t_s1,self.t_s2,self.t_s3)

                #si ya culmino el horario del local
                if m>self.t_cierre: break

                #este es el caso en que ya empezo el horario pico  o no para manejar con que valores de lambda se va a ir generando los tiempos de llegada
                ip,ip_i=self.intervalo_pico(m)
                if ip:
                    #Si se paso de un horario no pico a uno pico el empleado 3 tiene que empezar
                    # a tomar pedidos en espera xq esta en su horario de trabajo
                    if not self.activado_horario_pico and self.n>2:
                        self.SS[2]=self.SS[3]
                        del self.SS[3]
                        temp=a.tiempo_demora_fabricar(self.SS[2].tipo)
                        self.SS[2].t_preparacion=temp
                        self.t_s3=ip_i+temp
                        m=min(m,self.t_s3) 

                    self.activado_horario_pico=True
                    self.current_lambda=self.l_hp
                else: 
                    self.activado_horario_pico=False    
                    self.current_lambda=self.l_nhp

                #actualizar el tiempo general 
                self.t=m
                #se selecciona el correpondiente evento a ser analizado        
                if self.t==self.t_a:
                    self.arriba_pedido()
                elif self.t==self.t_s1:
                    self.sale_pedido_empleado1()
                elif self.t==self.t_s2:
                    self.sale_pedido_empleado2()
                elif self.t==self.t_s3:
                    self.sale_pedido_empleado3()       
        #caso dos empleados    
        else:
            while True:
                m=min(self.t_a,self.t_s1,self.t_s2)

                if m>self.t_cierre: break

                #este es el caso en que ya empezo el horario pico  o no
                ip,_=self.intervalo_pico(m)
                if ip:
                    self.current_lambda=self.l_hp
                    self.activado_horario_pico=True
                else: 
                    self.current_lambda=self.l_nhp
                    self.activado_horario_pico=False
                    
                #actualizar el tiempo general 
                self.t=m
                #se selecciona el correpondiente evento a ser analizado        
                if self.t==self.t_a:
                    self.arriba_pedido()
                elif self.t==self.t_s1:
                    self.sale_pedido_empleado1()
                elif self.t==self.t_s2:
                    self.sale_pedido_empleado2()
        
        #aun clientes esperando y ya culminado el horario del restaurante
        self.cierra_cocina()

        #calcular el porciento declientes que esperaron mas de 5 min
        total_clientes=len(self.consumidores)
        self.demora_mas_5_min=0
        for x in self.consumidores:
            temp=x.tiempo_espera()
            self.demora_mas_5_min+=1 if temp>5 else 0
        self.porciento= self.demora_mas_5_min/total_clientes 
        self.print_resultados()

    def arriba_pedido(self):
        self.N_a+=1
        c=Consumidor(self.t)
        t_at=a.tiempo_llegada_cliente(self.current_lambda)

        self.t_a=self.t+t_at   #genero el tiempo de llegada del proximo cliente
        #si un cliente llega despues de cerrado el local no es atendido
        if self.t_a>self.t_cierre: 
            self.t_a=sys.maxsize

        #Empleado 1 desocupado y no cola pendiente (no puede haber cola sino no estaria desocupado)   
        if self.SS[0]==0:
            t_temp=a.tiempo_demora_fabricar(c.tipo)
            c.t_preparacion=t_temp
            self.t_s1=self.t+t_temp
            self.SS[0]=c
        #Empleado 2 desocupado y no cola pendiente (no puede haber cola sino no estaria desocupado)   
        elif self.SS[1]==0:
            t_temp=a.tiempo_demora_fabricar(c.tipo)
            c.t_preparacion=t_temp
            self.t_s2=self.t+t_temp
            self.SS[1]=c
        #Caso 3 empleados, horario pico, Empleado 3 desocupado y no cola pendiente (no puede haber cola sino no estaria desocupado)
        elif self.caso and self.activado_horario_pico and self.SS[2]==0:
            t_temp=a.tiempo_demora_fabricar(c.tipo)
            c.t_preparacion=t_temp
            self.t_s3=self.t+t_temp
            self.SS[2]=c
        #Caso que hay cola pendiente
        else:
            self.SS.append(c)

        self.n+=1    
        
    def sale_pedido_empleado1(self):
        self.N_s1+=1
        self.SS[0].t_salida=self.t
        self.consumidores.append(self.SS[0])

        pos=3 if self.caso else 2

        #si no hay nadie esperando en la cola...
        if self.n<=2 or (self.n==3 and self.caso and self.t_s3!=sys.maxsize):
            self.SS[0]=0
            self.t_s1=sys.maxsize
        else:    
            temp1=self.SS[pos]
            del self.SS[pos]
            self.SS[0]=temp1    
            t_fab=a.tiempo_demora_fabricar(self.SS[0].tipo)
            self.SS[0].t_preparacion=t_fab
            self.t_s1=self.t+t_fab
        self.n-=1

    def sale_pedido_empleado2(self):
        self.N_s2+=1
        self.SS[1].t_salida=self.t
        self.consumidores.append(self.SS[1])

        pos=3 if self.caso else 2

        #si no hay nadie esperando en la cola...
        if self.n<=2 or (self.n==3 and self.caso and self.t_s3!=sys.maxsize):
            self.SS[1]=0
            self.t_s2=sys.maxsize
        else:    
            temp1=self.SS[pos]
            del self.SS[pos]
            self.SS[1]=temp1    
            t_fab=a.tiempo_demora_fabricar(self.SS[1].tipo)
            self.SS[1].t_preparacion=t_fab
            self.t_s2=self.t+t_fab
        self.n-=1

    def sale_pedido_empleado3(self):
        self.N_s3+=1
        self.SS[2].t_salida=self.t
        self.consumidores.append(self.SS[2])

        #si esta activado el horario pico implica que todavia el epleado tiene que tomar los pedidos
        if self.activado_horario_pico and self.n>3:
            temp1=self.SS[3]
            del self.SS[3]
            self.SS[2]=temp1    
            t_fab=a.tiempo_demora_fabricar(self.SS[2].tipo)
            self.SS[2].t_preparacion=t_fab
            self.t_s3=self.t+t_fab
        else:
            self.SS[2]=0
            self.t_s3=sys.maxsize    
        self.n-=1     
                
    def cierra_cocina(self):
        #Por cada cliente pendiente ir tomando su pedido pero este caso siempre sera para dos empleados
        # porque el ultimo hr pico termina antes del cierre, y el proceso de cierre por cada cliente es analogo al proceso en que sirve
        while True:
            self.t=min(self.t_s1,self.t_s2)
            if self.t==sys.maxsize: break
            if self.t==self.t_s1:
                self.sale_pedido_empleado1()
            else :
                self.sale_pedido_empleado2()

class Consumidor:
    #Un consumidor posee
    #Tipo: sandwich=0 o sushi=1
    #llegada : momento en que arriba
    #salida: momento en que es servido
    def __init__(self,  llegada):
        self.tipo=a.tipo_de_cliente()
        self.t_llegada=llegada
        self.t_salida=None
        self.t_preparacion=None

    def tiempo_espera(self):
        return self.t_salida-self.t_llegada-self.t_preparacion

if __name__=="__main__":

    #Para lambda en horario no pico =0.2 y en pico =0.5 
    l_hp=0.5
    l_nhp=0.2

    print("Para lambda en horario no pico: 0.2 y en pico : 0.5 ")
    print("Con 3 empleados ")
    C1=Cocina(1,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C1.simulacion_cocina()
        mas_5+=C1.demora_mas_5_min
        total+=C1.N_a
    mes_1=mas_5/total        

    print()
    print()
    print("Para lambda en horario no pico: 0.2 y en pico : 0.5 ")
    print("Con 2 empleados ")
    C2=Cocina(0,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C2.simulacion_cocina()
        mas_5+=C2.demora_mas_5_min
        total+=C2.N_a
    mes_2=mas_5/total    

    dif_1=mes_2-mes_1

    
    #Para lambda en horario no pico =0.5 y en pico =1 
    l_hp=1
    l_nhp=0.5

    print()
    print()
    print("Para lambda en horario no pico: 0.5 y en pico : 1 ")
    print("Con 3 empleados ")
    C1=Cocina(1,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C1.simulacion_cocina()
        mas_5+=C1.demora_mas_5_min
        total+=C1.N_a
    mes_1=mas_5/total        
    
    print()
    print()
    print("Para lambda en horario no pico: 0.5 y en pico : 1 ")
    print("Con 2 empleados ")
    C2=Cocina(0,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C2.simulacion_cocina()
        mas_5+=C2.demora_mas_5_min
        total+=C2.N_a
    mes_2=mas_5/total    

    dif_2=mes_2-mes_1

    #Para lambda en horario no pico =0.5 y en pico =1.5 
    l_hp=1.5
    l_nhp=0.5

    print()
    print()
    print("Para lambda en horario no pico: 0.5 y en pico : 1.5 ")
    print("Con 3 empleados ")
    C1=Cocina(1,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C1.simulacion_cocina()
        mas_5+=C1.demora_mas_5_min
        total+=C1.N_a
    mes_1=mas_5/total        

    print()
    print()
    print("Para lambda en horario no pico: 0.5 y en pico : 1.5 ")
    print("Con 2 empleados ")
    C2=Cocina(0,660,[90,210,420,540],l_nhp,l_hp)
    mas_5=0
    total=0
    for x in range(30):
        temp=C2.simulacion_cocina()
        mas_5+=C2.demora_mas_5_min
        total+=C2.N_a
    mes_2=mas_5/total    

    dif_3=mes_2-mes_1

    print()
    print(f'Lambda para horario no pico: 0.2,  Lambda para horario pico: 0.5, la diferencia entre 2 y 3 empleados es {dif_1}')
    print(f'Lambda para horario no pico: 0.5,  Lambda para horario pico: 1, la diferencia entre 2 y 3 empleados es {dif_2}')
    print(f'Lambda para horario no pico: 0.5,  Lambda para horario pico: 1.5, la diferencia entre 2 y 3 empleados es {dif_3}')
