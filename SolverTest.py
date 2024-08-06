import networkx as nx
import csv

def string_to_sudoku_array(digits):
    if len(digits) != 81:
        raise ValueError("Input string must be exactly 81 characters long.")
    
    # Convert the string to a list of integers
    digits = [int(digit) for digit in digits]
    
    # Create the 9x9 2D array
    sudoku_array = []
    for i in range(9):
        row = digits[i * 9:(i + 1) * 9]
        sudoku_array.append(row)
    
    return sudoku_array

def is_safe(G, node, color):
    for neighbor in G.neighbors(node):
        if 'color' in G.nodes[neighbor] and G.nodes[neighbor]['color'] == color:
            return False
    return True

def solve_sudoku(sudoku):
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

    def solve_sudoku_recursive(G, nodes):
        if not nodes:
            return True  # If all nodes are processed

        node = nodes.pop(0)
        if 'color' in G.nodes[node]:
            if solve_sudoku_recursive(G, nodes):
                return True
            nodes.insert(0, node)
            return False

        for color in range(1, 10):  # Sudoku numbers 1 to 9
            if is_safe(G, node, color):
                G.nodes[node]['color'] = color
                if solve_sudoku_recursive(G, nodes):
                    return True
                G.nodes[node].pop('color')

        nodes.insert(0, node)
        return False

    nodes = list(G.nodes)
    if solve_sudoku_recursive(G, nodes):
        solved_sudoku = [[G.nodes[(i, j)].get('color', 0) for j in range(9)] for i in range(9)]
        return solved_sudoku
    else:
        return None

def compare_sudoku(solved, solution):
    for i in range(9):
        for j in range(9):
            if solved[i][j] != solution[i][j]:
                return False
    return True

# MAIN DRIVER CODE 

# Read puzzles from the csv file and check accuracy
def main(num_cases=None):
    with open('SudokuSolver/sudoku.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        total_puzzles = 0
        correct_solutions = 0

        for row in reader:
            if num_cases is not None and total_puzzles >= num_cases:
                break

            puzzle_string = row['puzzle']
            solution_string = row['solution']

            sudoku_array = string_to_sudoku_array(puzzle_string)
            solution_array = string_to_sudoku_array(solution_string)

            solved_sudoku = solve_sudoku(sudoku_array)
            print(solved_sudoku)

            if solved_sudoku and compare_sudoku(solved_sudoku, solution_array):
                correct_solutions += 1
            total_puzzles += 1

        accuracy = (correct_solutions / total_puzzles) * 100 if total_puzzles else 0
        print(f"Accuracy: {accuracy:.2f}% ({correct_solutions}/{total_puzzles})")

# Set the number of cases to check (None to check all cases)
main(num_cases=10)