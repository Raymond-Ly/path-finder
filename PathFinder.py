import sys, os, re
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def errorexit(message):
	outputFile.write("error")
	outputFile.close()
	sys.exit(message)
	
if __name__ == "__main__":
	# Read input file from first argument
	if len(sys.argv) < 2:
		sys.exit("First argument must be a path to a file")
		
	if not os.path.isfile(sys.argv[1]):
		sys.exit("Input file specified does not exist")

	try:
		inputFile = open(sys.argv[1], "r")
		outputFile = open(sys.argv[1]+".answer", "w+")
		match = re.findall("x([0-9]+)y([0-9]*)", inputFile.read()) # This regex matches any number of instances in the format x[number]y[number] and captures the numbers
		inputFile.close()
	except IOError as err:
		sys.exit(err)
		
	if len(match) < 2:
		outputFile.write("error")
		outputFile.close()
		sys.exit("Input file must have at least two pairs of coordinates")
			
	# Now find the largest coordinates to allocate our map
	largestX = 0
	largestY = 0
	for i in range(1, len(match)-1): # Skip the source and goal
		if match[i][0] > largestX:
			largestX = match[i][0]
		if match[i][1] > largestY:
			largestY = match[i][1] 		
	
	largestX = int(largestX) + 1
	largestY = int(largestY) + 1
	
	startX = int(match[0][0])
	startY = int(match[0][1])
	endX = int(match[len(match)-1][0])
	endY = int(match[len(match)-1][1])
	
	print("Creating map of size " + str(largestX) + "x" + str(largestY))
	
	if startX >= largestX:
		errorexit("Start X coordinate exceeds map boundaries")
	if startY >= largestY:
		errorexit("Start Y coordinate exceeds map boundaries")
	if endX >= largestX:
		errorexit("End X coordinate exceeds map boundaries")
	if endY >= largestY:
		errorexit("End Y coordinate exceeds map boundaries")
	
	map = [[1 for i in range(largestX)] for j in range(largestY)]
	
	# Populate the map
	map[0][0] = 2
	for i in range(1, len(match)-1): # Skip the source and goal
		map[int(match[i][1])][int(match[i][0])] = 0 # Set reef
		
	grid = Grid(matrix=map)

	# Set our start and end
	start = grid.node(startX, startY)
	end = grid.node(endX, endY)

	finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
	path, runs = finder.find_path(start, end, grid)
	
	if len(path) == 0:
		errorexit("No path found")
		
	print("Found path of length " + str(len(path)) + " in " + str(runs) + " operations")
	
	output = grid.grid_str(path=path, start=start, end=end, border=False, start_chr='S', end_chr='E', block_chr='x', path_chr='O', empty_chr='.')
	outputFile.write(output)
	sys.exit(output)
