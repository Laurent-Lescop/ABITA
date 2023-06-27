#!/usr/bin/python
# -*- coding: utf-8 -*-

from statistics import mean
from .solution import Solution

class Population:
    """A class which represents a population, that is to
    say the set of all solutions calculated, with some
    statistics. In one word, the result of the algorithm.
    
    Attributes
    ----------
    nbTest : int
        Number of tests done
    maxFitness : float
        The maximum fitness (what is a fitness?)
    minFitness : float
        The minimum fitness
    avgFitness : float
        The average fitness
    nbSolutions : int
        Number of solutions in the list solutionList
    solutionList : List[Solution]
        The list of all solutions calculated
    _sizeMax : int
        The maxmimum size of the list of solutions
    
    Methods
    -------
    __init__() -> None
        The constructor of the class
    addSolution(sol : Solution) -> None
        Add a solution to the end of the list
    removeSolution(index : int) -> None
        Remove a solution in the list at a given index
    insertSolution(sol : Solution) -> boolean
        Insert a solution in the list according to its fitness
    resize(sizeMax : int) -> None
        Change the value of _sizeMax
    sortSolutions() -> None
        Sort the list of solutions by fitness
    stats() -> None
        Compute the statistics
    """

    def __init__(self) -> None:
        """Constructor of the class Population. All 
        attributes are set to zero (except _sizeMax).
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.nbTest = 0
        self.maxFitness = 0
        self.minFitness = 0
        self.avgFitness = 0
        self.nbSolutions = 0
        self.solutionList = []
        self._sizeMax = 2147483647  # we suppose it's for capacity memory
    

    def addSolution(self, sol:Solution) -> None:
        """Add another solution in the list of all solutions.
        
        Parameters
        ----------
        sol : Solution
            The new solution to add
        
        Returns
        -------
        None
        """

        # check if the solutions is a solution 
        if sol is None:
            raise Exception("Population.addSolution(sol) : sol is none")
        # check if solution is not already added
        for s in self.solutionList:
            if (s == sol):
                raise Exception("Population.addSolution(sol) : sol already added")
        # add the solution
        self.solutionList.append(sol)
        self.nbSolutions += 1


    def removeSolution(self, index:int) -> None:
        """Remove a solution based on its index
        
        Parameters
        ----------
        index : int
            The index of the solution in the list to be removed
        
        Returns
        -------
        None
        """

        # check the index is correct
        if index < 0 or index > self.nbSolutions-1:
            return
        # remove the solution
        self.solutionList.pop(index)
        self.nbSolutions -= 1
        

    def insertSolution(self, sol: Solution) -> bool:
        """Insert a solution at its place, ordered
        by fitnesses. Returns true if added, else false.
        
        Parameters
        ----------
        sol : Solution
            The solution to insert
        
        Returns
        -------
        added : boolean
            True if added in the list, false otherwise
        """

        # first solution: add it directly in the list
        if self.nbSolutions == 0 and self._sizeMax > 0:
            self.addSolution(sol)
            return True
        # check if solution is already in the list
        for s in self.solutionList:
            if s == sol:
                return False
        self.nbTest += 1
        # get the position where we want to place sol
        i = 0
        while i < self.nbSolutions and sol.fitness <= self.solutionList[i].fitness:
            i += 1
        # insert the solution
        if i == self.nbSolutions:
            if self.nbSolutions == self._sizeMax:
                return False
            self.addSolution(sol)
            return True
        else:
            if self.nbSolutions == self._sizeMax:
                self.removeSolution(self.nbSolutions-1)
            self.addSolution(sol)
            for j in range(self.nbSolutions-1, i, -1):
                self.solutionList[j] = self.solutionList[j-1]
            self.solutionList[i] = sol
            return True


    def resize(self, sizeMax: int) -> None:
        """Change the value of the sizeMax attribute.
        
        Parameters
        ----------
        sizeMax : int
            The new sizeMax to use
        
        Returns
        -------
        None
        """

        if sizeMax < 0:
            return
        for i in range(sizeMax, self.nbSolutions):
            self.removeSolution(i)
        self._sizeMax = sizeMax
    

    def sortSolutions(self) -> None:
        """Sort the list of solution by decreasing fitness
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.solutionList = sorted(
            self.solutionList, 
            key = lambda sol: -sol.fitness
        )
        

    def stats(self) -> None:
        """Compute the minimum, maximum, and average 
        fitness of the list of solutions.
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        # calculate the list of fitnesses
        fitList = [s.fitness for s in self.solutionList]
        # if empty, set to zero so as to have all stats to zero
        if len(fitList)==0: fitList = [0]
        # compute the stats
        self.maxFitness = max(fitList)
        self.minFitness = min(fitList)
        self.avgFitness = mean(fitList)
