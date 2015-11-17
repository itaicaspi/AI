#Homework 1 - Heuristic Search

The PDF for the assignment can found in docs/AI_HW1.pdf

Library documentation can be found in ways/README.md

##Directory Structure

Add your source files here, and insert calls for the functions in them inside main.py.

You can add directories for 3rd party libraries. Remember to declare `dir your_directory` in docs/dependencies.txt.


__init__.py: A hint for the interpreter - ignore this file

main.py: Minimal interface to the command line: `$ python main.py [args]`

stats.py: Gather and print statistics: `$ python stats.py`

___
ways/
Primary library. Basic usage: 
```python
from ways import load_map_from_csv
roads = load_map_from_csv()
````
ways/README.md: Library documentation

ways/__init__.py: Defines the functions accessible using `import ways`

ways/graph.py: Code to load the map from the database

ways/info.py: Constants

ways/tools.py: Arbitrary, possibly useful tools

ways/draw.py: Helper file for drawing paths using matplotlib

___

docs/
Documentation

[`docs/AI_HW1.pdf`](docs/AI_HW1.pdf) Assignment file

[`docs/dependencies.txt`](docs/dependencies.txt) Declarations of dependencies in 3rd party libraries. For example:

> pip numpy
>

___
db/
Database. Do not change.

db/israel.csv Roads description. primary database file
___		
results/
Put your experiment results (text and images) here
