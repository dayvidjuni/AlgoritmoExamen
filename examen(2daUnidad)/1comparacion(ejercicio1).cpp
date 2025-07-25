#include <iostream>
#include <vector>
#include <list>
#include <chrono>   // Librería para medir el tiempo con alta precisión
#include <numeric>  // Para la función std::iota
#include <algorithm>// Para la función std::sort

// --- Búsqueda Lineal ---
// Revisa cada elemento uno por uno. Complejidad O(n).
int busqueda_lineal(const std::vector<int>& datos, int objetivo) {
    for (int i = 0; i < datos.size(); ++i) {
        if (datos[i] == objetivo) {
            return i; // Devuelve el índice si lo encuentra
        }
    }
    return -1; // No encontrado
}

// --- Búsqueda Binaria ---
// Divide la búsqueda a la mitad en cada paso. Complejidad O(log n).
// Requiere que el vector esté ordenado.
int busqueda_binaria(const std::vector<int>& datos_ordenados, int objetivo) {
    int izquierda = 0;
    int derecha = datos_ordenados.size() - 1;

    while (izquierda <= derecha) {
        int medio = izquierda + (derecha - izquierda) / 2;
        if (datos_ordenados[medio] == objetivo) {
            return medio; // Devuelve el índice si lo encuentra
        }
        if (datos_ordenados[medio] < objetivo) {
            izquierda = medio + 1;
        } else {
            derecha = medio - 1;
        }
    }
    return -1; // No encontrado
}

int main() {
    // ====================================================================
    // 1. ANÁLISIS DE BÚSQUEDA: Lineal vs. Binaria
    // ====================================================================
    std::cout << "--- Analisis de Busqueda ---" << std::endl;
    const int N_BUSQUEDA = 10000000; // 10 millones de elementos
    std::vector<int> datos_busqueda(N_BUSQUEDA);
    
    // Llenar el vector con números del 0 al N-1 (ya queda ordenado)
    std::iota(datos_busqueda.begin(), datos_busqueda.end(), 0);
    
    int objetivo = N_BUSQUEDA - 1; // Peor caso: buscar el último elemento

    // Medir tiempo de Búsqueda Lineal
    auto inicio_lineal = std::chrono::high_resolution_clock::now();
    int indice_lineal = busqueda_lineal(datos_busqueda, objetivo);
    auto fin_lineal = std::chrono::high_resolution_clock::now();
    auto duracion_lineal = std::chrono::duration_cast<std::chrono::microseconds>(fin_lineal - inicio_lineal);

    std::cout << "Busqueda Lineal: Elemento encontrado en el indice " << indice_lineal << std::endl;
    std::cout << "Tiempo de ejecucion: " << duracion_lineal.count() << " microsegundos." << std::endl;

    // Medir tiempo de Búsqueda Binaria
    auto inicio_binaria = std::chrono::high_resolution_clock::now();
    int indice_binaria = busqueda_binaria(datos_busqueda, objetivo);
    auto fin_binaria = std::chrono::high_resolution_clock::now();
    auto duracion_binaria = std::chrono::duration_cast<std::chrono::microseconds>(fin_binaria - inicio_binaria);
    
    std::cout << "\nBusqueda Binaria: Elemento encontrado en el indice " << indice_binaria << std::endl;
    std::cout << "Tiempo de ejecucion: " << duracion_binaria.count() << " microsegundos." << std::endl;


    // ====================================================================
    // 2. ANÁLISIS DE INSERCIÓN: Vector Dinámico vs. Lista Enlazada
    // ====================================================================
    std::cout << "\n\n--- Analisis de Insercion al Inicio ---" << std::endl;
    const int N_INSERCIONES = 50000; // Número de inserciones a realizar

    // Medir tiempo de inserción en Vector Dinámico (std::vector)
    std::vector<int> mi_vector;
    auto inicio_vector = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N_INSERCIONES; ++i) {
        // Insertar al inicio es O(n), muy costoso.
        // Requiere desplazar todos los demás elementos.
        mi_vector.insert(mi_vector.begin(), i);
    }
    auto fin_vector = std::chrono::high_resolution_clock::now();
    auto duracion_vector = std::chrono::duration_cast<std::chrono::milliseconds>(fin_vector - inicio_vector);

    std::cout << "Vector Dinamico (std::vector):" << std::endl;
    std::cout << "Tiempo para " << N_INSERCIONES << " inserciones al inicio: " << duracion_vector.count() << " milisegundos." << std::endl;

    // Medir tiempo de inserción en Lista Enlazada (std::list)
    std::list<int> mi_lista;
    auto inicio_lista = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N_INSERCIONES; ++i) {
        // Insertar al inicio es O(1), muy eficiente.
        // Solo se actualizan punteros.
        mi_lista.push_front(i);
    }
    auto fin_lista = std::chrono::high_resolution_clock::now();
    auto duracion_lista = std::chrono::duration_cast<std::chrono::milliseconds>(fin_lista - inicio_lista);

    std::cout << "\nLista Enlazada (std::list):" << std::endl;
    std::cout << "Tiempo para " << N_INSERCIONES << " inserciones al inicio: " << duracion_lista.count() << " milisegundos." << std::endl;

    system("pause");
    return 0;
}