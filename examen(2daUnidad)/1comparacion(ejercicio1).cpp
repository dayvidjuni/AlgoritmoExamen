#include <iostream>
#include <vector>
#include <list>
#include <chrono>   
#include <numeric> 
#include <algorithm>

using namespace std;

// --- Búsqueda Lineal ---
// Revisa cada elemento uno por uno. Complejidad O(n).
int busqueda_lineal(const vector<int>& datos, int objetivo) {
    for (int i = 0; i < datos.size(); ++i) {
        if (datos[i] == objetivo) {
            return i; // Devuelve el índice si lo encuentra
        }
    }
    return -1; 
}

// --- Búsqueda Binaria ---
// Requiere que los datos estén ordenados. Complejidad O(log n).
int busqueda_binaria(const vector<int>& datos_ordenados, int objetivo) {
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
    cout << "--- Analisis de Busqueda ---" << endl;
    const int N_BUSQUEDA = 10000000; // 10 millones de elementos
    vector<int> datos_busqueda(N_BUSQUEDA);
    
    // Llenar el vector con números del 0 al N-1 (ya queda ordenado)
    iota(datos_busqueda.begin(), datos_busqueda.end(), 0);
    
    int objetivo = N_BUSQUEDA - 1; // Peor caso: buscar el último elemento

    // Medir tiempo de Búsqueda Lineal
    auto inicio_lineal = chrono::high_resolution_clock::now();
    int indice_lineal = busqueda_lineal(datos_busqueda, objetivo);
    auto fin_lineal = chrono::high_resolution_clock::now();
    auto duracion_lineal = chrono::duration_cast<chrono::microseconds>(fin_lineal - inicio_lineal);

    cout << "Busqueda Lineal: Elemento encontrado en el indice " << indice_lineal << endl;
    cout << "Tiempo de ejecucion: " << duracion_lineal.count() << " microsegundos." << endl;

    // Medir tiempo de Búsqueda Binaria
    auto inicio_binaria = chrono::high_resolution_clock::now();
    int indice_binaria = busqueda_binaria(datos_busqueda, objetivo);
    auto fin_binaria = chrono::high_resolution_clock::now();
    auto duracion_binaria = chrono::duration_cast<chrono::microseconds>(fin_binaria - inicio_binaria);
    
    cout << "\nBusqueda Binaria: Elemento encontrado en el indice " << indice_binaria << endl;
    cout << "Tiempo de ejecucion: " << duracion_binaria.count() << " microsegundos." << endl;

    // ====================================================================
    // 2. ANÁLISIS DE INSERCIÓN: Vector Dinámico vs. Lista Enlazada
    // ====================================================================
    cout << "\n\n--- Analisis de Insercion al Inicio ---" << endl;
    const int N_INSERCIONES = 50000; // Número de inserciones a realizar

    // Medir tiempo de inserción 
    vector<int> mi_vector;
    auto inicio_vector = chrono::high_resolution_clock::now();
    for (int i = 0; i < N_INSERCIONES; ++i) {
        mi_vector.insert(mi_vector.begin(), i);
    }
    auto fin_vector = chrono::high_resolution_clock::now();
    auto duracion_vector = chrono::duration_cast<chrono::milliseconds>(fin_vector - inicio_vector);

    cout << "Vector Dinamico (vector):" << endl;
    cout << "Tiempo para " << N_INSERCIONES << " inserciones al inicio: " << duracion_vector.count() << " milisegundos." << endl;

    // Medir tiempo de inserción en una Lista Enlazada 
    list<int> mi_lista;
    auto inicio_lista = chrono::high_resolution_clock::now();
    for (int i = 0; i < N_INSERCIONES; ++i) {
        mi_lista.push_front(i);
    }
    auto fin_lista = chrono::high_resolution_clock::now();
    auto duracion_lista = chrono::duration_cast<chrono::milliseconds>(fin_lista - inicio_lista);

    cout << "\nLista Enlazada (list):" << endl;
    cout << "Tiempo para " << N_INSERCIONES << " inserciones al inicio: " << duracion_lista.count() << " milisegundos." << endl;

    return 0;
}
