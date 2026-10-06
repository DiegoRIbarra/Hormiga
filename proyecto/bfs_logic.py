from collections import deque

def bfs_shortest_path(grid, start, end):
    """
    Algoritmo BFS para encontrar el camino más corto en un grid.
    grid: Lista de listas (0 = camino, 1 = obstáculo)
    start: Tupla (fila, col)
    end: Tupla (fila, col)
    """
    # Direcciones: Arriba, Abajo, Izquierda, Derecha
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Cola para BFS: almacena (posición_actual, camino_recorrido)
    queue = deque([(start, [start])])
    
    # Conjunto de posiciones visitadas para evitar bucles
    visited = set()
    visited.add(start)
    
    while queue:
        (current_x, current_y), path = queue.popleft()
        
        # Si llegamos al destino, devolvemos el camino
        if (current_x, current_y) == end:
            return path
        
        # Explorar vecinos
        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy
            
            # Verificar límites, que no sea obstáculo y que no haya sido visitado
            if (0 <= new_x < len(grid) and 
                0 <= new_y < len(grid[0]) and 
                grid[new_x][new_y] != 1 and 
                (new_x, new_y) not in visited):
                
                visited.add((new_x, new_y))
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))
                
    return [] # Retorna lista vacía si no hay camino
