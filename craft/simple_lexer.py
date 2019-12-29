#!/usr/bin/env python
# -*- coding: utf-8 -*-
from play_with_compiler.craft.base_type import Token, TokenReader, TokenType
from enum import Enum

'''
Token的一个简单实现。只有类型和文本值两个属性。
'''
class SimpleToken(Token):
    def __init__(self):
        self.token_type = None
        self.token_text = ''

    def get_type(self):  # Token的类型
        return self.token_type

    def get_text(self):     # Token的文本值
        return self.token_text

'''
一个简单的Token流。是把一个Token列表进行了封装。
'''
class SimpleTokenReader(TokenReader):
    def __init__(self, tokens): 
        self.tokens = tokens
        self.pos = 0

    def read(self):
        if (self.pos < len(self.tokens)):
            token = self.tokens[self.pos]
            self.pos = self.pos + 1
            return token
        return None

    def peek(self): 
        if (self.pos < len(self.tokens)): 
            return self.tokens[self.pos]
        return None

    def unread(self):
        if (self.pos > 0):
            self.pos = self.pos - 1

    def get_position(self):
        return self.pos

    def set_position(self, position):
        if (position >=0 and position < len(self.tokens)):
            self.pos = position

'''
有限状态机的各种状态。
'''
class DfaState(Enum):
    Initial = 0

    If = 1
    Id_if1 = 2
    Id_if2 = 3
    Else = 4
    Id_else1 = 5
    Id_else2 = 6
    Id_else3 = 7
    Id_else4 = 8
    Int = 9
    Id_int1 = 10
    Id_int2 = 11
    Id_int3 = 12
    Id = 13
    GT = 14
    GE = 15

    Assignment = 16

    Plus = 17
    Minus = 18
    Star = 19
    Slash = 20

    SemiColon = 21
    LeftParen = 22
    RightParen = 23

    IntLiteral = 24

'''
一个简单的手写的词法分析器。
能够为后面的简单计算器、简单脚本语言产生Token。
'''
class SimpleLexer(object):
    def __init__(self):
        self.token = SimpleToken() # 当前正在解析的Token
        self.tokens = [] # 保存解析出来的Token

    # 是否是字母
    def is_alpha(self, ch):
        return ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z'))

    # 是否是数字
    def is_digit(self, ch):
        return (ch >= '0' and ch <= '9')

    # 是否是空白字符
    def is_blank(self, ch):
        return ch == ' ' or ch == '\t' or ch == '\n'

    def dump(self, tokenReader):
        print('text\t\ttype')
        token = tokenReader.read()
        while (token != None):
            print('{}\t\t{}'.format(token.token_text, token.token_type))
            token = tokenReader.read()

    '''
    有限状态机进入初始状态。
    这个初始状态其实并不做停留，它马上进入其他状态。
    开始解析的时候，进入初始状态；某个Token解析完毕，也进入初始状态，在这里把Token记下来，然后建立一个新的Token。
    '''
    def init_token(self, ch):
        if (len(self.token.token_text) > 0):
            self.tokens.append(self.token)
            self.token = SimpleToken()

        new_state = DfaState.Initial
        if (self.is_alpha(ch)): # 第一个字符是字母      
            if (ch == 'i'):
                new_state = DfaState.Id_int1
            else: 
                new_state = DfaState.Id # 进入Id状态
            self.token.token_type = TokenType.Identifier
            self.token.token_text += ch
        elif (self.is_digit(ch)):  # 第一个字符是数字   
            new_state = DfaState.IntLiteral
            self.token.token_type = TokenType.IntLiteral
            self.token.token_text += ch
        elif (ch == '>'): # 第一个字符是>
            new_state = DfaState.GT
            self.token.token_type = TokenType.GT
            self.token.token_text += ch
        elif (ch == '+'):
            new_state = DfaState.Plus
            self.token.token_type = TokenType.Plus
            self.token.token_text += ch
        elif (ch == '-'):
            new_state = DfaState.Minus
            self.token.token_type = TokenType.Minus
            self.token.token_text += ch
        elif (ch == '*'):
            new_state = DfaState.Star
            self.token.token_type = TokenType.Star
            self.token.token_text += ch
        elif (ch == '/'):
            new_state = DfaState.Slash
            self.token.token_type = TokenType.Slash
            self.token.token_text += ch
        elif (ch == ';'):
            new_state = DfaState.SemiColon
            self.token.token_type = TokenType.SemiColon
            self.token.token_text += ch
        elif (ch == '('):
            new_state = DfaState.LeftParen
            self.token.token_type = TokenType.LeftParen
            self.token.token_text += ch
        elif (ch == ')'):
            new_state = DfaState.RightParen
            self.token.token_type = TokenType.RightParen
            self.token.token_text += ch
        elif (ch == '='):
            new_state = DfaState.Assignment
            self.token.token_type = TokenType.Assignment
            self.token.token_text += ch
        else:
            new_state = DfaState.Initial # skip all unknown patterns
        return new_state

    '''
    解析字符串，形成Token。
    这是一个有限状态自动机，在不同的状态中迁移。
    '''
    def tokenize(self, code):
        self.tokens = []
        self.token = SimpleToken()
        ich = 0
        ch = 0
        state = DfaState.Initial

        while (ich < len(code)):
            ch = code[ich]
            if (state == DfaState.Initial):
                state = self.init_token(ch)          # 重新确定后续状态
            elif (state == DfaState.Id):
                if (self.is_alpha(ch) or self.is_digit(ch)):
                    self.token.token_text += ch   # 保持标识符状态
                else:
                    state = self.init_token(ch)   # 退出标识符状态，并保存Token
            elif (state == DfaState.GT):
                if (ch == '='):
                    self.token.token_type = TokenType.GE  # 转换成GE
                    state = DfaState.GE
                    self.token.token_text += ch
                else:
                    state = self.init_token(ch)   # 退出GT状态，并保存Token
            elif (state in [DfaState.GE, DfaState.Assignment, DfaState.Plus, DfaState.Minus, DfaState.Star,  
                    DfaState.Slash, DfaState.SemiColon, DfaState.LeftParen, DfaState.RightParen]):
                state = self.init_token(ch)       # 退出当前状态，并保存Token
            elif (state == DfaState.IntLiteral):
                if (self.is_digit(ch)):
                    self.token.token_text += ch   # 继续保持在数字字面量状态
                else:
                    state = self.init_token(ch)   # 退出当前状态，并保存Token
            elif (state == DfaState.Id_int1):
                if (ch == 'n'):
                    state = DfaState.Id_int2
                    self.token.token_text += ch
                elif (self.is_digit(ch) or self.is_alpha(ch)):
                    state = DfaState.Id     # 切换回Id状态
                    self.token.token_text += ch
                else:
                    state = self.init_token(ch)
            elif (state == DfaState.Id_int2):
                if (ch == 't'):
                    state = DfaState.Id_int3
                    self.token.token_text += ch
                elif (self.is_digit(ch) or self.is_alpha(ch)):
                    state = DfaState.Id    # 切换回id状态
                    self.token.token_text += ch
                else:
                    state = self.init_token(ch)
            elif (state == DfaState.Id_int3):
                if (self.is_blank(ch)):
                    self.token.token_type = TokenType.Int
                    state = self.init_token(ch)
                else:
                    state = DfaState.Id    # 切换回Id状态
                    self.token.token_text += ch
            ich = ich + 1
        # 把最后一个token送进去
        if (len(self.token.token_text) > 0):
            self.init_token(ch)

        return SimpleTokenReader(self.tokens)