#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from .solution import Solution
from .segment import Segment
from .element import Element
from .point import Point

class Lot:
    """
    Class representing a lot, ie a set of elements which 
    correspond to a certain space to allocate for a flat
    or common space. 
    
    Attributes
    ----------
    fitness : float
        The value (score) of the lot
    length : float
        The length of the border of the lot (perimeter of the lot)
    index : int
        The index of this lot in the list of lot
    common : boolean
        If this lot is marked as common or not
    area : float
        The area of this lot
    typeNo : int
        The numero of the type the lot is
    solution : Solution
        The global solution in which this lot exists
    segmentList : List[Segment]
        The list of segments defining the border of the lot
    elementList : List[Element]
        The list of elements defining the lot
    nbElements : int
        Length of the element list
    nbSegments : int
        Length of the segment list
    
    Methods
    -------
    I'm lazy sorry, perhaps one day?
    """
    
    def __init__(self, sol:Solution, index:int) -> None:
        """
        Default constructor for a predefined lot

        Parameters
        ----------
        sol : Solution
            The solution associated to this lot
        index : int
            The index of the lot

        Returns
        -------
        None
        """

        self.fitness = 0.0
        self.length = 0.0
        self.index = index
        self.common = False
        self.area = 0.0
        self.typeNo = 0
        self.solution = sol
        self.segmentList = []
        self.elementList = []
        self.nbElements = 0
        self.nbSegments = 0


    def stillConnex(self, removed:Element) -> bool:
        """Check if all elements are still connected one to each other (that is
        to say the graph representing the elements of the lot is still connex)
        if we remove the given element from the lot.
        
        Parameters
        ----------
        removed : Element
            The element we want to remove
        
        Returns
        -------
        A boolean :
            True if the lot is still connex if we remove the element
            False if not
        """

        # Check that the element is in this lot
        lot = removed.getLot(self.solution)
        if lot != self.index:
            return False

        # Check that the element can be removed
        if self.nbElements < 2 or removed.imposed:
            return False

        # Initialize the marks
        for i in range(self.nbElements):
            self.elementList[i].mark = False
        removed.mark = True

        # Get first neigbour in this lot
        elt = None
        for seg in removed.segmentList:
            elt = seg.nextOf(removed)
            if elt is not None and elt.getLot(self.solution) == self.index:
                break

        # Diffuse the marks from first neigbour in this lot
        self._markFrom(elt)

        # Count the marks
        nb = 0
        for elt in self.elementList:
            if elt.mark: nb += 1
        
        # Return true if all elements have been marked
        return nb == self.nbElements

    
    def stillConnected(self, removed:Element) -> bool:
        """Check if the current lot is still connected to an entrance 
        (or a common lot) if we remove the given element from the lot.
        
        Parameters
        ----------
        removed : Element
            The element we want to remove
        
        Returns
        -------
        A boolean:
        1. In case of the common lot: 
            return true if every element remains connected to at least one 
            entrance
        2. In case of other lots :
            return true if the lot keeps contact to the lot 0 (the common lot)
        """

        # Retrieve the lot of the removed element
        lot = removed.getLot(self.solution)

        # The element is in lot 0
        if lot == 0:

            # Case of the common lot
            if self.common:

                # Eliminate the imposed elements
                if removed.imposed:
                    return False

                # Initialise the marks
                for i in range(self.nbElements):
                    self.elementList[i].mark = self.elementList[i].exit
                removed.mark = True

                # Diffuse the marks from entrance
                for elt in self.elementList:
                    if elt.exit:
                        self._markFrom(elt)
                
                # Count the marks
                nb = 0
                for elt in self.elementList:
                    if elt.mark: nb += 1
                
                # return true if all elements have been marked
                return nb == self.nbElements
            
            # Case of the other lots
            else:

                for seg in self.segmentList:
                    # Retrieve the neighbour element
                    elt = seg.e2 if self.contain(seg.e1) else seg.e1
                    # If the neighbour exist check its lot
                    if elt is not None and elt != removed:
                        if elt.getLot(self.solution) == 0:
                            return True
                
                return False
        
        # case elt is not in lot 0
        else:

            if lot != self.index:
                return True
            else:

                for seg in self.segmentList:
                    if removed != seg.e1 and removed != seg.e2:
                        # Retrieve the neighbour element
                        elt = seg.e2 if self.contain(seg.e1) else seg.e1
                        # If the neighbour exists check its lot
                        if elt is not None and elt != removed:
                            if elt.getLot(self.solution) == 0:
                                return True
                
                return False


    def diffuse(self) -> bool:
        """Diffuse the lot: look after all neighbours elements of the lot 
        and then merge the first which is not yet in another lot, or marked
        as imposed common.

        Parameters
        ----------
        None

        Returns
        -------
        A boolean:
            True if an element was merged
            False if no element was merged
        """

        for i in range(self.nbSegments):
            seg = self.segmentList[i]
            
            # retreive the neighbour element
            elt = seg.e2 if self.contain(seg.e1) else seg.e1

            # if the neighbour exists
            if elt is not None:
                lotID = elt.getLot(self.solution)

                # if the neighbour is free, merge it
                if lotID < 0 and not elt.imposed:
                    if self.mergeElement(elt): return True
                
                # else if neighbour in common test before merging
                elif lotID == 0 and not elt.imposed:

                    # test if neighbour lot remains connected
                    j = 0
                    while j < elt.nbSegments:
                        seg = elt.segmentList[j]
                        nextElt = seg.nextOf(elt)
                        lotID = (-1 if nextElt is None 
                                    else nextElt.getLot(self.solution))
                        if lotID > -1 and lotID != self.index:
                            if not self.solution.lotList[lotID].stillConnected(elt):
                                break
                        j += 1
                    
                    if j == elt.nbSegments:
                        # remove element from common lot
                        self.solution.lotList[0].removeElement(elt)
                        # add element to this lot
                        if self.mergeElement(elt): return True
        
        # return false if no element merged
        return False
                    


    def buildBorder(self) -> None:
        """Method that builds the border of the lot

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # for each element
        for j in range(self.nbElements):
            elt = self.elementList[j]
            # for each segment of each element
            for i in range(elt.nbSegments):
                seg = elt.segmentList[i]
                # if the element on the other side of the segment is in the lot,
                # segment must not be in the border list, else it must be.
                elt2 = seg.nextOf(elt)
                if self.contain(seg.nextOf(elt)):
                    self._removeSegment(seg)
                else:
                    self._addSegment(seg)
        


    def contain(self, elt:Element) -> bool:
        """
        Method that checks if an element is contained is the solution associated to this lot

        Parameters
        ----------
        elt : Element
            The element that must be checked

        Returns
        -------
        bool : Boolean
            Wether or not the element is contained is the lot
        """
        if elt is None:
            return False
        else:
            return (self.index == elt.getLot(self.solution))
    

    def addElement(self, elt:Element) -> None:
        """Add an element to the element list. Build a predifined valid lot. 
        Don't build the border so that elements can be added in any order.
        
        Parameters
        ----------
        elt : Element
            The element to add to the geometry

        Returns
        -------
        None

        Exceptions
        ----------
        Raises an exception if :
            element is None or 
            element is already in the list
        """

        # check if the element is an element 
        if elt is None :
            raise Exception("AddElementError : null elt")
        
        # check if element is not already added
        for e in self.elementList:
            if elt == e:
                raise Exception("AddElementError : elt E{} already defined".format(elt.index))
        
        #add the element to the list
        self.elementList.append(elt)
        self.nbElements += 1

        # Update the solution distribution
        self.solution.distribution[elt.index]=self.index
        if elt.exit: self.common=True

        # update area
        self.area += elt.area
    

    def mergeElement(self, elt:Element) -> bool:
        """Merge a neighbour element to the lot and rebuild the border so that 
        elements have to be added in a valid order (e.g. diffusion algo).
        
        Parameters
        ----------
        elt : Element
            The element we want to add
        
        Returns
        -------
        A boolean :
            - True if the element was added
            - False if not (that means that elt is None or that it is already in
              the list)
        """

        if elt is None: return False

        for e in self.elementList: 
            if e == elt: return False
        
        # add the element tp the list
        self.elementList.append(elt)
        self.nbElements += 1

        # rebuild border list of segments
        for seg in elt.segmentList:
            if self.contain(seg.nextOf(elt)):
                self._removeSegment(seg)
            else:
                self._addSegment(seg)
        
        # update the solution distribution
        self.solution.distribution[elt.index] = self.index

        # update area
        self.area += elt.area
        
        return True



    def removeElement(self, elt:Element) -> bool:
        """Removing an element from the lot.
        
        Parameters
        ----------
        elt : Element
            The element to remove
        
        Returns
        -------
        A boolean :
            True if the element was found and removed
            False if the element was not found
        """

        for i in range(self.nbElements):
            if self.elementList[i] == elt:

                # remove element
                self.elementList.pop(i)
                self.nbElements -= 1

                # rebuild the border
                for seg in elt.segmentList:
                    if self.contain(seg.nextOf(elt)):
                        self._addSegment(seg)
                    else:
                        self._removeSegment(seg)
                
                # update the solution distribution
                self.solution.distribution[elt.index] = -1

                # update area
                self.area -= elt.area

                # exit
                return True
        
        # if element was not found
        return False
                


    def _markFrom(self, elt:Element) -> None:
        """Diffuse a mark from elt to all neighbours which are in the same lot.
        Recursive call. No diffusion from already marked elements. 
        The attribute mark must be initialised for all elements.

        This method allows to check if all elements of a lot are connected one
        to each other (see the method stillConnex), by exploring all neighbours
        of an element recursively.

        Parameters
        ----------
        elt : Element
            The source element from which we began the diffusion

        Returns
        -------       
        None
        """

        elt.mark = True
        for i in range(elt.nbSegments):
            next = elt.segmentList[i].nextOf(elt)
            if next is not None :
                if next.getLot(self.solution)==self.index and not next.mark:
                    next.mark = True
                    self._markFrom(next)



    def _addSegment(self, seg:Segment) -> None:
        """
        Method that adds a segment to the list of border segments of the lot
        
        Parameters
        ----------
        seg : Segment
            The segment to add to the border of the lot

        Returns
        -------
        None
        """
        
        self.segmentList.append(seg)
        self.nbSegments += 1
        #update length
        self.length += seg.length


    def _removeSegment(self, seg:Segment) -> None:
        """Remove a segment from the list of segments representing the border
        of the lot. Update also nbSegments and length attributes.
        
        Parameters
        ----------
        seg : Segment
            The segment to remove
        
        Returns
        -------
        None
        """
        
        try:
            self.segmentList.remove(seg)
            self.nbSegments -= 1
            self.length -= seg.length
        except ValueError:
            # segment to remove is not in the list
            pass


    def getPointList(self) -> List[Point]:
        """Get the list of all the points defining the border of the lot,
        following the order of the border.

        Parameters
        ----------
        None

        Returns
        -------
        A list of Point representing the border of the lot
        """

        # if empty
        if len(self.segmentList) == 0: return []
        # we use the marks to know if we have visited a segment
        # init
        for seg in self.segmentList:
            seg.mark = False
        # take the points of the first segment
        prevSeg = self.segmentList[0]
        prevSeg.mark = True
        pointList = [prevSeg.p1, prevSeg.p2]
        # while we do not have all the points
        while len(pointList) != len(self.segmentList):
            for nextSeg in self.segmentList:
                # we try to find the segment which is linked to the previous one
                # and when we find it, we mark it as read and search the next
                # one in the list
                if not nextSeg.mark and nextSeg.p1 == pointList[-1]:
                    pointList.append(nextSeg.p2)
                    nextSeg.mark = True
                    prevSeg = nextSeg
                    break
                if not nextSeg.mark and nextSeg.p2 == pointList[-1]:
                    pointList.append(nextSeg.p1)
                    nextSeg.mark = True
                    prevSeg = nextSeg
                    break
        # when we have all points in order, return it
        return pointList

                    




