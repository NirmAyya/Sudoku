import networkx as nx

# The unsolved input will be given as a 9x9 2D array.
# Blank spaces will be denoted by 0
# Example grid will look like this:
'''
example_sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]'''
sudoku =[
    [4, 0, 0, 5, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 4, 3, 0, 1, 8],
    [3, 1, 0, 0, 0, 0, 0, 5, 6],
    [0, 3, 6, 9, 7, 0, 1, 0, 0],
    [0, 4, 0, 0, 2, 0, 0, 8, 0],
    [0, 0, 9, 0, 5, 4, 2, 6, 0],
    [6, 8, 0, 0, 0, 0, 0, 2, 1],
    [1, 5, 0, 4, 6, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 5, 0, 0, 4]
]

# Convert this array into a graph
G = nx.Graph()

# Populate the graph
for i in range(9):
    for j in range(9):
        G.add_node((i, j))

# Connect the graph

# Same row connection
for i in range(9):
    for j in range(9):
        for k in range(j + 1, 9):
            G.add_edge((i, j), (i, k))

# Same column connection
for i in range(9):
    for j in range(9):
        for k in range(i + 1, 9):
            G.add_edge((i, j), (k, j))

# Connecting mini 3x3 grids
for subgrid_x in range(0, 9, 3):
    for subgrid_y in range(0, 9, 3):
        cells = []
        for i in range(3):
            for j in range(3):
                cells.append((subgrid_x + i, subgrid_y + j))
        
        # Connect every cell in the subgrid with every other cell in the same subgrid
        for m in range(9):
            for n in range(m + 1, 9):
                G.add_edge(cells[m], cells[n])

# Manually start a coloring
for i in range(9):
    for j in range(9):
        if sudoku[i][j] != 0:
            G.nodes[(i, j)]['color'] = sudoku[i][j]

def is_safe(G, node, color):
    for neighbor in G.neighbors(node):
        if 'color' in G.nodes[neighbor] and G.nodes[neighbor]['color'] == color:
            return False
    return True

def solve_sudoku(G, nodes):
    if not nodes:
        return True  # If all nodes are processed

    node = nodes.pop(0)
    if 'color' in G.nodes[node]:
        if solve_sudoku(G, nodes):
            return True
        nodes.insert(0, node)
        return False

    for color in range(1, 10):  # Sudoku numbers 1 to 9
        if is_safe(G, node, color):
            G.nodes[node]['color'] = color
            if solve_sudoku(G, nodes):
                return True
            G.nodes[node].pop('color')

    nodes.insert(0, node)
    return False

def print_sudoku(G):
    result = ""
    for i in range(9):
        row = [str(G.nodes[(i, j)].get('color', 0)) for j in range(9)]
        result += " ".join(row) + "\n"
    return result

# Solve the Sudoku
nodes = list(G.nodes)
if solve_sudoku(G, nodes):
    print("Sudoku solved successfully!")
    print(print_sudoku(G))
else:
    print("Failed to solve Sudoku.")

# Validate the solution
