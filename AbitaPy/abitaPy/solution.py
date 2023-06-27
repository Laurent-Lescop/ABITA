#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Any
from random import random

class Solution:
    """Class representing a solution, ie a configuration
    of the elements regrouped in lots.

    Attributes
    ----------
    mark : bool
        If the element is marked or not
    fitness : float
        The score of this solution
    lotList : List[Lot]
        The list of lots which defines this solution
    elementList : List[Element]
        The list of elements we use
    distribution : List[int]
        A list registering the lot where each element is.
        For example: distribution[elt.index] = index of the lot in listLot,
        with elt.index the index of the element in elementList (which is shared
        accross all solutions and geometry)
    nbLots : int
        The length of the lot list
    nbElements : int
        The length of the element list
    
    Methods
    -------
    __init__(sol_or_geom : Union[Solution, Geom]) -> None
        Constructor of the class
    setLots() -> None
        Create the lot list from the chosen distribution
    swap(lotID:int, segID:int) -> boolean
        *We don't know what it does*
    sortLots() -> None
        Sort the list of lots following the distribution
    rndSet(nbSeeds:int) -> None
        *We don't know what it does*
    __eq__(other:Solution) -> boolean
        Implements the == operator
    __ne__(other:Solution) -> boolean
        Implements the != operator
    """


    def __init__(self, solOrGeom:Any=None) -> None:
        """Constructor of the Solution class. You can create a Solution object
        in three ways:
        ->  without args, by calling Solution(): 
            all attributes are set to zero or an empty list
        ->  with another solution as arg, by calling Solution(sol:Solution):
            the constructor then copies data from this solution
        ->  with a geometry as arg, by calling Solution(geom:Geometry):
            the construcor take some interresting data from the geometry
        
        Parameters
        ----------
        solOrGeom : Union[Solution, Geom], optional
            The solution or geometry we want to pass as an arg, default to None
        """

        self.mark = False
        self.fitness = 0
        self.nbLots = 0
        self.lotList = []
        self.nbElements = 0
        self.elementList = []
        self.distribution = []
        # constructor if called with a geometry
        from .geom import Geom
        if isinstance(solOrGeom, Geom):
            geom = solOrGeom
            if self.nbElements > 0:
                raise Exception("Already initialized")
            self.nbElements = geom.nbElements
            self.elementList = geom.elementList
            self.distribution = [-1] * self.nbElements
        # constructor if called with a solution
        elif isinstance(solOrGeom, Solution):
            sol = solOrGeom
            self.nbElements = sol.nbElements
            self.elementList = sol.elementList
            self.distribution = [i for i in sol.distribution]
            self.setLots()
        # error if solOrGeom not correct type
        elif solOrGeom is not None:
            raise Exception("solOrGeom is neither a solution or a geometry")



    def setLots(self) -> None:
        """Create the lot list from the elementList and the given distribution.
        
        No parameters, no returns
        """
        
        # check if we have elements
        if self.nbElements == 0: return
        # Clean the current lot list
        self.lotList = []
        # Count the lots
        self.nbLots = max(self.distribution) + 1
        if self.nbLots == 0: return
        # create new lotList
        from .lot import Lot
        for i in range(self.nbLots):
            self.lotList.append(Lot(self, i))
        # build each lot from the distribution :
        # set element list
        for j in range(self.nbElements):
            lotID = self.distribution[j]
            if lotID > -1:
                self.lotList[lotID].addElement(self.elementList[j])
        # build borders
        for lot in self.lotList:
            lot.buildBorder()
        

    def swap(self, lotID:int, segID:int) -> bool:
        """I think it does something, but I don't know what..."""

        if self.nbLots < 2:
            return False
        
        # check the lot ID
        if lotID > self.nbLots-1 or lotID < 0:
            return False
        lot = self.lotList[lotID]

        # check the seg ID
        if segID > lot.nbSegments-1 or segID < 0:
            return False
        seg = lot.segmentList[segID]

        # check if neighbour element exists and not imposed
        elt = seg.e2 if lot.contain(seg.e1) else seg.e1
        if elt is None or elt.imposed:
            return False
        
        # check neighbour lot
        nlot = self.distribution[elt.index]
        if lotID == 0 and not elt.common:
            return False
        if self.lotList[nlot].nbElements < 2:
            return False
        
        # check if neighbour lot remains connex
        if nlot > 0 and not self.lotList[nlot].stillConnex(elt):
            return False
        
        # check if neighbour lot remains connected
        if lotID > 0:
            j = 0
            while j < elt.nbSegments:
                seg = elt.segmentList[j]
                next = seg.nextOf(elt)
                i = -1 if next is None else self.distribution[next.index]
                if i > -1 and i != lotID:
                    if not self.lotList[i].stillConnected(elt):
                        break
                j += 1
            if j < elt.nbSegments:
                return False
        
        # remove elt from neighbour
        self.lotList[nlot].removeElement(elt)

        # add element to the lot
        lot.mergeElement(elt)
        return True


    def sortLots(self) -> None:
        """Sort the list of Lots following distribution order and
        rebuild the distribution according the new order.
        
        No parameters, no returns
        """

        if self.nbLots < 2: return

        # save list
        oldList = self.lotList

        # create new list
        self.lotList = [None] * self.nbLots
        self.lotList[0] = oldList[0]

        # sort lotList following distribution order
        # Note from the traductor (C++=>Python): I don't understand what it does
        # exactly, so I keep the C++ way so it should work
        i=0; j=1
        while i < self.nbElements and j < self.nbLots:
            k = 0
            while k < j and oldList[self.distribution[i]] != self.lotList[k]:
                k += 1
            if k == j:
                self.lotList[j] = oldList[self.distribution[i]]
                j += 1
            i += 1
        
        # rebuild the distribution
        for i in range(self.nbLots):
            self.lotList[i].index = i
            for elt in self.lotList[i].elementList:
                self.distribution[elt.index] = i
            


    def rndSet(self, nbSeeds:int) -> None:
        """This function is really weird, I wrote it from the C++ code but I can
        hardly say what it does exactly... Netherless, it should work."""

        if self.nbElements == 0: return

        # maxmimum fill of the outbuildings
        nelt = 0
        for i in range(self.nbElements):
            if self.elementList[i].common and self.distribution[i] < 0:
                self.distribution[i] = 0
                nelt += 1
        
        # seed the domain: not optimal yet
        nb = 0
        j = None
        while nb < nbSeeds:
            imax = self.nbElements - nelt - 1
            i = int((imax+1)*random())
            i = imax if i > imax else i
            k = -1
            while k < i:
                j = 0
                # for each element
                while j < self.nbElements:
                    # if it is not already in a lot : j == -1
                    if self.distribution[j] < 0:
                        elt = self.elementList[j]
                        # for each neighbour element
                        for l in range(elt.nbSegments):
                            seg = elt.segmentList[l]
                            next = seg.nextOf(elt)
                            if next is not None:
                                if self.distribution[next.index] == 0:
                                    k += 1
                                    break
                    if k == i:
                        break
                    j += 1
            nb += 1
            nelt += 1
            # WARNING : we add a condition to correct a bug, but this condition
            # was not in the legacy code
            self.distribution[j] = nb
        
        # build the lots
        self.setLots()

        # diffusing filling (not for lot 0)
        nb = 1
        while nb > 0:
            nb = 0
            for lot in self.lotList:
                if lot.index !=0 and lot.diffuse():
                    nb += 1
        
        # complete empty zones if ever
        nb = 1
        while nb > 0:
            nb = 0
            for i in range(self.nbElements):
                if self.distribution[i] < 0:
                    nb += 1
                    self.distribution[i] = self.nbLots
                    self.setLots()
                    while self.lotList[-1].diffuse():
                        pass
        


    def __eq__(self, other) -> bool:
        """Define == operator for solutions. Two solutions are equal if they
        have the same list element (in adresses) and the same distribution 
        (in values).
        
        Paramaters
        ----------
        other : Solution
            The other solution we want to check with
        
        Returns
        -------
        A boolean indicate whether the two solutions are equal or not. If the
        type of the "other" arg is not Solution, returns notImplemented.
        """
        
        if isinstance(other, Solution):
            if (self.nbLots != other.nbLots or 
                self.nbElements != other.nbElements or
                self.elementList != other.elementList):
                return False
            for i in range(self.nbElements):
                if self.distribution[i] != other.distribution[i]:
                    return False
            return True
        else:
            return NotImplemented


    def __ne__(self, other) -> bool:
        """
        Define != operator by opposition to the == operator.
        See documentation of == operator for more infos.
        """
        return not(self.__eq__(other))
