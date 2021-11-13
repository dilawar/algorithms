all : run_example

setup: requirements.txt
	python3 -m pip install -r $< --user

run_example: maze.py
	python3 maze.py -s 20,20 --plot maze.png -o maze.txt
	python3 maze.py -s 20,20 --show-solution --plot maze_solution.png
