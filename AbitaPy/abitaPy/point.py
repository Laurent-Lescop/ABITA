#!/usr/bin/python
# -*- coding: utf-8 -*-


class Point:
    """
    Class representing a simple 2D point. This 
    implementation supports the lexicographic order.

    Attributes
    ----------
    x : float
        The X coordinate of the Point
    y : float
        The Y coordinate
    floorId : int
        The index of the floor where the point is
    no : int
        The numero referencing this point
    
    Methods
    -------
    __init__(x, y, floor, no) -> None
        Creating a new point
    equals(other) -> bool
        Compare X, Y coordinates and the floor proeprties with another point
    """

    def __init__(self, x:float, y:float, floor:int, no:int) -> None:
        """Constructor for a new point
        
        Parameters
        ----------
        x : float
            The x coordinate
        y : float
            The y coordinate
        floor : int
            The floor index
        np : int
            The numero identifying the point
        """

        self.x = x
        self.y = y
        self.floorId = floor
        self.no = no
    

    def __str__(self) -> str:
        """Text which is printed by print() method"""
        return '({}, {})'.format(self.x, self.y)
    
    
    def equals(self, other) -> bool:
        """Compare X, Y coordinates and the floor proeprties with another point
        
        Parameters
        ----------
        other: Point
            The other instance of the same class with which we want to test the
            equality
        
        Returns
        -------
        bool
            True if the X and Y coordinates and the floor id are the same,
            false if not.
        """
        
        return (
            self.x == other.x and
            self.y == other.y and
            self.floorId == other.floorId)
    



