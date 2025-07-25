import os
import time

# --- Clase para el Nodo (Paciente) ---
class Paciente:
    """
    Representa un nodo en la lista enlazada. Contiene los datos
    del paciente y un puntero al siguiente.
    """
    def __init__(self, nombre, edad, prioridad):
        self.nombre = nombre
        self.edad = edad
        self.prioridad = prioridad
        self.siguiente = None  # Puntero al siguiente paciente en la lista

# --- Clase para la Cola de Espera (Lista Enlazada Optimizada) ---
class ColaDeEspera:
    """
    Implementa una cola (Queue) con una lista enlazada. Utiliza punteros
    a la cabeza y a la cola para operaciones FIFO eficientes.
    """
    def __init__(self):
        self.cabeza = None  # El frente de la cola (quién será atendido)
        self.cola = None    # El final de la cola (dónde se forman los nuevos)
        self.contador = 0   # Para saber el tamaño de la cola

    def agregar_paciente(self, nombre, edad, prioridad):
        """
        Añade un paciente al final de la cola (Enqueue).
        Gracias al puntero 'self.cola', esta operación es O(1).
        """
        nuevo_paciente = Paciente(nombre, edad, prioridad)
        if self.esta_vacia():
            # Si la cola está vacía, el nuevo paciente es cabeza y cola
            self.cabeza = nuevo_paciente
            self.cola = nuevo_paciente
        else:
            # El 'siguiente' del actual último apunta al nuevo
            self.cola.siguiente = nuevo_paciente
            # El nuevo paciente es ahora la nueva cola
            self.cola = nuevo_paciente
        
        self.contador += 1
        print(f"\n>> INFO: {nombre} se ha formado al final de la cola.")

    def atender_paciente(self):
        """
        Atiende al paciente del frente de la cola (Dequeue).
        Gracias al puntero 'self.cabeza', esta operación es O(1).
        """
        if self.esta_vacia():
            print("\n>> INFO: No hay pacientes en la cola para atender.")
            return

        # Se obtiene el paciente al frente de la cola
        paciente_atendido = self.cabeza
        
        print("\n" + "*"*40)
        print("   ATENDIENDO AL SIGUIENTE PACIENTE...")
        print("*"*40)
        print(f"   Nombre:    {paciente_atendido.nombre}")
        print(f"   Edad:      {paciente_atendido.edad}")
        print(f"   Prioridad: {paciente_atendido.prioridad.capitalize()}")
        print("*"*40)

        # Se avanza la cabeza al siguiente en la cola
        self.cabeza = self.cabeza.siguiente
        
        # Si la cabeza es None, la cola quedó vacía
        if self.cabeza is None:
            self.cola = None

        self.contador -= 1
        return paciente_atendido

    def mostrar_lista_actual(self):
        """
        Muestra el estado completo de la cola.
        Es una operación O(n) porque debe recorrer toda la lista.
        """
        if self.esta_vacia():
            print("\n>> La cola de espera está vacía.")
            return

        print("\n" + "="*45)
        print("      COLA DE ESPERA DE PACIENTES (FIFO)")
        print("="*45)
        print(f"{'Orden':<7}{'Nombre':<15}{'Edad':<7}{'Prioridad'}")
        print("-"*45)
        
        actual = self.cabeza
        orden = 1
        while actual:
            print(f"{orden:<7}{actual.nombre:<15}{actual.edad:<7}{actual.prioridad.capitalize()}")
            actual = actual.siguiente
            orden += 1
        print("="*45)
        print(f"Total de pacientes en espera: {self.contador}")

    def esta_vacia(self):
        """Chequea si la cola no tiene pacientes."""
        return self.cabeza is None

# --- Interfaz de Consola ---
def main():
    sistema = ColaDeEspera()
    
    # Datos de ejemplo para iniciar
    print("Cargando sistema con pacientes iniciales...")
    sistema.agregar_paciente("Ana Lopez", 45, "normal")
    sistema.agregar_paciente("Carlos Vera", 67, "urgente")
    sistema.agregar_paciente("Sofia Marin", 22, "normal")
    time.sleep(1)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n🏥 === Sistema de Cola de Pacientes (FIFO) ===")
        print("1. Agregar paciente a la cola")
        print("2. Atender siguiente paciente")
        print("3. Mostrar cola de espera actual")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese nombre del paciente: ")
            edad = int(input("Ingrese edad del paciente: "))
            prioridad = input("Ingrese prioridad (urgente/normal): ")
            sistema.agregar_paciente(nombre, edad, prioridad)
        
        elif opcion == '2':
            sistema.atender_paciente()

        elif opcion == '3':
            sistema.mostrar_lista_actual()

        elif opcion == '4':
            print("\nSaliendo del sistema... ¡Hasta luego!")
            break
        
        else:
            print("\nOpción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()