import json
import os
import flet as ft

class SensorTemp:
    def __init__(self, temp_actual):
        self.temp_actual = temp_actual
        self.temp_objetivo = 25  # Temperatura objetivo en °C

    def actualizar_temp(self, nueva_temp):
        self.temp_actual = nueva_temp

class SensorHumedad:
    def __init__(self, humedad_actual):
        self.humedad_actual = humedad_actual
        self.humedad_objetivo = 50  # Humedad objetivo en porcentaje

    def actualizar_humedad(self, nueva_humedad):
        self.humedad_actual = nueva_humedad

class SensorNutrientes:
    def __init__(self, nivel_actual):
        self.nivel_actual = nivel_actual
        self.nivel_objetivo = 7  # Nivel objetivo de pH (valor entre 6 y 8)

    def actualizar_nivel(self, nuevo_nivel):
        self.nivel_actual = nuevo_nivel

class ActuadorLuz:
    def __init__(self, estado_luz):
        self.estado_luz = estado_luz  # True: encendida, False: apagada

    def ajustar_luz(self, encender):
        self.estado_luz = encender

class ActuadorNutrientes:
    def __init__(self, nutrientes):
        self.nutrientes = nutrientes  # True: añadiendo nutrientes, False: no

    def ajustar_nutrientes(self, añadir):
        self.nutrientes = añadir

class ControladorInvernadero:
    def __init__(self):
        self.sensor_temperatura = SensorTemp(23)  # Temperatura inicial
        self.sensor_humedad = SensorHumedad(45)  # Humedad inicial
        self.sensor_nutrientes = SensorNutrientes(7.5)  # Nutrientes iniciales (pH)
        self.actuador_luz = ActuadorLuz(False)  # Luz apagada al inicio
        self.actuador_nutrientes = ActuadorNutrientes(False)  # Nutrientes no añadidos al inicio

    def controlar(self):
        # Controlar temperatura
        if self.sensor_temperatura.temp_actual < self.sensor_temperatura.temp_objetivo:
            self.sensor_temperatura.actualizar_temp(self.sensor_temperatura.temp_actual + 1)
        elif self.sensor_temperatura.temp_actual > self.sensor_temperatura.temp_objetivo:
            self.sensor_temperatura.actualizar_temp(self.sensor_temperatura.temp_actual - 1)

        # Controlar humedad
        if self.sensor_humedad.humedad_actual < self.sensor_humedad.humedad_objetivo:
            self.sensor_humedad.actualizar_humedad(self.sensor_humedad.humedad_actual + 1)
        elif self.sensor_humedad.humedad_actual > self.sensor_humedad.humedad_objetivo:
            self.sensor_humedad.actualizar_humedad(self.sensor_humedad.humedad_actual - 1)

        # Controlar nivel de nutrientes
        if self.sensor_nutrientes.nivel_actual < self.sensor_nutrientes.nivel_objetivo:
            self.sensor_nutrientes.actualizar_nivel(self.sensor_nutrientes.nivel_actual + 0.1)
            self.actuador_nutrientes.ajustar_nutrientes(True)
        elif self.sensor_nutrientes.nivel_actual > self.sensor_nutrientes.nivel_objetivo:
            self.sensor_nutrientes.actualizar_nivel(self.sensor_nutrientes.nivel_actual - 0.1)
            self.actuador_nutrientes.ajustar_nutrientes(False)

        # Controlar luz 
        if self.sensor_temperatura.temp_actual < 22 and not self.actuador_luz.estado_luz:
            self.actuador_luz.ajustar_luz(True)
        elif self.sensor_temperatura.temp_actual > 22 and self.actuador_luz.estado_luz:
            self.actuador_luz.ajustar_luz(False)

class ManejoArchivos:
    def __init__(self, archivo):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w') as f:
                json.dump([], f)

    def alta(self, datos):
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        registros.append(datos)
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def baja(self, indice):
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        if 0 <= indice < len(registros):
            registros.pop(indice)
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def modificar(self, indice, nuevos_datos):
        with open(self.archivo, 'r') as f:
            registros = json.load(f)
        if 0 <= indice < len(registros):
            registros[indice] = nuevos_datos
        with open(self.archivo, 'w') as f:
            json.dump(registros, f, indent=4)

    def consultar(self):
        with open(self.archivo, 'r') as f:
            return json.load(f)

def main(page: ft.Page):
    # Inicializar componentes
    invernadero = ControladorInvernadero()
    archivo = ManejoArchivos("variables.json")
    resultado = ft.Text()

    # Función para mostrar las variables almacenadas
    def mostrar_variables():
        variables = archivo.consultar()
        lista_variables.controls.clear()
        if variables:
            for i, var in enumerate(variables):
                lista_variables.controls.append(ft.Text(f"Variable {i}: Temp={var['temperatura']}°C, "
                                                        f"Humedad={var['humedad']}%, "
                                                        f"Nutrientes={var['nutrientes']} pH, "
                                                        f"Luz={'Encendida' if var['luz'] else 'Apagada'}"))
        else:
            lista_variables.controls.append(ft.Text("No hay variables guardadas."))
        page.update()

    # Función para limpiar campos de texto
    def limpiar_campos():
        temperatura.value = ""
        humedad.value = ""
        nutrientes.value = ""
        luz.value = ""
        indice_baja.value = ""
        indice_modificar.value = ""

    # Funciones para alta, baja y modificación de variables
    def alta_click(e):
        try:
            temp = float(temperatura.value)
            hum = float(humedad.value)
            nut = float(nutrientes.value)
            luz_estado = luz.value.lower() == "encender"
            datos = {
                "temperatura": temp,
                "humedad": hum,
                "nutrientes": nut,
                "luz": luz_estado
            }
            archivo.alta(datos)
            invernadero.controlar()
            resultado.value = "Variables guardadas exitosamente."
            mostrar_variables()
        except ValueError:
            resultado.value = "Error: Ingrese valores numéricos válidos."
        page.update()

    def baja_click(e):
        try:
            indice = int(indice_baja.value)
            archivo.baja(indice)
            resultado.value = "Posición eliminada exitosamente."
            mostrar_variables()
        except ValueError:
            resultado.value = "Error: Ingrese un índice válido."
        page.update()

    def modificar_click(e):
        try:
            indice = int(indice_modificar.value)
            temp = float(temperatura.value)
            hum = float(humedad.value)
            nut = float(nutrientes.value)
            luz_estado = luz.value.lower() == "encender"
            datos = {
                "temperatura": temp,
                "humedad": hum,
                "nutrientes": nut,
                "luz": luz_estado
            }
            archivo.modificar(indice, datos)
            invernadero.controlar()
            resultado.value = "Posición modificada exitosamente."
            mostrar_variables()
        except ValueError:
            resultado.value = "Error: Ingrese valores numéricos válidos."
        page.update()

    # Elementos de la interfaz
    temperatura = ft.TextField(label="Temperatura (°C)")
    humedad = ft.TextField(label="Humedad (%)")
    nutrientes = ft.TextField(label="Nutrientes (pH)")
    luz = ft.TextField(label="Luz (encender/apagar)")
    indice_baja = ft.TextField(label="Índice para eliminar")
    indice_modificar = ft.TextField(label="Índice para modificar")
    
    lista_variables = ft.Column(scroll="adaptive")

    # Menú de opciones
    def cambiar_vista(menu_item):
        container_opciones.controls.clear()
        resultado.value = ""
        if menu_item == "Alta":
            container_opciones.controls.extend([temperatura, humedad, nutrientes, luz, ft.ElevatedButton("Guardar Variables", on_click=alta_click)])
        elif menu_item == "Baja":
            container_opciones.controls.extend([indice_baja, ft.ElevatedButton("Eliminar Variables", on_click=baja_click)])
        elif menu_item == "Modificación":
            container_opciones.controls.extend([indice_modificar, temperatura, humedad, nutrientes, luz, ft.ElevatedButton("Modificar Variables", on_click=modificar_click)])
        elif menu_item == "Consultas":
            mostrar_variables()
        page.update()

    # Contenedor para los menús y opciones
    container_opciones = ft.Column()

    # Interfaz principal
    page.add(
        ft.Text("Control de Invernadero", style="headlineMedium"),
        ft.Row([ft.ElevatedButton(text="Alta", on_click=lambda e: cambiar_vista("Alta")),
                ft.ElevatedButton(text="Baja", on_click=lambda e: cambiar_vista("Baja")),
                ft.ElevatedButton(text="Modificación", on_click=lambda e: cambiar_vista("Modificación")),
                ft.ElevatedButton(text="Consultas", on_click=lambda e: cambiar_vista("Consultas"))]),
        container_opciones,
        resultado,
        ft.Text("Variables Guardadas:", style="headlineSmall"),
        lista_variables
    )

    # Inicializar con la lista de variables guardadas
    mostrar_variables()

ft.app(target=main, view="web_browser")
