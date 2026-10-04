/*
 * BFS - BREADTH-FIRST SEARCH (Búsqueda en Anchura)
 * 
 * ¿QUÉ ES?
 * Es un algoritmo para recorrer o buscar en grafos/árboles.
 * Explora NIVEL POR NIVEL, como ondas en el agua.
 * 
 * ¿CÓMO FUNCIONA?
 * 1. Empieza en un nodo raíz
 * 2. Visita todos los vecinos directos (nivel 1)
 * 3. Luego visita los vecinos de los vecinos (nivel 2)
 * 4. Y así sucesivamente...
 * 
 * ESTRUCTURA DE DATOS CLAVE: COLA (Queue)
 * - Usa FIFO (First In, First Out)
 * - Garantiza que visitemos por niveles
 * 
 * COMPLEJIDAD:
 * - Tiempo: O(V + E) donde V = vértices, E = aristas
 * - Espacio: O(V) para la cola y el array de visitados
 */
  
#include <iostream>
#include <queue>
#include <vector>
#include <list>
using namespace std;

class Grafo {
private:
    int numVertices;                      // Número de nodos
    vector<list<int>> listaAdyacencia;   // Lista de adyacencia para representar el grafo
    
public:
    // Constructor
    Grafo(int vertices) {
        numVertices = vertices;
        listaAdyacencia.resize(vertices);
    }
    
    // Agregar arista (conexión entre dos nodos)
    void agregarArista(int origen, int destino) {
        listaAdyacencia[origen].push_back(destino);
        // Si el grafo NO es dirigido, descomenta la siguiente línea:
        // listaAdyacencia[destino].push_back(origen);
    }
    
    /*
     * BFS - ALGORITMO PRINCIPAL
     * 
     * PASO A PASO:
     * 1. Crear un array de visitados (todos false al inicio)
     * 2. Crear una cola vacía
     * 3. Marcar el nodo inicial como visitado y agregarlo a la cola
     * 4. MIENTRAS la cola no esté vacía:
     *    a) Sacar el primer elemento de la cola (actual)
     *    b) Procesar ese nodo (imprimirlo, guardarlo, etc.)
     *    c) Para cada vecino del nodo actual:
     *       - Si NO ha sido visitado:
     *         * Marcarlo como visitado
     *         * Agregarlo a la cola
     */
    void BFS(int nodoInicial) {
        // 1. Array de visitados (false = no visitado)
        vector<bool> visitado(numVertices, false);
        
        // 2. Crear la cola
        queue<int> cola;
        
        // 3. Marcar el nodo inicial como visitado y agregarlo a la cola
        visitado[nodoInicial] = true;
        cola.push(nodoInicial);
        
        cout << "\n=== RECORRIDO BFS ===" << endl;
        cout << "Inicio desde nodo: " << nodoInicial << endl;
        cout << "\nOrden de visita: ";
        
        // 4. Mientras la cola tenga elementos
        while (!cola.empty()) {
            // a) Sacar el primer elemento (FIFO)
            int nodoActual = cola.front();
            cola.pop();
            
            // b) Procesar el nodo
            cout << nodoActual << " ";
            
            // c) Explorar todos los vecinos
            for (int vecino : listaAdyacencia[nodoActual]) {
                if (!visitado[vecino]) {
                    visitado[vecino] = true;  // Marcar como visitado
                    cola.push(vecino);         // Agregar a la cola
                }
            }
        }
        cout << endl;
    }
    
    /*
     * BFS CON NIVELES
     * Muestra en qué nivel/distancia está cada nodo
     */
    void BFS_conNiveles(int nodoInicial) {
        vector<bool> visitado(numVertices, false);
        vector<int> nivel(numVertices, -1);  // -1 = no alcanzable
        queue<int> cola;
        
        visitado[nodoInicial] = true;
        nivel[nodoInicial] = 0;
        cola.push(nodoInicial);
        
        cout << "\n=== BFS CON NIVELES ===" << endl;
        
        while (!cola.empty()) {
            int nodoActual = cola.front();
            cola.pop();
            
            cout << "Nodo " << nodoActual << " (Nivel " << nivel[nodoActual] << ")" << endl;
            
            for (int vecino : listaAdyacencia[nodoActual]) {
                if (!visitado[vecino]) {
                    visitado[vecino] = true;
                    nivel[vecino] = nivel[nodoActual] + 1;
                    cola.push(vecino);
                }
            }
        }
    }
    
    /*
     * BFS PARA ENCONTRAR CAMINO MÁS CORTO
     * Encuentra el camino más corto entre dos nodos
     */
    void caminoMasCorto(int inicio, int destino) {
        if (inicio == destino) {
            cout << "\nEl inicio y destino son el mismo: " << inicio << endl;
            return;
        }
        
        vector<bool> visitado(numVertices, false);
        vector<int> padre(numVertices, -1);  // Para reconstruir el camino
        queue<int> cola;
        
        visitado[inicio] = true;
        cola.push(inicio);
        
        bool encontrado = false;
        
        while (!cola.empty() && !encontrado) {
            int actual = cola.front();
            cola.pop();
            
            for (int vecino : listaAdyacencia[actual]) {
                if (!visitado[vecino]) {
                    visitado[vecino] = true;
                    padre[vecino] = actual;
                    cola.push(vecino);
                    
                    if (vecino == destino) {
                        encontrado = true;
                        break;
                    }
                }
            }
        }
        
        if (!encontrado) {
            cout << "\nNo hay camino de " << inicio << " a " << destino << endl;
            return;
        }
        
        // Reconstruir el camino
        vector<int> camino;
        int nodo = destino;
        while (nodo != -1) {
            camino.push_back(nodo);
            nodo = padre[nodo];
        }
        
        cout << "\nCamino más corto de " << inicio << " a " << destino << ": ";
        for (int i = camino.size() - 1; i >= 0; i--) {
            cout << camino[i];
            if (i > 0) cout << " → ";
        }
        cout << "\nDistancia: " << camino.size() - 1 << " pasos" << endl;
    }
    
    // Mostrar el grafo
    void mostrarGrafo() {
        cout << "\n=== ESTRUCTURA DEL GRAFO ===" << endl;
        for (int i = 0; i < numVertices; i++) {
            cout << "Nodo " << i << " → ";
            for (int vecino : listaAdyacencia[i]) {
                cout << vecino << " ";
            }
            cout << endl;
        }
    }
};

int main() {
    /*
     * EJEMPLO: Crear un grafo
     * 
     *         0
     *        / \
     *       1   2
     *      / \   \
     *     3   4   5
     *          \ /
     *           6
     */
    
    cout << "╔════════════════════════════════════════════╗" << endl;
    cout << "║   BFS - BREADTH-FIRST SEARCH             ║" << endl;
    cout << "║   (Búsqueda en Anchura)                  ║" << endl;
    cout << "╚════════════════════════════════════════════╝" << endl;
    
    Grafo g(7);  // Grafo con 7 nodos (0 a 6)
    
    // Agregar aristas (dirigidas)
    g.agregarArista(0, 1);
    g.agregarArista(0, 2);
    g.agregarArista(1, 3);
    g.agregarArista(1, 4);
    g.agregarArista(2, 5);
    g.agregarArista(4, 6);
    g.agregarArista(5, 6);
    
    g.mostrarGrafo();
    
    // Ejecutar BFS desde el nodo 0
    g.BFS(0);
    
    // BFS con niveles
    g.BFS_conNiveles(0);
    
    // Camino más corto
    g.caminoMasCorto(0, 6);
    g.caminoMasCorto(3, 5);
    
    cout << "\n";
    
    // Ejemplo interactivo
    cout << "\n╔════════════════════════════════════════════╗" << endl;
    cout << "║   MODO INTERACTIVO                        ║" << endl;
    cout << "╚════════════════════════════════════════════╝" << endl;
    
    int n, m;
    cout << "\n¿Cuántos nodos tiene tu grafo? ";
    cin >> n;
    
    Grafo miGrafo(n);
    
    cout << "¿Cuántas aristas? ";
    cin >> m;
    
    cout << "\nIngresa las aristas (formato: origen destino):" << endl;
    for (int i = 0; i < m; i++) {
        int u, v;
        cout << "Arista " << (i + 1) << ": ";
        cin >> u >> v;
        miGrafo.agregarArista(u, v);
    }
    
    int inicio;
    cout << "\n¿Desde qué nodo iniciar el BFS? ";
    cin >> inicio;
    
    miGrafo.mostrarGrafo();
    miGrafo.BFS(inicio);
    miGrafo.BFS_conNiveles(inicio);
    
    cout << "\n¿Buscar camino más corto? (1=Si, 0=No): ";
    int opcion;
    cin >> opcion;
    
    if (opcion == 1) {
        int dest;
        cout << "¿A qué nodo quieres llegar? ";
        cin >> dest;
        miGrafo.caminoMasCorto(inicio, dest);
    }
    
    return 0;
}

/*
 * EXPLICACIÓN VISUAL DEL BFS:
 * 
 * Grafo:     0
 *           / \
 *          1   2
 *         / \   \
 *        3   4   5
 *             \ /
 *              6
 * 
 * PROCESO:
 * 
 * Cola: [0]          Visitados: {0}         Nivel 0: 0
 * Cola: [1,2]        Visitados: {0,1,2}     Nivel 1: 1, 2
 * Cola: [2,3,4]      Visitados: {0,1,2,3,4} Nivel 2: 3, 4
 * Cola: [3,4,5]      Visitados: {0,1,2,3,4,5}
 * Cola: [4,5,6]      Visitados: {0,1,2,3,4,5,6} Nivel 3: 5, 6
 * Cola: [5,6]
 * Cola: [6]
 * Cola: []           ¡Terminado!
 * 
 * Orden de visita: 0 → 1 → 2 → 3 → 4 → 5 → 6
 * 
 * USOS COMUNES DE BFS:
 * ✓ Encontrar el camino más corto (en grafos sin pesos)
 * ✓ Verificar si un grafo es conexo
 * ✓ Encontrar todos los nodos a una distancia K
 * ✓ Resolver laberintos
 * ✓ Análisis de redes sociales (amigos en común)
 * ✓ Web crawlers
 */
