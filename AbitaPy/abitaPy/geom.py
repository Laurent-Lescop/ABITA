#!/usr/bin/python
# -*- coding: utf-8 -*-


from .element import Element
from .floor import Floor
from .point import Point
from .segment import Segment

class Geom:
    """
    Class describing a geometry
    
    Attributes
    ----------
    segmentList : list[Segment]
        List of segments composing the geometry
    nbSegments : int 
        Number of segments composing the geometry
    nbPoints : int
        Number of points composing the geometry
    nbElements : int
        Number of elements in the elementList
    nbFloors : int 
        Number of floors in floorList
    pointList : list[Point]
        List of points composing the geometry
    elementList : list[Element]
        List of elements composing the geometry
    floorList : list[Floor]
        List of the floors composing the geometry
    
    Methods
    -------
    __init__() -> None
        Creates an empty Geom instance 
    build() -> None
        Builds a geometry and sorts the elements by floor
    addPoint(pt:Point) -> None
        Adds a point to the geometry
    addElement(elt:Element) -> None
        Adds an element to the geometry
    addFloor(floor:Floor) -> None
        Adds a floor to the geometry (?)
    _addSegment(seg:Segment) -> int
        Adds a segment to the geometry
    """

    def __init__(self) -> None:
        """
        Default onstructor for an empty geometry

        Parameters
        ----------
        None
        """
        self.segmentList = []
        self.nbSegments = 0
        self.nbPoints = 0
        self.nbElements = 0
        self.nbFloors = 0
        self.pointList = []
        self.elementList = []
        self.floorList = []

    
    def build(self) -> None:
        """
        Method that builds a geometry and sorts the elements by floor
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # Close elements
        for i in range(self.nbElements):
            self.elementList[i].close()
        
        # Generate segment list
        for i in range(self.nbElements):
            elt = self.elementList[i]
            for j in range(elt.nbPoints-1):
                seg = Segment(elt.pointList[j], elt.pointList[j+1])
                self._addSegment(seg)
        
        #Brute force connectivity finding
        for i in range(self.nbElements):
            elt = self.elementList[i]
            for j in range(elt.nbPoints-1):
                p1 = elt.pointList[j]
                p2 = elt.pointList[j+1]
                for k in range(self.nbSegments):
                    seg=self.segmentList[k]
                    if (p1 == seg.p1 and p2 == seg.p2) or (p2 == seg.p1 and p1 == seg.p2):
                        seg.setElement(elt)
                        elt.segmentList[elt.nbSegments] = seg
                        elt.nbSegments += 1
                        break

        #Sort elements by floor
        for i in range(self.nbElements):
            for j in range(self.nbFloors):
                if self.elementList[i].floorId == j:
                    self.floorList[j].addElement(self.elementList[i])



    def addPoint(self, pt:Point) -> None:
        """
        Method that adds a point to the geometry
        
        Parameters
        ----------
        pt : Point
            The point to add to the geometry
        
        Returns
        -------
        None
        """

        # check if the point is not null
        if pt is None :
            raise Exception("AddPointError : null pt")
        # check if pointlist is not none
        if self.pointList is None:
            raise Exception("AddPointError : null pointList")
        # check if element is not already added
        for i in range(self.nbPoints):
            if pt == self.pointList[i]:
                raise Exception("AddPointError : pt P{} already defined".format(pt.no))
        # add the point
        self.pointList.append(pt)
        self.nbPoints += 1


    def addElement(self, elt:Element) -> None:
        """
        Method that adds an element to the geometry
        
        Parameters
        ----------
        elt : Element
            The element to add to the geometry

        Returns
        -------
        None
        """

        # check if the element is an element 
        if elt is None :
            raise Exception("AddElementError : null elt")
        # check if pointlist is not none
        if self.elementList is None:
            raise Exception("AddElementError : null elementList")
        # check if element is not already added
        for i in range(self.nbElements):
            if elt == self.elementList[i]:
                raise Exception("AddElementError : elt E{} already defined".format(elt.no))
        # add the element
        self.elementList.append(elt)
        elt.index = self.nbElements
        self.nbElements += 1


    def addFloor(self, floor:Floor) -> None:
        """
        Method that adds a floor to the geometry
        
        Parameters
        ----------
        floor : Floor
            The floor to add to the geometry

        Returns
        -------
        None
        """
        # check if the floor is not null
        if floor is None :
            raise Exception("AddFloorError : null floor")
        # check if floorlist is not none
        if self.floorList is None:
            raise Exception("AddFloorError : null floorList")
        # check if element is not already added
        for i in range(self.nbFloors):
            if floor == self.floorList[i]:
                raise Exception("AddFloorError : floor F{} already defined".format(floor.no))
        # add the element
        self.floorList.append(floor)
        self.nbFloors += 1


    def _addSegment(self, seg:Segment) -> Segment:
        """
        Method that adds a segment to the geometry
        
        Parameters
        ----------
        seg : Segment
            The segment to add to the geometry

        Returns
        -------
        seg : Segment
            Return the passed segment if already added
        """

        # check if the segment is not null
        if seg is None :
            raise Exception("AddSegmentError : null seg")
        # check if floorlist is not none
        if self.segmentList is None:
            raise Exception("AddSegmentError : null segmentList")
        # check if floor is not already added
        for i in range(self.nbSegments):
            if seg == self.segmentList[i]:
                return seg
        # add the element
        self.segmentList.append(seg)
        self.nbSegments += 1
        return None

