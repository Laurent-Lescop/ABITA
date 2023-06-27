#!/usr/bin/python
# -*- coding: utf-8 -*-

from .point import Point
from .solution import Solution

class Element:
    """Class representing a space element, ie a polygon, a space or a room.
    
    Attributes
    ----------
    bonus : float
        The bonus set to the element
    mark : boolean
        Whether this element is set as marked or not
    no : int
        The numero of this element
    floorId : int
        The id of the floor where this element is
    index : int
        The index of this element in the list of elements
    exit : boolean
        True if the element is set as an exit
    common : boolean
        True if the element can be a common place
    imposed : boolean
        True if the element must be a common place
    area : float
        The surface of the element
    nbPoints : int
        The length of the point list
    nbSegments : int
        The length of the segment list
    pointList : List[Point]
        The list of points defining the element
    segmentList : List[Segment]
        The list of segments defining the element

    Methods
    -------
    getLot(sol: Solution) -> int
        get the lot in a solution where the element is
    addPoint(p: Point) -> None
        add a point to the element
    close() -> None
        Close the element when we give all points    
    """

    
    def __init__(self, floorId: int, no: int) -> None:
        """Constructor for Element

        Parameters
        ----------
        floorId : int
            The id of the floor of the element
        no : int
            The numero of the element
        """

        self.no = no
        self.floorId = floorId
        self.bonus = 0
        self.mark = None
        self.index = -1
        self.exit = False
        self.common = False
        self.imposed = False
        self.area = 0
        self.nbPoints = 0
        self.nbSegments = 0
        self.pointList = []
        self.segmentList = []


    def getLot(self, sol: Solution) -> int:
        """Get the index of the lot in the solution where 
        this element is attributed.
        
        Parameters
        ----------
        sol : Solution
            A solution with several lots
        
        Returns
        -------
        lotId : int
            The index of the lot where this element is
        """
        if self.index < 0:
            return -1
        else:
            return sol.distribution[self.index]
    
    
    def addPoint(self, p: Point) -> None:
        """Add a point to the element.
        
        Parameters
        ----------
        p : Point
            A point
        
        Returns
        -------
        None
        """
        self.pointList.append(p)
        self.nbPoints += 1


    def close(self) -> None:
        """Close the perimeter of the element, add the first point
        to the end of the point list, compute the area and generate
        an empty segment list.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # check number of points
        if self.nbPoints < 2:
            raise Exception("Cannot close element: not enough points!")

        # add first point in last position
        self.addPoint(self.pointList[0])

        # compute area
        p1 = None
        p2 = self.pointList[0]
        self.area = 0
        for i in range(1, self.nbPoints):
            p1 = p2
            p2 = self.pointList[i]
            self.area += p2.x * p1.y - p1.x * p2.y
        self.area *= 0.5
        if self.area < 0:
            self.area *= -1
        if self.area == 0:
            raise Exception("Cannot close element: area is null")
        
        # generate empty segment list
        self.segmentList = [None for _ in range(self.nbPoints-1)]
        
