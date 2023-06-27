#!/usr/bin/python
# -*- coding: utf-8 -*-

class Tx:
    """Class representing a Tx class, that is to say
    a Type for Lots. A type can be for exemple T1, T2,
    T3, etc... and describe the type of lot it is (how 
    many rooms, size of the appartment, ...)
    
    Attributes
    ----------
    benefit : float
        Value of 1m² habitable surface for this type
        (in relative unit with other types)
    areaMin : float
        Minimum area value possible for this type
    areaMax : float
        Maximum area value possible for this type
    nbMin : int
        Minimum quantity of lot with this type in one
        solution
    nbMax : int
        Maximum quantity of lot with this type ine one
        solution
    no : int
        The numero referencing this type
    nb : int
        *Unknown attribute, complete later* 
    """

    def __init__(
            self, 
            benefit = 0, 
            areaMin = 0, 
            areaMax = 0, 
            nbMin = 0, 
            nbMax = 1000, 
            no = 0) -> None:
        """Constructor of a Tx object.
        
        Parameters
        ----------
        benefit : float, optional
            Value of 1m² habitable surface for this type
            (in relative unit with other types), 
            default to 0
        areaMin : float, optional
            Minimum area value possible for this type,
            default to 0
        areaMax : float, optional
            Maximum area value possible for this type,
            default to 0
        nbMin : int, optional
            Minimum quantity of lot with this type in one
            solution, default to 0
        nbMax : int, optional
            Maximum quantity of lot with this type ine one
            solution, default to 1000
        no : int, optional
            The numero referencing this type,
            default to 0
        """
        self.benefit = benefit
        self.areaMin = areaMin
        self.areaMax = areaMax
        self.nbMin = nbMin
        self.nbMax = nbMax
        self.no = no
        self.nb = 0
    