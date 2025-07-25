#include <iostream>
#include <algorithm> 

using namespace std;

// Estructura del nodo del árbol
struct Nodo {
    int key;
    Nodo *izquierda;
    Nodo *derecha;
    int altura;
};

// Clase para encapsular la lógica del Árbol AVL
class ArbolAVL {
public:
    ArbolAVL() : raiz(nullptr) {}

    // Función para insertar una clave
    void insertar(int key) {
        raiz = insertar_recursivo(raiz, key);
    }

    // Función para mostrar el árbol en pre-orden
    void mostrarPreOrden() {
        preOrden(raiz);
        cout << endl;
    }

private:
    Nodo* raiz;

    // Función para obtener la altura de un nodo
    int obtenerAltura(Nodo* n) {
        return (n == nullptr) ? 0 : n->altura;
    }

    // Obtener el factor de balance de un nodo
    int obtenerBalance(Nodo* n) {
        if (n == nullptr) return 0;
        return obtenerAltura(n->izquierda) - obtenerAltura(n->derecha);
    }

    // Crear un nuevo nodo
    Nodo* nuevoNodo(int key) {
        Nodo* nodo = new Nodo();
        nodo->key = key;
        nodo->izquierda = nullptr;
        nodo->derecha = nullptr;
        nodo->altura = 1; // Un nuevo nodo siempre tiene altura 1
        return nodo;
    }

    // Rotación simple a la derecha (Caso Izquierda-Izquierda)
    Nodo* rotacionDerecha(Nodo* y) {
        cout << "--> Realizando Rotacion Simple a la Derecha sobre el nodo " << y->key << endl;
        Nodo* x = y->izquierda;
        Nodo* T2 = x->derecha;

        // aqui se realiza la rotacion
        x->derecha = y;
        y->izquierda = T2;

        // Actualizar alturas
        y->altura = max(obtenerAltura(y->izquierda), obtenerAltura(y->derecha)) + 1;
        x->altura = max(obtenerAltura(x->izquierda), obtenerAltura(x->derecha)) + 1;

        return x; 
    }

    // Rotación simple a la izquierda 
    Nodo* rotacionIzquierda(Nodo* x) {
        cout << "--> Realizando Rotacion Simple a la Izquierda sobre el nodo " << x->key << endl;
        Nodo* y = x->derecha;
        Nodo* T2 = y->izquierda;

        // Realizar la rotación
        y->izquierda = x;
        x->derecha = T2;

        // Actualizar alturas
        x->altura = max(obtenerAltura(x->izquierda), obtenerAltura(x->derecha)) + 1;
        y->altura = max(obtenerAltura(y->izquierda), obtenerAltura(y->derecha)) + 1;

        return y; 
    }

    // Función recursiva para insertar un nodo y balancear el árbol
    Nodo* insertar_recursivo(Nodo* nodo, int key) {
        // 1. Inserción normal de un BST
        if (nodo == nullptr) return nuevoNodo(key);
        if (key < nodo->key) {
            nodo->izquierda = insertar_recursivo(nodo->izquierda, key);
        } else if (key > nodo->key) {
            nodo->derecha = insertar_recursivo(nodo->derecha, key);
        } else {
            return nodo; 
        }

        // 2. Actualizar la altura del nodo actual
        nodo->altura = 1 + max(obtenerAltura(nodo->izquierda), obtenerAltura(nodo->derecha));

        // 3. Obtener el factor de balance para ver si el nodo se ha desbalanceado
        int balance = obtenerBalance(nodo);

        // 4. Si está desbalanceado, hay 4 casos posibles:

        // Caso Izquierda-Izquierda (Se necesita una rotación simple a la derecha)
        if (balance > 1 && key < nodo->izquierda->key) {
            return rotacionDerecha(nodo);
        }

        // Caso Derecha-Derecha (Se necesita una rotación simple a la izquierda)
        if (balance < -1 && key > nodo->derecha->key) {
            return rotacionIzquierda(nodo);
        }

        // Caso Izquierda-Derecha (Rotación doble)
        if (balance > 1 && key > nodo->izquierda->key) {
            cout << "--> Desbalance Izquierda-Derecha detectado en el nodo " << nodo->key << endl;
            nodo->izquierda = rotacionIzquierda(nodo->izquierda);
            return rotacionDerecha(nodo);
        }

        // Caso Derecha-Izquierda (Rotación doble)
        if (balance < -1 && key < nodo->derecha->key) {
            cout << "--> Desbalance Derecha-Izquierda detectado en el nodo " << nodo->key << endl;
            nodo->derecha = rotacionDerecha(nodo->derecha);
            return rotacionIzquierda(nodo);
        }

        // Si no hubo desbalance, devolver el nodo sin cambios
        return nodo;
    }

    // Función recursiva para mostrar en pre-orden
    void preOrden(Nodo* nodo) {
        if (nodo != nullptr) {
            cout << nodo->key << " ";
            preOrden(nodo->izquierda);
            preOrden(nodo->derecha);
        }
    }
};


int main() {
    ArbolAVL arbol;

    // Insertaremos una secuencia de números diseñada para provocar rotaciones
    cout << "Insertando 10, 20, 30 (provocara una rotacion Izquierda)\n";
    arbol.insertar(10);
    arbol.insertar(20);
    cout << "Insertando 30...\n";
    arbol.insertar(30); // causa un desbalance Derecha-Derecha
    cout << "Arbol actual (PreOrden): ";
    arbol.mostrarPreOrden();
    cout << "-------------------------------------------\n";

    cout << "\nInsertando 40, 50 (provocara otra rotacion Izquierda)\n";
    arbol.insertar(40);
    cout << "Insertando 50...\n";
    arbol.insertar(50); // Desbalance Derecha-Derecha
    cout << "Arbol actual (PreOrden): ";
    arbol.mostrarPreOrden();
    cout << "-------------------------------------------\n";

    cout << "\nInsertando 35 (provocara una rotacion doble Derecha-Izquierda)\n";
    arbol.insertar(35);
    cout << "Arbol actual (PreOrden): ";
    arbol.mostrarPreOrden();
    cout << "-------------------------------------------\n";

    system("pause");
    return 0;
}