# !/usr/bin/env python3
"""
=============================================================================
Date : 11/29/2023
Version : 1.0
Notes : -i,-o,-s should all be strings. -i and -o are file paths, -s is a scoring seed string. -p is an int
Python Version: 3.11.3
=============================================================================
"""





import argparse
from decryptLetter import decryptLetter
from multiprocessing import Pool

def decryptLetter(letter, rotationValue):
  rotationString  = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ "
  currentPosition = rotationString.find(letter)

  return rotationString[(currentPosition + rotationValue) % 95]


"""
    Main function call to create and return a list, which will be the list that is created from doing the seed calculations on a row by comparing adjacent neighbors
    Instead of having multiple comparisons while iterating through each i,j variable and checking if a neighbor is existing or not
    I check for: If it's the first or last row, or if its a "middle" row (i == number), and then manually computate the first entry of the row
    and the last entry of the row. The "middle" entries can be done in a while/for loop 

"""
def rowCalc(matrixData):
    #Matrix data is passed as a tuple of [ [A list of lists], [integer (row number)]   ]
    matrix = matrixData[0]
    i = matrixData[1]
    del(matrixData)
    rowLen = len(matrix[0])-1
    sum = 0
    colCount = 1
    newRow = []
    if(i == 0):
        sum = letterCheck(matrix[0][1]) + letterCheck(matrix[1][0]) + letterCheck(matrix[1][1])
        newRow.append(checkSum(sum, matrix[0][0]))
        while colCount < (rowLen):
            sum = 0
            sum = letterCheck(matrix[0][colCount -1]) + letterCheck(matrix[0][colCount + 1]) + letterCheck(matrix[1][colCount]) + letterCheck(matrix[1][colCount -1]) + letterCheck(matrix[1][colCount + 1])
            newRow.append(checkSum(sum, matrix[0][colCount]))
            colCount+=1
        sum = 0
        sum = letterCheck(matrix[0][rowLen-1]) + letterCheck(matrix[1][rowLen]) + letterCheck(matrix[1][rowLen -1])
        newRow.append(checkSum(sum, matrix[0][rowLen]))
        return newRow
    

    elif(i == rowLen):
        sum = letterCheck(matrix[1][1]) + letterCheck(matrix[0][0]) + letterCheck(matrix[0][1])
        newRow.append(checkSum(sum, matrix[1][0]))
        while colCount < (rowLen):
            sum = 0
            sum = letterCheck(matrix[1][colCount -1]) + letterCheck(matrix[1][colCount + 1]) + letterCheck(matrix[0][colCount]) + letterCheck(matrix[0][colCount -1]) + letterCheck(matrix[0][colCount + 1])
            newRow.append(checkSum(sum, matrix[1][colCount]))
            colCount+=1
        sum = 0
        sum = letterCheck(matrix[1][rowLen-1]) + letterCheck(matrix[0][rowLen]) + letterCheck(matrix[0][rowLen -1])
        newRow.append(checkSum(sum, matrix[1][rowLen]))
        return newRow
    
    else:
        sum = letterCheck(matrix[0][0]) + letterCheck(matrix[0][1]) + letterCheck(matrix[1][1]) + letterCheck(matrix[2][0]) + letterCheck(matrix[2][1])
        newRow.append(checkSum(sum, matrix[1][0]))
        while colCount < (rowLen):
            sum = 0
            sum = letterCheck(matrix[0][colCount-1]) + letterCheck(matrix[0][colCount]) + letterCheck(matrix[0][colCount+1]) + letterCheck(matrix[1][colCount-1]) + letterCheck(matrix[1][colCount+1]) + letterCheck(matrix[2][colCount-1]) + letterCheck(matrix[2][colCount]) + letterCheck(matrix[2][colCount+1])
            newRow.append(checkSum(sum, matrix[1][colCount]))
            colCount+=1
        sum = 0
        sum = letterCheck(matrix[0][rowLen-1]) + letterCheck(matrix[0][rowLen]) + letterCheck(matrix[1][rowLen-1]) + letterCheck(matrix[2][rowLen-1]) + letterCheck(matrix[2][rowLen])
        newRow.append(checkSum(sum, matrix[1][rowLen]))
        return newRow
        
            

#This function provides the integer on return that will be added to the summation
def letterCheck(letter):
    if(letter == "a"):
        return 0
    elif(letter == "b"):
        return 1
    elif(letter == "c"):
        return 2

# Dr. Rees said modulo was not a good idea, so instead I hard coded a check for every number
# 0 times 8 = minimum = 0. 2 times 8 = maximum = 16
#This will just return the corresponding letter based on the sum of the neighbors and the current letter
def checkSum(sum, currentLetter):
    if (currentLetter == "a"): 
        if( sum == 2 or sum == 3 or sum == 5 or sum == 7 or sum == 11 or sum == 13):
            return "a"
        elif( sum == 0  or sum == 4 or sum == 6 or sum == 8 or sum == 10 or sum == 12 or sum == 14 or sum == 16):
            return "b"
        elif( sum ==1 or sum == 9 or sum == 15):
            return "c"
    elif (currentLetter == "b"): 
        if( sum == 2 or sum == 3 or sum == 5 or sum == 7 or sum == 11 or sum == 13):
            return "b"
        elif( sum == 0  or sum == 4 or sum == 6 or sum == 8 or sum == 10 or sum == 12 or sum == 14 or sum == 16):
            return "c"
        elif( sum ==1 or sum == 9 or sum == 15):
            return "a"
    elif (currentLetter == "c"): 
        if( sum == 2 or sum == 3 or sum == 5 or sum == 7 or sum == 11 or sum == 13):
            return "c"
        elif( sum == 0  or sum == 4 or sum == 6 or sum == 8 or sum == 10 or sum == 12 or sum == 14 or sum == 16):
            return "a"
        elif( sum ==1 or sum == 9 or sum == 15):
            return "b"

#This function is used in the summation of columns when deciphering the word (After the looped 100 iterations, not part of it)     
def finalCheck(letter):
    if(letter == "a"):
        return 0
    elif(letter == "b"):
        return 1
    if(letter == "c"):
        return 2

            




def main():
    """
    This section sets up argparse
    Inputs:
    "-i" for a defined inputFile: REQUIRED
    "-o" for a defined outputFile: REQUIRED
    "-s" for a defined scoring seed: REQUIRED
    "-p" for a defined number of processes which is > 0: NOT REQUIRED. DEFAULT = 1
    """
    parser = argparse.ArgumentParser()                                               
    parser.add_argument("--inputFile", "-i", type=str, required=True)
    parser.add_argument("--scoringSeed", "-s", type=str, required=True)
    parser.add_argument("--outputFile", "-o", type=str, required=True)
    parser.add_argument("--processes", "-p", type=int, required=False, default=1)
    args = parser.parse_args()

    #Error checking inputs
    if args.processes < 1:
        print("Error, integer passed as -p was not >= 1")
        exit()
    if len(args.scoringSeed) > 0:
        for letter in args.scoringSeed:
            if letter == "a" or letter == "b" or letter == "c":
                continue
            else:
                print("Error, invalid character in scoring seed")
                exit()
    else:
        print("Error -s either too short or doesn't exist")
        exit()


    #Opening input file and intializing variables
    openInput = open(args.inputFile, "r")
    inputString = openInput.readline()
    inputString = inputString.replace("\\n", "")
    inputString = inputString.strip()
    openInput.close()

    #Create a LxL matrix
    matrix = []
    for x in range(len(inputString)):
        list = [None] * len(inputString)
        matrix.append(list)

    #fill the LxL matrix with the scoring seed
    counter = 0
    maxCount = len(args.scoringSeed)
    scoreSeed = args.scoringSeed
    for row in matrix:
        for index in range(len(row)):
            row[index] = scoreSeed[counter]
            counter+=1
            if(counter >= maxCount):
                counter = 0

    #Concurrency is done with process pools
    processPool = Pool(processes=args.processes)
    #Start of the 100 iterations
    for x in range(100):
        poolData = []
        #Fill each element in poolData with a tuple of [matrix,rowIndex
        poolData.append([matrix[0:2], 0])
        for rowIndex in range(len(matrix)-2):
            matrixData = [matrix[rowIndex:rowIndex+3], rowIndex+1]
            poolData.append(matrixData)
        poolData.append([matrix[(len(matrix)-2):],len(matrix)-1])
        #Map the pooldata with the rowCalc function to return a completed matrix after calculation
        matrix = processPool.map(rowCalc, poolData)
        del (poolData)

    
    #Column summation for decryption
    decryptString = ""
    for y in range(len(inputString)):
        sum = 0
        for x in range(len(inputString)):
            sum += finalCheck(matrix[x][y])
        decryptString += decryptLetter(inputString[y],sum)
        




    f = open(args.outputFile, "w")
    f.write(decryptString + "\n")
    f.close()
    


if __name__ == '__main__':
    main()