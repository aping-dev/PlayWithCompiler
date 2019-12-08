#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

'''
Token的类型
'''
class TokenType(Enum):
    Plus = 0   # +
    Minus = 1  # -
    Star = 2   # *
    Slash = 3  # /

    GE = 4  # >=
    GT = 5  # >
    EQ = 6  # ==
    LE = 7  # <=
    LT = 8  # <

    SemiColon = 9  # ;
    LeftParen = 10  # (
    RightParen = 11 # )

    Assignment = 12 # =

    If = 13
    Else = 14
    
    Int = 15

    Identifier = 16     # 标识符

    IntLiteral = 17     # 整型字面量
    StringLiteral = 18  # 字符串字面量


'''
一个简单的Token。
只有类型和文本值两个属性。
'''
class Token(object):
    def getType(self):  # Token的类型
        pass
    def getText(self):     # Token的文本值
        pass

'''
AST节点的类型。
'''
class ASTNodeType(Enum):
    Programm = 0          # 程序入口，根节点

    IntDeclaration = 1    # 整型变量声明
    ExpressionStmt = 2    # 表达式语句，即表达式后面跟个分号
    AssignmentStmt = 3    # 赋值语句

    Primary = 4           # 基础表达式
    Multiplicative = 5    # 乘法表达式
    Additive = 6          # 加法表达式

    Identifier = 7        # 标识符
    IntLiteral = 8        # 整型字面量

'''
AST的节点。
属性包括AST的类型、文本值、下级子节点和父节点
'''
class ASTNode(object):
    def getParent(self):    # 父节点
        pass
    def getChildren(self):  # 子节点
        pass
    def getType(self):      # AST类型
        pass
    def getText(self):      # 文本值
        pass

'''
一个Token流。由Lexer生成。Parser可以从中获取Token。
'''
class TokenReader(object):
    '''
    返回Token流中下一个Token，并从流中取出。 如果流已经为空，返回null;
    '''
    def read(self):
        pass

    '''
    返回Token流中下一个Token，但不从流中取出。 如果流已经为空，返回null;
    '''
    def peek(self):
        pass

    '''
    Token流回退一步。恢复原来的Token。
    '''
    def unread(self):
        pass

    '''
    获取Token流当前的读取位置。
    '''
    def getPosition(self):
        pass

    '''
    设置Token流当前的读取位置
    '''
    def setPosition(self, position):
        pass