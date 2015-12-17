# -*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.DEBUG)

import ply.lex as lex
import ply.yacc as yacc

from booltree import And, Or, Not, Token


class ExprParser(object):
    tokens = ('NAME', 'LPAREN', 'RPAREN',  'NOT', 'AND', 'OR')

    t_NOT = r'not'
    t_AND = r'and'
    t_OR = r'or'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NAME = r'(?!and)(?!or)(?!not)[\w]+'

    t_ignore = " \t"

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
    )

    def __init__(self):
        lex.lex(module=self, debug=0)
        yacc.yacc(module=self, debug=0, write_tables=0)

    def __call__(self, expr):
        return yacc.parse(expr)

    def t_error(self, t):
        logging.error('Illegal character "{}"'.format(t.value[0]))
        t.lexer.skip(1)

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_name(self, p):
        """expression : NAME"""
        p[0] = Token(p[1])

    def p_expression_or(self, p):
        """expression : expression OR expression"""
        p[0] = Or(p[1], p[3])

    def p_expression_and(self, p):
        """expression : expression AND expression"""
        p[0] = And(p[1], p[3])

    def p_expression_not(self, p):
        """expression : NOT expression"""
        p[0] = Not(p[2])

    def p_error(self, p):
        if p:
            logging.error('Syntax error at "{}"'.format(p.value))
        else:
            logging.error('Syntax error at EOF')
