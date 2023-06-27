#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main file of the solver"""

import sys
import logging
from typing import Tuple, List
from .abiFile import AbiFile
from .algo import Algo
from .geom import Geom
from .population import Population


HELP_MESSAGE = """
Usage: python3 -m abitaPy [option]
       python3 -m abitaPy [option] inputfilename
       python3 -m abitaPy [option] inputfilename outputfilename
       python2 -m abitaPy2 [option]
       python2 -m abitaPy2 [option] inputfilename
       python2 -m abitaPy2 [option] inputfilename outputfilename

Options:
  -h, --help       show this help message and exit
"""

logging.basicConfig(format="%(levelname)s: %(message)s")


def getFileNames(*args: List[str]) -> Tuple[str, str]:
    """Get the name of the files for input and output.
    
    Parameters
    ----------
    args: str[]
        The list of arguments passed to the command
    
    Returns
    -------
    fileNameIn, fileNameOut: str, str
        A tuple with the names of the input and output files.
    """

    print("#####################################")
    print("##                                 ##")
    print("##          AbitaPy v1.0           ##")
    print("##                                 ##")
    print("#####################################")

    # get the input and output files name, from command line
    # or directly from user if not given
    if len(args) == 0:
        fileNameIn = input("Type the input file name: ")
        fileNameOut = input("Type the output file name: ")
    elif len(args) == 1:
        fileNameIn = args[0]
        fileNameOut = ""    
    elif len(args) == 2:
        fileNameIn = args[0]
        fileNameOut = args[1]
    else:
        print(HELP_MESSAGE)
        exit()

    # error : no input file name
    if len(fileNameIn) == 0:
        raise Exception("Please enter a file name.")

    # add ".abi" extension if absent and create automatic 
    # output file name if needed
    if len(fileNameIn) < 4 or fileNameIn[-4:] != ".abi":
        fileNameIn = fileNameIn + ".abi"
    if len(fileNameOut) == 0:
        fileNameOut = '{}_solved.abi'.format(fileNameIn[:-4])
    if len(fileNameOut) < 4 or fileNameOut[-4:] != ".abi":
        fileNameOut = fileNameOut + ".abi"
    print('Input file: {}'.format(fileNameIn))
    print('Output file: {}'.format(fileNameOut))

    return fileNameIn, fileNameOut


def readInput(fileNameIn: str) -> Tuple[Geom, Population, Algo]:
    """Read a file and construct the apropriate geom, popu and algo objects.
    
    Parameters
    ----------
    fileNameIn: str
        The name of the input file
    
    Returns
    -------
    geom: Geom
        The geometry of the problem
    popu: Population
        The population of the algorithm
    algo:
        The algorithm parameters
    """

    geom = Geom()
    popu = Population()
    algo = Algo(geom, popu)
    file = AbiFile(fileNameIn)
    file.read(geom, popu, algo)
    return geom, popu, algo


def solveProblem(geom: Geom, popu: Population, algo: Algo) -> None:
    """Solve the given problem. Update geom, popu and algo during the execution.
    
    Parameters
    ----------
    geom: Geom
        The geometry of the problem
    popu: Population
        The population of the algorithm
    algo:
        The algorithm parameters
    """

    print("")
    print("")
    print("             statistics              ")
    print("-------------------------------------")
    print(" iter   minimun    average    maximum")
    print("-------------------------------------")
    print("")
    while algo.run():
        if ((algo.currentIteration() < algo.initIT and 
            algo.currentIteration() % 1000 == 0) or
            algo.currentIteration() >= algo.initIT):
            print("{:>5d} {:>8.2f} {:>10.2f} {:>10.2f}".format(
                algo.currentIteration(),
                popu.minFitness,
                popu.avgFitness,
                popu.maxFitness
            ))
    print("-------------------------------------")


def saveOuput(geom: Geom, popu: Population, algo: Algo, fileNameOut: str) -> None:
    """Save the solution in a file.
    
    Parameters
    ----------
    geom: Geom
        The geometry of the problem
    popu: Population
        The population of the algorithm
    algo:
        The algorithm parameters
    fileNameOut: str
        The name of the file in which we want to save the results
    """

    file = AbiFile(fileNameOut)
    file.write(geom, popu, algo)
    print("")
    print('Results saved in {}'.format(fileNameOut))


def main():
    """Run the main program."""
    args = sys.argv[1:]
    if len(args) > 0 and (args[0] == "-h" or args[0] == "--help"):
        print(HELP_MESSAGE)
        exit()
    fileNameIn, fileNameOut = getFileNames(*args)
    geom, popu, algo = readInput(fileNameIn)
    solveProblem(geom, popu, algo)
    saveOuput(geom, popu, algo, fileNameOut)
    

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logging.error(err)