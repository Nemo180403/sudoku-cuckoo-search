{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "1761f29b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: numpy in c:\\programdata\\anaconda3\\lib\\site-packages (1.23.5)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install numpy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "11561870",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Solved Sudoku:\n",
      "[[5 3 4 2 7 6 9 1 8]\n",
      " [6 7 2 1 9 5 4 3 0]\n",
      " [1 9 8 3 4 0 7 6 2]\n",
      " [8 1 9 7 6 4 5 2 3]\n",
      " [4 2 6 8 5 3 0 9 1]\n",
      " [7 5 3 9 2 1 8 4 6]\n",
      " [9 6 1 5 3 7 2 8 4]\n",
      " [2 8 7 4 1 9 6 0 5]\n",
      " [3 4 5 6 8 2 1 7 9]]\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import random\n",
    "\n",
    "# Firstly we initialize Sudoku puzzle (0 represents empty cells)\n",
    "sudoku_puzzle = [\n",
    "    [5, 3, 0, 0, 7, 0, 0, 0, 0],\n",
    "    [6, 0, 0, 1, 9, 5, 0, 0, 0],\n",
    "    [0, 9, 8, 0, 0, 0, 0, 6, 0],\n",
    "    [8, 0, 0, 0, 6, 0, 0, 0, 3],\n",
    "    [4, 0, 0, 8, 0, 3, 0, 0, 1],\n",
    "    [7, 0, 0, 0, 2, 0, 0, 0, 6],\n",
    "    [0, 6, 0, 0, 0, 0, 2, 8, 0],\n",
    "    [0, 0, 0, 4, 1, 9, 0, 0, 5],\n",
    "    [0, 0, 0, 0, 8, 0, 0, 7, 9]\n",
    "]\n",
    "\n",
    "# then we define some utility functions to check the validity of a move\n",
    "def is_valid_move(puzzle, r, c, num):\n",
    "    for x in range(9):\n",
    "        if puzzle[r][x] == num or puzzle[x][c] == num:\n",
    "            return False\n",
    "\n",
    "    box_start_row, box_start_col = 3 * (r // 3), 3 * (c // 3)\n",
    "    for x in range(3):\n",
    "        for y in range(3):\n",
    "            if puzzle[box_start_row + x][box_start_col + y] == num:\n",
    "                return False\n",
    "    return True\n",
    "\n",
    "# Fitness function to evaluate Sudoku solution\n",
    "def fitness(sudoku):\n",
    "    fitness_score = 0\n",
    "    for r in range(9):\n",
    "        fitness_score += len(set(sudoku[r]))  # They are unique numbers in rows\n",
    "\n",
    "    for c in range(9):\n",
    "        col_vals = [sudoku[r][c] for r in range(9)]\n",
    "        fitness_score += len(set(col_vals))  # They are unique numbers in columns\n",
    "\n",
    "    return fitness_score\n",
    "\n",
    "# Cuckoo Search core function\n",
    "def cuckoo_search(sudoku, max_generations=100, nest_size=25, pa=0.25):\n",
    "    nests = [generate_initial_solution(sudoku) for _ in range(nest_size)]\n",
    "    best_solution = nests[0]\n",
    "    \n",
    "    for generation in range(max_generations):\n",
    "        new_nests = []\n",
    "        for nest in nests:\n",
    "            new_solution = get_new_solution(nest)\n",
    "            if fitness(new_solution) > fitness(nest):\n",
    "                nest = new_solution\n",
    "            new_nests.append(nest)\n",
    "        \n",
    "        # Sorting and selecting the best nest\n",
    "        new_nests = sorted(new_nests, key=fitness, reverse=True)\n",
    "        best_solution = new_nests[0] if fitness(new_nests[0]) > fitness(best_solution) else best_solution\n",
    "\n",
    "        # Apply probability (pa) to some nests for randomization\n",
    "        for x in range(int(pa * nest_size), nest_size):\n",
    "            new_nests[x] = generate_initial_solution(sudoku)\n",
    "\n",
    "        nests = new_nests\n",
    "\n",
    "        # Early stopping if puzzle is solved\n",
    "        if fitness(best_solution) == 162:  # It is perfect fitness score for a valid Sudoku\n",
    "            break\n",
    "\n",
    "    return best_solution\n",
    "\n",
    "# It is helper function to generate an initial solution\n",
    "def generate_initial_solution(sudoku):\n",
    "    solution = np.copy(sudoku)\n",
    "    for r in range(9):\n",
    "        for c in range(9):\n",
    "            if solution[r][c] == 0:\n",
    "                valid_numbers = [n for n in range(1, 10) if is_valid_move(solution, r, c, n)]\n",
    "                if valid_numbers:\n",
    "                    solution[r][c] = random.choice(valid_numbers)\n",
    "    return solution\n",
    "\n",
    "# Helper function to get a new solution based on Cuckoo Search rules\n",
    "def get_new_solution(sudoku):\n",
    "    new_sudoku = np.copy(sudoku)\n",
    "    r, c = random.randint(0, 8), random.randint(0, 8)\n",
    "    if new_sudoku[r][c] == 0:  # Mutate only empty cells\n",
    "        valid_numbers = [n for n in range(1, 10) if is_valid_move(new_sudoku, r, c, n)]\n",
    "        if valid_numbers:\n",
    "            new_sudoku[r][c] = random.choice(valid_numbers)\n",
    "    return new_sudoku\n",
    "\n",
    "# In last we solve the Sudoku puzzle using Cuckoo Search\n",
    "solved_sudoku = cuckoo_search(sudoku_puzzle)\n",
    "\n",
    "# Display the solved Sudoku puzzle\n",
    "print(\"Solved Sudoku:\")\n",
    "print(np.array(solved_sudoku))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a4b8d539",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
