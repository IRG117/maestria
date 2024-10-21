import json
import os

class SensorTemp:
    def _init_(self, temp_actual):
        self.temp_actual = temp_actual
        self.temp_objetivo = 25  # Temperatura objetivo en °C

    def actualizar_temp(self, nueva_temp):
        self.temp_actual = nueva_temp


class SensorHumedad:
    def _init_(self, humedad_actual):
        self.humedad_actual = humedad_actual
        self.humedad_objetivo = 50  # Humedad objetivo en porcentaje

    def actualizar_humedad(self, nueva_humedad):
        self.humedad_actual = nueva_humedad


class SensorNutrientes:
    def _init_(self, nivel_actual):
        self.nivel_actual = nivel_actual
        self.nivel_objetivo = 7  # Nivel objetivo de pH (valor entre 6 y 8)

    def actualizar_nivel(self, nuevo_nivel):
        self.nivel_actual = nuevo_nivel


class ActuadorLuz:
    def _init_(self, estado_luz):
        self.estado_luz = estado_luz  # True: encendida, False: apagada

    def ajustar_luz(self, encender):
        self.estado_luz = encender


class ActuadorNutrientes:
    def _init_(self, nutrientes):
        self.nutrientes = nutrientes  # True: añadiendo nutrientes, False: no

    def ajustar_nutrientes(self, añadir):
        self.nutrientes = añadir


class ControladorInvernadero:
    def _init_(self):
        self.sensor_tempera = SensorTemp(23)  # Temperatura inicial
        self.sensor_humedad = SensorHumedad(45)  # Humedad inicial
        self.sensor_nutrientes = SensorNutrientes(7.5)  # Nutrientes iniciales (pH)
        self.actuador_luz = ActuadorLuz(False)  # Luz apagada al inicio
        self.actuador_nutrientes = ActuadorNutrientes(False)  # Nutrientes no añadidos al inicio

    def controlar(self):
        # Controlar temperatura
        if self.sensor_tempera.temp_actual < self.sensor_tempera.temp_objetivo:
            print("Ajustando calefacción...")
            self.sensor_tempera.actualizar_temp(self.sensor_tempera.temp_actual + 1)
        elif self.sensor_tempera.temp_actual > self.sensor_tempera.temp_objetivo:
            print("Ajustando refrigeración...")
            self.sensor_tempera.actualizar_temp(self.sensor_tempera.temp_actual - 1)

        # Controlar humedad
        if self.sensor_humedad.humedad_actual < self.sensor_humedad.humedad_objetivo:
            print("Activando humidificador...")
            self.sensor_humedad.actualizar_humedad(self.sensor_humedad.humedad_actual + 1)
        elif self.sensor_humedad.humedad_actual > self.sensor_humedad.humedad_objetivo:
            print("Activando deshumidificador...")
            self.sensor_humedad.actualizar_humedad(self.sensor_humedad.humedad_actual - 1)

        # Controlar nivel de nutrientes
        if self.sensor_nutrientes.nivel_actual < self.sensor_nutrientes.nivel_objetivo:
            print("Añadiendo nutrientes...")
            self.sensor_nutrientes.actualizar_nivel(self.sensor_nutrientes.nivel_actual + 0.1)
            self.actuador_nutrientes.ajustar_nutrientes(True)
        elif self.sensor_nutrientes.nivel_actual > self.sensor_nutrientes.nivel_objetivo:
            print("Reduciendo nutrientes...")
            self.sensor_nutrientes.actualizar_nivel(self.sensor_nutrientes.nivel_actual - 0.1)
            self.actuador_nutrientes.ajustar_nutrientes(False)

        # Controlar luz 
        if self.sensor_tempera.temp_actual < 22 and not self.actuador_luz.estado_luz:
            print("Encendiendo luz...")
            self.actuador_luz.ajustar_luz(True)
        elif self.sensor_tempera.temp_actual > 22 and self.actuador_luz.estado_luz:
            print("Apagando luz...")
            self.actuador_luz.ajustar_luz(False)



class ManejoArchivos:
    def _init_(self, archivo):
        self.archivo = archivo
        # Crear archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w') as f:
                json.dump([], f)

    def alta(self, datos):
        # Cargar los datos existentes
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        # Añadir nuevos datos
        registros.append(datos)
        # Guardar los cambios
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def baja(self, indice):
        # Cargar los datos existentes
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        # Eliminar por índice
        if 0 <= indice < len(registros):
            registros.pop(indice)
        # Guardar los cambios
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def modificar(self, indice, nuevos_datos):
        # Cargar los datos existentes
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        # Modificar el registro por índice
        if 0 <= indice < len(registros):
            registros[indice] = nuevos_datos
        # Guardar los cambios
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def consultar(self):
        # Cargar los datos existentes
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        return registros



def mostrar_menu():
    print("\nMenú del Brazo Robótico:")
    print("1. Alta (Guardar nueva posición)")
    print("2. Baja (Eliminar una posición por índice)")
    print("3. Modificación (Modificar una posición por índice)")
    print("4. Consultas (Mostrar todas las posiciones guardadas)")
    print("5. Salir")
    return input("Seleccione una opción: ")

def main():
    invernadero = ControladorInvernadero()
    archivo = ManejoArchivos("variables.json")


    while True:
        opcion = mostrar_menu()

        if opcion == "1":  # Alta
            # Captura nuevos valores de variables
            try:
                temp = float(input("Temperatura: "))
                hum = float(input("Porcentaje de Humedad: "))
                nut = float(input("Nutrientes: "))
                luz = float(input("Luz: "))
                invernadero.controlar([temp, hum, nut, luz])
                archivo.alta(indice, invernadero.controlar())   
            except ValueError:
                print("Error: Por favor ingrese valores numéricos válidos.")

        elif opcion == "2":  # Baja
            try:
                indice = int(input("Ingrese el índice de la posición que desea eliminar: "))
                archivo.baja(indice)
                print("Posición eliminada exitosamente.")
            except ValueError:
                print("Error: Ingrese un índice válido.")
            except IndexError:
                print("Error: Índice fuera de rango.")

        elif opcion == "3":  # Modificación
            try:
                indice = int(input("Ingrese el índice de la posición que desea modificar: "))
                temp = float(input("Nueva temperatura: "))
                hum = float(input("Nuevo porcentaje de humedad: "))
                nut = float(input("Nuevo porcentaje de nutrientes: "))
                luz = float(input("Estatuz luz: "))
                invernadero.controlar([temp, hum, nut, luz])
                archivo.modificar(indice, invernadero.controlar())
                print("Variables modificadas exitosamente.")
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.")
            except IndexError:
                print("Error: Índice fuera de rango.")
        
        elif opcion == "4":  # Consultas
            variables = archivo.consultar()
            if variables:
                for i, vari in enumerate(variables):
                    print(f"Variable {i}: Humedad={vari['humedad']}, Temperatura={vari['temperatura']}, Nutrientes={vari['nutrientes']}, Luz={vari['luz']}")
            else:
                print("No hay variables guardadas.")
        
        elif opcion == "5":  # Salir
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor seleccione una opción del menú.")

if __name__ == "_main_":
    main()


controlador = ControladorInvernadero()


# Simulando el monitoreo y control en un bucle
for i in range(10):
    print(f"Estado actual: Temp: {controlador.sensor_tempera.temp_actual}°C, "
          f"Humedad: {controlador.sensor_humedad.humedad_actual}%, "
          f"Nutrientes: {controlador.sensor_nutrientes.nivel_actual} pH, "
          f"Luz: {'Encendida' if controlador.actuador_luz.estado_luz else 'Apagada'}, "
          f"Nutrientes: {'Añadiendo' if controlador.actuador_nutrientes.nutrientes else 'No añadiendo'}")
    
    # Ejecutar el controlador
    controlador.controlar()