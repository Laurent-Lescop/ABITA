#!/usr/bin/python
# -*- coding: utf-8 -*-

from .element import Element


class Floor:
    """
    Class representing a floor. 
    
    Attributes
    ----------
    no: int
        which nth floor of the construction this floor is
    elementList: list[Element]
        list of the element which compose this floor
    nbElements : int
        number of elements which compose this floor
        
    Methods
    -------
    __init__(no:int)-> None:
        Default constructor for a floor
    addElement(elt:Element)-> None:
        Adds an element to a floor
    """

    def __init__(self, no:int) -> None:
        """
        Constructor for a floor

        Parameters
        ----------
        no : int
            The numero of the floor
        """

        self.no = no
        self.elementList = []
        self.nbElements = 0
    

    def addElement(self, elt:Element) -> None:
        """
        Method to add an element to a floor

        Parameters
        ----------
        elt : Element
            The element to add to the floor

        Returns
        -------
        None
        """

        # check if the element is an element 
        if elt is None :
            raise Exception("AddElementError : null elt")
        # check if element is not already added
        for i in range(self.nbElements):
            if elt == self.elementList[i]:
                raise Exception("AddElementError : elt E{} already defined".format(elt.index))
        # add the element
        self.elementList.append(elt)
        self.nbElements += 1

        



   