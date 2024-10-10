class Bateria:
    def __init__(self,capacidad_actual, capaidad_Max, eficiencia_carga):
        self.capacidad_actual= capacidad_actual
        self.capacidad_Max= capaidad_Max
        self.eficicienia_carga= eficiencia_carga
        self.temperatura= 20

    def actualizar_nivel_de_carga(self,nivel_carga):
        self.nivel_carga= nivel_carga


    def __str__(self):
        return f"Bateria: {self.capacidad_actual}Khw, {self.temperatura}°c,{self.capacidad_Max}khw, {self.eficicienia_carga}km/khw"




class Motor:
    def __init__(self,consumo_de_energia,potencia):
        self.consumo_de_energia= consumo_de_energia
        self.potencia= potencia
        self.estado= "Apagado"

    def encender(self):
        self.estado= "Encendido"

    def apagar(self):
        self.estado= "Apagado"

    def __str__(self):
        return f"Motor Eléctrico: {self.potencia} kW,{self.consumo_de_energia}%, {self.estado}"




class GestorEnergia:
    def __init__(self,bateria,motor_electrico):
        self.bateria= bateria
        self.motor_electrico= motor_electrico
        self.consumo_energia = 0  
        self.estado = "Apagado"

    def encender(self):
        self.motor_electrico.encender()
        self.estado = "Encendido"

    def apagar(self):
        self.motor_electrico.apagar()
        self.estado = "Apagado"

    def actualizar_consumo_energia(self, consumo_energia):
        self.consumo_energia = consumo_energia

    def __str__(self):
        return f"Sistema de Gestión de Energía: {self.estado},Consumo: {self.consumo_energia} kWh"









bateria = Bateria(60, 80, 50)
motor_electrico = Motor(150, 90)
sistema_gestion_energia = GestorEnergia(bateria, motor_electrico)


print(sistema_gestion_energia)
print(motor_electrico)
print(bateria)

sistema_gestion_energia.encender()
print(sistema_gestion_energia)

sistema_gestion_energia.actualizar_consumo_energia(10)
print(sistema_gestion_energia)

