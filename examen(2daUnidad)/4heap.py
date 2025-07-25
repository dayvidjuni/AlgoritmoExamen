import heapq
import os
import time

# --- Clase para el Gestor de Tareas (usando un Heap) ---
class GestorDeTareas:
    """
    Gestiona una cola de prioridad de tareas usando un montículo (heap).
    Las tareas con mayor prioridad numérica (10) son atendidas primero.
    """
    def __init__(self):
        # El heap se implementa como una lista simple en Python.
        # Guardaremos tuplas: (-prioridad, id_tarea, descripcion)
        self.tareas_heap = []
        self.contador_id = 0 # Para que cada tarea sea única

    def agregar_tarea(self, descripcion, prioridad):
        """
        Agrega una nueva tarea al montículo (heap).
        La operación heappush tiene una complejidad de O(log n).
        """
        if not 1 <= prioridad <= 10:
            print("\n❌ ERROR: La prioridad debe estar entre 1 y 10.")
            return

        # Truco para simular un Max-Heap: usar prioridad negativa.
        # El contador_id ayuda a desempatar si dos tareas tienen la misma prioridad.
        prioridad_negativa = -prioridad
        self.contador_id += 1
        tarea = (prioridad_negativa, self.contador_id, descripcion)
        
        heapq.heappush(self.tareas_heap, tarea)
        print(f"\n✅ Tarea '{descripcion}' con prioridad {prioridad} ha sido añadida.")

    def atender_siguiente_tarea(self):
        """
        Extrae y procesa la tarea con la más alta prioridad.
        La operación heappop tiene una complejidad de O(log n).
        """
        if not self.tareas_heap:
            print("\n👍 ¡Felicidades! No hay tareas pendientes.")
            return None

        # heappop siempre extrae el elemento más pequeño (en nuestro caso, la prioridad más negativa)
        prioridad_neg, _, descripcion = heapq.heappop(self.tareas_heap)
        
        prioridad_real = -prioridad_neg # Convertir de nuevo a positivo
        
        print("\n" + "*"*45)
        print("  ⚙️  ATENDIENDO LA TAREA MÁS URGENTE...")
        print("*"*45)
        print(f"   Descripción: {descripcion}")
        print(f"   Prioridad:   {prioridad_real}")
        print("*"*45)
        return descripcion

    def ver_siguiente_tarea(self):
        """
        Muestra la tarea de mayor prioridad sin eliminarla (peek).
        Esta es una operación O(1), ya que solo mira el primer elemento.
        """
        if not self.tareas_heap:
            print("\n👍 No hay tareas pendientes para mostrar.")
            return

        # El elemento con mayor prioridad siempre está en el índice 0
        prioridad_neg, _, descripcion = self.tareas_heap[0]
        prioridad_real = -prioridad_neg

        print("\n" + "-"*45)
        print("  👀 PRÓXIMA TAREA EN LA COLA")
        print(f"   Descripción: {descripcion}")
        print(f"   Prioridad:   {prioridad_real}")
        print("-"*45)

    def mostrar_todas_las_tareas(self):
        """
        Muestra todas las tareas ordenadas por prioridad.
        Esta es una operación O(n log n) porque ordena una copia de la lista.
        """
        if not self.tareas_heap:
            print("\n👍 No hay tareas pendientes.")
            return

        print("\n" + "="*50)
        print("        LISTA COMPLETA DE TAREAS PENDIENTES")
        print("="*50)
        print(f"{'Prioridad':<12}{'Descripción'}")
        print("-"*50)
        
        # Mostramos las tareas ordenadas sin destruir el heap original
        # sorted() es eficiente para esto.
        for prioridad_neg, _, descripcion in sorted(self.tareas_heap):
            prioridad_real = -prioridad_neg
            print(f"{prioridad_real:<12}{descripcion}")
        print("="*50)
        print(f"Total de tareas pendientes: {len(self.tareas_heap)}")

# --- Interfaz de Consola ---
def main():
    sistema = GestorDeTareas()
    
    print("Cargando sistema con tareas de ejemplo...")
    sistema.agregar_tarea("Revisar servidor de base de datos", 9)
    sistema.agregar_tarea("Enviar reporte semanal", 5)
    sistema.agregar_tarea("Arreglar bug crítico en producción", 10)
    sistema.agregar_tarea("Planificar reunión de equipo", 3)
    time.sleep(1)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n⚙️ === Sistema de Prioridades con Heap ===")
        print("1. Agregar nueva tarea")
        print("2. Atender la tarea más urgente")
        print("3. Ver cuál es la próxima tarea")
        print("4. Mostrar todas las tareas pendientes")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            desc = input("Descripción de la tarea: ")
            try:
                prio = int(input("Prioridad de la tarea (1-10): "))
                sistema.agregar_tarea(desc, prio)
            except ValueError:
                print("\n❌ ERROR: La prioridad debe ser un número.")
        
        elif opcion == '2':
            sistema.atender_siguiente_tarea()

        elif opcion == '3':
            sistema.ver_siguiente_tarea()
            
        elif opcion == '4':
            sistema.mostrar_todas_las_tareas()

        elif opcion == '5':
            print("\nSaliendo del sistema...")
            break
        
        else:
            print("\nOpción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()