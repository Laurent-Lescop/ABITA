#!/usr/bin/python
# -*- coding: utf-8 -*-

from .algo import Algo
from .geom import Geom
from .population import Population
from .utils import exists_by_attr, get_by_attr

import ply.lex as lex
import ply.yacc as yacc


class AbiFile:
    """A class to manage reading and writing in files.
    
    Attributes
    ----------
    _fileName : str
        The name of the file we want to read or write in
    
    Methods
    -------
    __init__(fileName: str) -> None
        Create an AbiFile instance with its file name
    write(geom: Geom, popu: Population, algo: Algo) -> None
        Write and save current data in a .abi file
    read(geom: Geom, popu: Population, algo: Algo) -> None
        Read a .abi file and import data in the program
    """

    def __init__(self, fileName:str) -> None:
        """Constructor for the AbiFile class.
        
        Parameters
        ----------
        fileName : str
            The name of the file we want to read or write in.
        """
        self._fileName = fileName
    
    
    def write(self, geom: Geom, popu: Population, algo: Algo) -> None:
        """Write the results of the computation in the (filename).abi file.
        
        Parameters
        ----------
        geom : Geom
            The geometry of the problem (point, segments, etc...)
        popu : Population
            The computed solutions (lot, solutions...)
        algo : Algo
            The parameters of the problem
        
        Returns
        -------
        None
        """

        # open the file
        f = open(self._fileName, 'w')

        # algorithm parameter
        # -------------------

        # solver's parameters
        f.write("A1\t{:d}\n".format(algo.initIT))
        f.write("A2\t{:d}\n".format(algo.endIT))
        f.write("A3\t{:d}\n".format(algo.nbSols))
        f.write("A4\t{:.2f}\n".format(float(algo.alpha)))

        # types definition
        for type in algo.typeList:
            f.write("T{:d}\t{:.2f}\t{:.2f}\t{:.2f}\t{:d}\t{:d}\n".format(
                type.no,
                float(type.benefit),
                float(type.areaMin),
                float(type.areaMax),
                type.nbMin,
                type.nbMax
            ))
        
        # write geometry
        # --------------

        for i in range(len(geom.floorList)):
            # floor no
            floor = geom.floorList[i]
            f.write("F{:d}\n".format(floor.no))
            # points coordinates
            for pt in geom.pointList:
                if pt.floorId == i:
                    f.write("P{:d}\t{:.2f}\t{:.2f}\n".format(
                        pt.no,
                        float(pt.x),
                        float(pt.y)
                    ))
            # elements definition
            for elt in floor.elementList:
                f.write("E{:d}\t{:d}".format(elt.no, elt.nbPoints-1))
                for p in elt.pointList[:-1]:
                    f.write("\t{:d}".format(p.no))
                f.write("\n")
            # list of common elements
            for elt in floor.elementList:
                if elt.common and not(elt.imposed):
                    f.write("C{:d}\n".format(elt.no))
            # list of imposed common elements
            for elt in floor.elementList:
                if elt.imposed and not(elt.exit):
                    f.write("I{:d}\n".format(elt.no))
            # list of exit imposed common elements
            for elt in floor.elementList:
                if elt.exit:
                    f.write("X{:d}\n".format(elt.no))
            # list of bonus
            for elt in floor.elementList:
                if elt.bonus != 0:
                    f.write("B{:d}\t{:.2f}\n".format(elt.no, float(elt.bonus)))
        
        # write solutions
        # ---------------

        for i in range(popu.nbSolutions):
            # solution no and fitness
            sol = popu.solutionList[i]
            f.write("S{:d}\t{:.2f}\n".format(i, float(sol.fitness)))
            # lots definition
            for j in range(sol.nbLots):
                lot = sol.lotList[j]
                f.write("L{:d}\t{:d}\t{:.2f}\t{:d}".format(
                    j,
                    lot.typeNo,
                    float(lot.fitness),
                    lot.nbElements
                ))
                for elt in sorted(lot.elementList, key=lambda e:e.no):
                    f.write("\t{:d}".format(elt.no))
                f.write("\n")

        # save file
        # ---------

        f.close()
    

    def read(self, geom: Geom, popu: Population, algo: Algo) -> None:
        """Read the (fileName).abi file and save the informations in variables 
        passed as parameters.

        Parameters
        ----------
        geom : Geom
            An empty geometry
        popu : Population
            An empty poulation
        algo : Algo
            An empty algorithm configuration
        
        Returns
        -------
        None
        """

        # read the file
        finput = open(self._fileName, 'r')
        program = finput.read()
        finput.close()

        # execute the parser
        parser = AbiParser(geom, popu, algo).parser
        parser.parse(program)

        # initialize geometry, population, and algorithm
        geom.build()
        for sol in popu.solutionList: 
            algo.evaluate(sol)
        popu.stats()




class AbiLexer:
    """Class for the lexical analyzer definition"""

    tokens = ('COMMENT', 'PARAMETER', 'DEF_ELEMENT', 'DEF_FLOOR', 'DEF_LOT', 
              'DEF_POINT', 'DEF_SOLUTION', 'DEF_TYPE', 'SET_BONUS', 
              'SET_AS_IMPOSED', 'SET_AS_COMMON','SET_AS_EXIT', 'NUMBER')

    # the commands
    t_PARAMETER = r'A'
    t_DEF_ELEMENT = r'E'
    t_DEF_FLOOR = r'F'
    t_DEF_LOT = r'L'
    t_DEF_POINT = r'P'
    t_DEF_SOLUTION = r'S'
    t_DEF_TYPE = r'T'
    t_SET_BONUS = r'B'
    t_SET_AS_IMPOSED = r'I'
    t_SET_AS_COMMON = r'C'
    t_SET_AS_EXIT = r'X'

    # the parameters
    def t_NUMBER(self, t):
        r'-?((\d*\.\d+)|(\d+\.\d*)|(\d+))'
        t.value = float(t.value)
        if t.value % 1 == 0:
            t.value = int(t.value)
        return t
    
    def t_COMMENT(self, t):
        r'\#.*'
        pass
    
    t_ignore = " \t"
    
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise Exception('Unexpected character at line {}: {}'.format(
            t.lexer.lineno,
            t.value[0]))
    
    def __init__(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)




class AbiParser:
    """Class for the grammatical analyser definition"""
    
    tokens = AbiLexer.tokens
    
    def __init__(self, geom: Geom, popu: Population, algo: Algo):
        """Initialize the parser for read AbiFiles. Datas will be save into 
        geom, popu and algo passed as arguments."""

        self.floorId = 0
        self.solId = -1
        self.geom = geom
        self.popu = popu
        self.algo = algo
        self.lexer = AbiLexer()
        self.parser = yacc.yacc(module=self)


    # axiom
    def p_expression(self, p):
        '''expression : cmd expression 
                      | cmd'''
    

    # define the parameters of the algorithm
    def p_cmd_param(self, p):
        '''cmd : PARAMETER id NUMBER'''
        parameter = p[2]
        if parameter == 1:
            self.algo.initIT = p[3]
        elif parameter == 2:
            self.algo.endIT = p[3]
        elif parameter == 3:
            self.algo.nbSols = p[3]
        elif parameter == 4:
            self.algo.alpha = p[3]
        else:
            raise Exception('Error at line {}: Parameter A{} does not exist'.format(
                p.lineno(1),
                parameter))
    

    # define the declaration of objects

    def p_cmd_def_elt(self, p):
        '''cmd : DEF_ELEMENT id nb p_list'''
        no, nb_points, p_list = p[2:]
        # check if number of points is correct
        if nb_points != len(p_list):
            raise Exception('Error at line {}: Element {} has wrong number of points.'.format(
                p.lineno(1),
                no))
        # check if element already exists
        if exists_by_attr(self.geom.elementList, 'no', no):
            raise Exception('Error at line {}: Element {} is already defined!'.format(
                p.lineno(1),
                no))
        # create the element and save it
        from .element import Element
        elt = Element(self.floorId, no)
        for p in p_list:
            elt.addPoint(p)
        self.geom.addElement(elt)
    
    def p_point_list(self, p):
        '''p_list : id p_list 
                  | id'''
        pt = get_by_attr(self.geom.pointList, 'no', p[1])
        p[0] = [pt]
        if len(p) > 2:
            p[0] += p[2]
    
    def p_cmd_def_floor(self, p):
        '''cmd : DEF_FLOOR id'''
        from .floor import Floor
        floor = Floor(p[2])
        self.geom.addFloor(floor)
        self.floorId = self.geom.nbFloors - 1
    
    def p_cmd_def_lot(self, p):
        '''cmd : DEF_LOT id id NUMBER nb elt_list'''
        no, tx, valeur_lot, nb_elt, elt_list = p[2:]
        if nb_elt != len(elt_list):
            raise Exception('Error at line {}: Lot {} has wrong number of elements.'.format(
                p.lineno(1),
                no))
        for elt in elt_list:
            elt_id = self.geom.elementList.index(elt)
            self.popu.solutionList[self.solId].distribution[elt_id] = no
    
    def p_elt_list(self, p):
        '''elt_list : id elt_list 
                    | id'''
        elt = get_by_attr(self.geom.elementList, 'no', p[1])
        p[0] = [elt]
        if len(p) > 2:
            p[0] += p[2]
    
    def p_def_point(self, p):
        '''cmd : DEF_POINT id NUMBER NUMBER'''
        no, x, y = p[2:]
        if exists_by_attr(self.geom.pointList, 'no', no):
            raise Exception('Error at line {}: Point {} is already defined!'.format(
                p.lineno(1),
                no))
        from .point import Point
        p = Point(x, y, self.floorId, no)
        self.geom.addPoint(p)
    
    def p_def_solution(self, p):
        '''cmd : DEF_SOLUTION id NUMBER'''
        from .solution import Solution
        sol = Solution(self.geom)
        self.popu.addSolution(sol)
        sol.fitness = p[3]
        self.solId += 1
    
    # define a type of lot (T1, T2, T3, ...)
    def p_def_type(self, p):
        '''cmd : DEF_TYPE id NUMBER NUMBER NUMBER nb nb'''
        no, benefit, areaMin, areaMax, nbMin, nbMax = p[2:]
        # check if tye already exists
        if exists_by_attr(self.algo.typeList, 'no', no):
            raise Exception('Error at line {}: Type {} is already defined!'.format(
                p.lineno(1),
                no))
        # create the type
        from .tx import Tx
        t = Tx(benefit, areaMin, areaMax, nbMin, nbMax, no)
        self.algo.addType(t)
    

    # define the commands to modify the properties of an element

    def p_cmd_set_bonus(self, p):
        '''cmd : SET_BONUS id NUMBER'''
        no, val = p[2:]
        elt = get_by_attr(self.geom.elementList, 'no', no)
        elt.bonus = val
    
    def p_cmd_set_as_common(self, p):
        '''cmd : SET_AS_COMMON id'''
        no = p[2]
        elt = get_by_attr(self.geom.elementList, 'no', no)
        elt.common = True
    
    def p_cmd_set_as_imposed(self, p):
        '''cmd : SET_AS_IMPOSED id'''
        no = p[2]
        elt = get_by_attr(self.geom.elementList, 'no', no)
        elt.common = True
        elt.imposed = True
    
    def p_set_as_exit(self, p):
        '''cmd : SET_AS_EXIT id'''
        no = p[2]
        elt = get_by_attr(self.geom.elementList, 'no', no)
        elt.common = True
        elt.imposed = True
        elt.exit = True

    def p_id_nb_number(self, p):
        '''id : NUMBER
           nb : NUMBER'''
        if p[1] % 1 != 0 or p[1] < 0:
            raise Exception("Error at line {}: get {} instead of a natural number".format(
                p.lineno(1),
                p[1]))
        p[0] = abs(int(p[1]))
    
    # minimalist management syntax errors
    def p_error(self, p):
        if p:
            raise Exception("Syntax error: {}".format(p.value))
        else:
            raise Exception("Unexpected EndOfLine")