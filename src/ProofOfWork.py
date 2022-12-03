import sys
import hashlib
import time

# Generates a target based on the POW difficulty
def TargetGen(d = 20, targetFile = "../data/target.txt"):
	difBits = '0' * int(d)			# Makes a string of 0's of d bits length
	oneBits = '1' * (256 - int(d))	# Makes a string of 1's of 256 - d length
	target = difBits + oneBits	# Makes target

	# Print and write target
	print ("Target: ", target)
	with open(targetFile, "w") as targetF:
		targetF.write(target)
		targetF.close()


# Generates a binary solution by iterating through every possibility
def SolutionGeneration(targetFile = "../data/target.txt", inputFile = "../data/input.txt", solutionFile = "../data/solution.txt", n = 0):
	# Retrieve input
	with open(inputFile, "r") as inputF:
		inputMessage = inputF.read()
		inputF.close()
	# Retrieve target
	with open(targetFile, "r") as targetF:
		targetMessage = targetF.read()
		targetF.close()

	# Iterate through all nonce possibilities until a solution is found
	foundSolution = False
	while (foundSolution == False):
		n = str(bin(n))[2:] # Convert nonce integer to binary
		# Compute hash value of concatenated string (input + solution)
		hBinaryRaw = hashlib.sha256( (inputMessage + n).encode() ).digest()

		# Convert bytes to bits
		x = bin(int.from_bytes(hBinaryRaw, byteorder=sys.byteorder))[2:]

		# If Hash <= target then it is a solution, otherwise continue and generate new hash with next nonce value
		foundSolution = int(x, 2) <= int(targetMessage.encode(), 2)
		if (foundSolution == False):
			n = int(n, 2) + 1

	print ("Solution: ", str(int(n, 2)))

	# Write solution to output file
	with open(solutionFile, "w") as solutionF:
		solutionF.write(str(int(n, 2)))
		solutionF.close()

	return int(n, 2)


# Verifies if a solution is valid
def Verify(targetFile = "../data/target.txt", inputFile = "../data/input.txt", solutionFile = "../data/solution.txt"):
	# Retrieve input
	with open(inputFile, "r") as inputF:
		inputMessage = inputF.read()
		inputF.close()
	# Retrieve target
	with open(targetFile, "r") as targetF:
		targetMessage = targetF.read()
		targetF.close()
	# Retrieve solution
	with open(solutionFile, "r") as solutionF:
		solutionMessage = solutionF.read()
		solutionF.close()

	n = str(bin(int(solutionMessage)))[2:] # Convert solution integer to binary
	hBinaryRaw = hashlib.sha256( (inputMessage + n).encode() ).digest()

	# Convert bytes to bits
	x = bin(int.from_bytes(hBinaryRaw, byteorder=sys.byteorder))[2:]

	# If Hash <= target then it is a solution and print 1, otherwise print 0
	if (int(x, 2) <= int(targetMessage.encode(), 2)):
		print (1)
	else:
		print (0)


# Checks performance of program by incrementally going through a set of 9 difficulty levels to produce a different solution for each
def PerformanceCheck(inpFile = "../data/input.txt"):
	# Iterate through difficulty levels 16 through 24
	solution = 0
	totalTime = 0
	for d in range(16, 25):
		TargetGen(d)

		startTime = time.time()
		# Generate a solution that is different than the others (i.e. starting the nonce value one increment after the previous solution will avoid similar solutions)
		solution = SolutionGeneration(inputFile = inpFile, n = solution) + 1
		# Calculate time values for each difficulty and all the difficulties
		endTime = time.time()
		elapsedTime = endTime - startTime
		totalTime = totalTime + elapsedTime
		print ("Elapsed Time: {:.4f} seconds".format(elapsedTime))
		print ("Total Time:   {:.4f} seconds".format(totalTime))
		print ("Difficulty: {}\n".format(d))


# Input checks
if len(sys.argv) > 1:
	if sys.argv[1] == "TargetGen":
		if len(sys.argv) > 3:
			TargetGen(sys.argv[2], sys.argv[3])
		else:
			print("Not enough arguments (key length, skprf file, skaes file), using default values")
			TargetGen()
	elif sys.argv[1] == "SolutionGeneration":
		if len(sys.argv) > 4:
			SolutionGeneration(sys.argv[2], sys.argv[3], sys.argv[4])
		else:
			print("Not enough arguments (skprf file, skaes file, index file, files dir, ciphertextfiles dir), using default values")
			SolutionGeneration()
	elif sys.argv[1] == "Verify":
		if len(sys.argv) > 4:
			Verify(sys.argv[2], sys.argv[3], sys.argv[4])
		else:
			print("Not enough arguments (keyword, skprf file, token file), using default values")
			Verify()
	elif sys.argv[1] == "PerformanceCheck":
		if len(sys.argv) > 2:
			PerformanceCheck(sys.argv[2])
		else:
			print("Not enough arguments (index file, token file, ciphertextfiles dir, skaes file, results file), using default values")
			PerformanceCheck()
else:
    # Calls default functions
	TargetGen()
	SolutionGeneration()
	Verify()
	PerformanceCheck()