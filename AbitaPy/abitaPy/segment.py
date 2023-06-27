#!/usr/bin/python
# -*- coding: utf-8 -*-

from .point import Point
from .element import Element
from math import sqrt

class Segment:
    """Class representing a segment.

    Attributes
    ----------
    p1 : Point
        First point composing the segment
    p2 : Point
        Second point composing the segment
    e1 : Element
        An element using this segment as a border
    e2 : Element
        Another element using also this segment as a border
    floorId : int
        The floor where this segment is
    mark : boolean
        Whether this segment is marked or not
    length : float
        The length of the segment

    Methods
    -------
    __init__(p1:Point, p2:Point) -> None
        Create a segment using two points
    __str__() -> string
        Print a string describing the segment
    __eq__(other:Element) -> boolean
        Check if the segment is equal to another segment
    setElement(elt:Element) -> boolean
        Set a value to the Element attributes
    nextOf(elt:Element) -> None
        Returns the other element linked to the segment
    """


    def __init__(self, p1:Point, p2:Point) -> None:
        """Constructor of a segment
        
        Parameters
        ----------
        p1 : Point
            The first extremity of the segment
        p2 : Point
            The second extremity of the segment
        """

        self.p1 = p1
        self.p2 = p2
        self.floorId = p1.floorId
        self.mark = False
        self.length = sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
        self.e1 = None
        self.e2 = None

    
    def __str__(self) -> str:
        """Print the segment as a string of characters 

        Parameters
        ----------
        None

        Returns
        -------
        The string of characters that describes the segment
        """

        return '[{}, {}]'.format(self.p1, self.p2)
    

    def __eq__(self, other) -> bool:
        """Method checking if the considered segment is equal to another segment

        Parameters
        ----------
        other : Segment
            The other segment we want to compare our segment to 

        Returns
        -------
        A boolean indicated if the two segments have the same points as
        extremities. If "other" is not a Segment, returns NotImplemented
        """

        if isinstance(other, Segment):
            return (
                self.p1 == other.p1 and self.p2 == other.p2 or
                self.p1 == other.p2 and self.p2 == other.p1)
        else:
            return NotImplemented
    

    def setElement(self, elt: Element) -> bool:
        """Setter the e1 and e2 attributes to the proposed element
        
        Parameters
        ----------
        elt : Element
            The element we want to set the value of the attributes to
        
        Returns
        -------
        True if the element was added as an attribute or was already set as an
        attribute, else False.
        """

        if self.e1 is None:
            self.e1 = elt
            return True
        elif self.e2 is None:
            self.e2 = elt
            return True
        else :
            return self.e1 is elt or self.e2 is elt


    def nextOf(self, elt:Element) -> Element:
        """Return the other element linked to the segment
        
        Parameters
        ----------
        elt : Element
            The element which shloud be linked to the segment
        
        Returns
        -------
        elt : Element
            The other element linked to the segment
        """

        if self.e1 is elt:
            return self.e2
        elif self.e2 is elt:
            return self.e1
        else:
            return None
    

