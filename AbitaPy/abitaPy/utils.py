#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Any

def get_by_attr(list:List[Any], attr:str, value:Any, unique=True) -> Any:
    """Get an element in a list by one of his attributes.
    
    Parameters
    ----------
    list : List[Any]
        The list in which we search the element
    attr : str
        The name of the attribute we look up
    value : Any
        The value of the attribute we want for the item
    unique : bool, optional
        If True, check if the item we search in the list is unique, 
        else returns the last element (default is True)
    
    Returns
    -------
    res : Any
        The item in the list we searched for
    """

    found = False
    res = None
    for item in list:
        attr_val = getattr(item, attr)
        if attr_val == value:
            if found and unique:
                raise TooManyFoundException(attr, value)
            found = True
            res = item
    if not found:
        raise NotFoundException(attr, value)
    return res


def exists_by_attr(list:List[Any], attr:str, value:Any) -> bool:
    """Check if an element with a certain value on an attribute
    exists in the list.

    Parameters
    ----------
    list : List[Any]
        The list in which we search the element
    attr : str
        The name of the attribute we look up
    value : Any
        The value of the attribute we want for the item
    
    Returns
    -------
    exists : bool
        True if the item exists, else False
    """
    try:
        _ = get_by_attr(list, attr, value, False)
        return True
    except NotFoundException:
        return False


class TooManyFoundException(Exception):
    """Too many items found in a list

    Exception raised when there is too many items found
    corresponding to search parameters in a list.
    
    Attributes
    ----------
    attr : str
        The attribute we look up for
    val : any
        The value of the attribute asked
    """

    def __init__(self, attr:str, val:Any) -> None:
        self.attr = attr
        self.val = val

    def __str__(self) -> str:
        return 'Found more than one item with value \
                {} for attribute {}'.format(self.val, self.attr)


class NotFoundException(Exception):
    """Not Found Exception

    Exception raised when we did not found an
    item in a list.
    
    Attributes
    ----------
    attr : str
        The attribute we look up for
    val : any
        The value of the attribute asked
    """

    def __init__(self, attr:str, val:Any) -> None:
        self.attr = attr
        self.val = val

    def __str__(self) -> str:
        return 'There is no item with value {} for attribute \
                {} in the list.'.format(self.val, self.attr)

