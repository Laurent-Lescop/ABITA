#!/usr/bin/python
# -*- coding: utf-8 -*-

from .geom import Geom
from .population import Population
from .solution import Solution
from .tx import Tx

from typing import Union
from random import random

class Algo:
    """Class representing the main algorithm to solve the problem.
    
    Attributes
    ----------
    popu : Population
        The population in which we will store the results of the computation
    geom : Geometry
        The geometry of the problem describing the points, segments and elements
    nbSols : int
        The number of solutions to compute
    initIT : int
        The first iteration number
    endIT : int 
        The last iteration number
    _currentIT : int
        The current iteration number
    alpha : float
        A coefficient for solving the problem ?
    nbTypes : int
        Length of the typeList list
    typeList : List[Tx]
        List of all type of lots we have to use
    _minLots : int
        The minimum number of lots we want in each solution
    _maxLots : int
        The maxmimum number of lots we want in each solution
    
    Methods
    -------

    """


    def __init__(self, geom: Geom, popu: Population) -> None:
        """Init the algo object by default values.
        
        Parameters
        ----------
        geom : Geometry
            The geometry of the problem
        popu : Population
            An empty Population object to save in results of the algorithm
        """
        
        self.popu = popu
        self.geom = geom
        # initialise the iteration counter
        self._currentIT = 0
        # default values
        self.nbSols = 100
        self._minLots = 0
        self._maxLots = 0
        self.initIT = -1
        self.endIT = -1
        self.alpha = 0.0
        self.nbTypes = 0
        self.typeList = []
    

    def addType(self, type: Tx) -> None:
        """Add another type Tx to list of type.
        
        Parameters
        ----------
        type : Tx
            The new type to add.
        
        Returns
        -------
        None
        """

        #Check the argument
        if type is None:
            raise Exception("AddTypeError: null type")
        
        #Check if the argument already in list 
        for i in range(self.nbTypes):
            #probablement coder une fonction égal sur Tx.py
            if self.typeList[i] == type:
                raise Exception("AddTypeError: type already exists")

        #Add the type if not null nor already inside the list
        self.typeList.append(type)
        self.nbTypes += 1


    def evaluate(self, sol: Solution) -> None:
        """Calculate the fitness for each lot of a solution, and then the
        global fitness of the solution.
        
        Parameters
        ----------
        sol : Solution
            The solution from which we want to compute fitnesses
        
        Returns
        -------
        None
        """

        # Build lots if needed
        if sol.nbLots == 0:
            sol.setLots()
        
        # Initialize quantities
        sol.fitness = 0
        sumArea = sol.lotList[0].area

        for j in range(self.nbTypes):
            self.typeList[j].nb = 0
        
        # Compute fitness
        for i in range(1, sol.nbLots):
            lot = sol.lotList[i]

            # Compute the TYPE benefit
            for j in range(self.nbTypes):
                if (lot.area > self.typeList[j].areaMin and 
                    lot.area <= self.typeList[j].areaMax):
                    lot.fitness = lot.area * self.typeList[j].benefit
                    lot.typeNo = self.typeList[j].no
                    self.typeList[j].nb += 1

            # Add (or remove) bonus for good (bad) elements
            if lot.fitness > 0:
                for j in range(lot.nbElements):
                    lot.fitness += lot.elementList[j].bonus * lot.elementList[j].area
            
            # Penalize for aspect ration
            lot.fitness *= 1 + self.alpha * (lot.area/(lot.length**2) - 1)

            # Accumulate solution fitness
            sol.fitness += lot.fitness
            sumArea += lot.area
        
        # Penalize for out of bounds
        i=0
        for j in range(self.nbTypes):
            i += self.typeList[j].nb
            if (self.typeList[j].nb > self.typeList[j].nbMax or 
                self.typeList[j].nb < self.typeList[j].nbMin):
                sol.fitness = 0
                break

        if i != sol.nbLots - 1:
            sol.fitness = 0
        
        # Reduce benefits to unit area
        for i in range(1, sol.nbLots):
            sol.lotList[i].fitness /= sol.lotList[i].area
        sol.fitness /= sumArea

        # Sort lots for futur comparison
        sol.sortLots()



    def currentIteration(self):
        return self._currentIT
    

    def run(self) -> bool:
        """Run one iteration of the algorithm
        
        Parameters
        ----------
        None
        
        Returns
        -------
        A boolean, evaluated to True if we have to make other iterations,
        or False if we ended the process and solved the problem.
        """

        # declare the new population object
        newPopu = Population()

        # Initializing: first iteration
        if self._currentIT == 0:
            self._init()
            self.popu.sortSolutions()

        # Update the iteration counter
        self._currentIT += 1
        if self._currentIT > self.initIT + self.endIT:
            return False

        # Generate randomized solutions
        if self._currentIT <= self.initIT:
            newSol = Solution(self.geom)
            newSol.rndSet(self._rnd(self._minLots, self._maxLots))
            self.evaluate(newSol)

            if self.popu.insertSolution(newSol):
                newPopu.resize(self.popu.nbSolutions)
                for j in range(newSol.nbLots):
                    for k in range(newSol.lotList[j].nbSegments):
                        sol = Solution(newSol)
                        sol.swap(j, k)
                        self.evaluate(sol)
                        if not newPopu.insertSolution(sol):
                            del sol
                for i in range(newPopu.nbSolutions):
                    if self.popu.insertSolution(newPopu.solutionList[i]):
                        newPopu.solutionList[i] = None
            else:
                del newSol
        
        # Finish by local improvements
        else:
            newPopu.resize(self.popu.nbSolutions)
            for i in range(self.popu.nbSolutions):
                for j in range(self.popu.solutionList[i].nbLots):
                    for k in range(self.popu.solutionList[i].lotList[j].nbSegments):
                        newSol = Solution(self.popu.solutionList[i])
                        newSol.swap(j, k)
                        self.evaluate(newSol)
                        if not newPopu.insertSolution(newSol):
                            del newSol
            k = 0
            for i in range(newPopu.nbSolutions):
                if self.popu.insertSolution(newPopu.solutionList[i]):
                    newPopu.solutionList[i] = 0
                    k += 1
            if k == 0:
                return False
        
        # Evaluate the population
        self.popu.stats()
        return True


    def _rnd(self, low:Union[int, float], high:Union[int, float]) -> Union[int, float]:
        """Choose a random int or float between a low value and high value.
        In the following, A might be int or float.
        
        Parameters
        ----------
        low : A
            The low value
        high : A
            The high value
        
        Returns
        -------
        A random value of type A between low (included) and high (excluded)
        """
        val = (high - low) * random() + low
        val = high if val > high else low if val < low else val
        # NB: val is between low and high
        if isinstance(low, int) and isinstance(high, int):
            return int(val)
        elif isinstance(low, float) and isinstance(high, float):
            return val
    
    
    def _init(self) -> None:
        """Initiate the paramters of the algorithm from a geometry.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        sol = Solution(self.geom)

        # Set the default types if not already specified
        if self.nbTypes == 0:
            self.addType(Tx(70.,  30., 45.,  0, 1000, 1))
            self.addType(Tx(80.,  45., 60.,  0, 1000, 2))
            self.addType(Tx(100., 60., 75.,  0, 1000, 3))
            self.addType(Tx(50.,  75., 85.,  0, 1000, 4))
            self.addType(Tx(40.,  85., 100., 0, 1000, 5))

        # Compute the maximum number of lots
        from .lot import Lot
        lot = Lot(sol, 0)

        for i in range(self.geom.nbElements):
            if self.geom.elementList[i].common:
                lot.addElement(self.geom.elementList[i])
        lot.buildBorder()

        for i in range(self.geom.nbElements):
            self.geom.elementList[i].mark = False
        
        for i in range(lot.nbSegments):
            seg = lot.segmentList[i]
            if lot.contain(seg.e1):
                elt = seg.e2
            else:
                elt = seg.e1
            if elt is not None:
                elt.mark = True
        
        del lot
        
        self._maxLots = 0
        for i in range(self.geom.nbElements):
            if self.geom.elementList[i].mark:
                self._maxLots += 1

        sum = 0
        for i in range(self.nbTypes):
            sum += self.typeList[i].nbMax
        if self._maxLots > sum:
            self._maxLots = sum
        
        self._minLots = 1
        sum = 0
        for i in range(self.nbTypes):
            sum += self.typeList[i].nbMin
        if self._minLots < sum:
            self._minLots = sum

        # Update default values if not specified yet
        if self.initIT < 0:
            self.initIT = 250 * self._maxLots
        if self.endIT < 0:
            self.endIT = 10 * self._maxLots
        
        # Resize the population
        self.popu.resize(self.nbSols)

        # Evaluate the initializing population
        for i in range(self.popu.nbSolutions):
            self.evaluate(self.popu.solutionList[i])
            self.popu.stats()

