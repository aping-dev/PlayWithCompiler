#!/usr/bin/env python
# -*- coding: utf-8 -*-

from play_with_compiler.craft.simple_lexer import SimpleLexer
from play_with_compiler.craft.base_type import Token, TokenReader, ASTNodeType, TokenType
from play_with_compiler.craft.simple_calculator import SimpleASTNode

'''
 * 一个简单的语法解析器。
 * 能够解析简单的表达式、变量声明和初始化语句、赋值语句。
 * 它支持的语法规则为：
 *
 * programm -> int_declare | expressionStatement | assignmentStatement
 * int_declare -> 'int' Id ( = additive) ';'
 * expressionStatement -> addtive ';'
 * addtive -> multiplicative ( (+ | -) multiplicative)*
 * multiplicative -> primary ( (* | /) primary)*
 * primary -> IntLiteral | Id | (additive)
'''
class SimpleParser(object):
    '''
    解析脚本
    '''
    def parse(self, script):
        lexer = SimpleLexer()
        tokens = lexer.tokenize(script)
        root_node = self.prog(tokens)
        return root_node

    '''
    AST的根节点，解析的入口
    '''
    def prog(self, tokens):
        node = SimpleASTNode(ASTNodeType.Programm, 'pwc')
        while tokens.peek():
            child = self.int_declare(tokens)
            
            if not child:
                child = self.expression_statement(tokens)

            if not child:
                child = self.assignment_statement(tokens)

            if not child:
                node.add_child(child)

            if not child:
                raise Exception('unknown statement')

            node.add_child(child)
            
        return node

    '''
    表达式语句，即表达式后面跟个分号
    '''
    def expression_statement(self, tokens):
        pos = tokens.get_position()
        node = self.additive(tokens)
        if node:
            token = tokens.peek()
            if (token and token.get_type() == TokenType.SemiColon):
                tokens.read()
            else:
                node = None
                tokens.set_position(pos) # 回溯
        return node
    
    '''
    赋值语句，如age = 10*2;
    '''
    def assignment_statement(self, tokens):
        node = None
        token = tokens.peek() # 预读，看看下面是不是标识符
        if (token != None and token.get_type() == TokenType.Identifier):
            token = tokens.read() # 读入标识符
            node = SimpleASTNode(ASTNodeType.AssignmentStmt, token.get_text())
            token = tokens.peek() # 预读，看下面是不是等号
            if (token != None and token.get_type() == TokenType.Assignment):
                tokens.read() # 取出等号
                child = self.additive(tokens)
                if (child == None): # 出错，等号右边不是一个合法的表达式
                    raise Exception('invalide assignment statement, expecting an expression')
                else:
                    node.add_child(child) # 添加子节点
                    token = tokens.peek() # 预读，看后面是不是分号
                    if (token != None and token.get_type() == TokenType.SemiColon):
                        tokens.read()  # 消耗掉该分号
                    else:
                        raise Exception('invalid statement, expecting semicolon')
            else: # 回溯，吐出之前消化掉的标识符
                tokens.unread()
                node = None
        return node

    '''
     * 整型变量声明，如：
     * int a;
     * int b = 2*3;
    '''
    def int_declare(self, tokens):
        node = None
        token = tokens.peek()
        if (token and token.get_type() == TokenType.Int):
            token = tokens.read()
            if (tokens.peek().get_type() == TokenType.Identifier):
                token = tokens.read()
                node = SimpleASTNode(ASTNodeType.IntDeclaration, token.get_text())
                token = tokens.peek()
                if (token and token.get_type() == TokenType.Assignment):
                    tokens.read()  # 取出等号
                    child = self.additive(tokens)
                    if (not child):
                        raise Exception('invlide variable initialization, expecting an expression')
                    else:
                        node.add_child(child)
            else:
                raise Exception('variable name expected')

            if node:
                token = tokens.peek()
                if (token and token.get_type() == TokenType.SemiColon):
                    tokens.read()
                else:
                    raise Exception('invalid statemennt, expecting semicolon')
        return node
    
    '''
    加法表达式
    '''
    def additive(self, tokens):
        child1 = self.multiplicative(tokens) # 应用 add 规则
        node = child1
        if child1:
            while True:  # 循环应用 add' 规则
                token = tokens.peek()
                if (token and (token.get_type() == TokenType.Plus or token.get_type() == TokenType.Minus)):
                    token = tokens.read() # 读出加号
                    child2 = self.multiplicative(tokens) # 计算下级节点
                    if child2:
                        node = SimpleASTNode(ASTNodeType.Additive, token.get_text())
                        node.add_child(child1)
                        node.add_child(child2)
                        child1 = node
                    else:
                        raise Exception('invlide additive expression, expecting the right part.')
                else:
                    break
        return node

    '''
    乘法表达式
    '''
    def multiplicative(self, tokens):
        child1 = self.primary(tokens)
        node = child1
        while True:
            token = tokens.peek()
            if (token != None and (token.get_type() == TokenType.Star or token.get_type() == TokenType.Slash)):
                token = tokens.read()
                child2 = self.primary(tokens)
                if (child2 != None):
                    node = SimpleASTNode(ASTNodeType.Multiplicative, token.get_text())
                    node.add_child(child1)
                    node.add_child(child2)
                    child1 = node
                else:
                    raise Exception('invalid multiplicative expression, expecting the right part.')
            else:
                break
        return node

    '''
    基础表达式
    '''
    def primary(self, tokens):
        node = None
        token = tokens.peek()
        if token:
            if (token.get_type() == TokenType.IntLiteral):
                token = tokens.read()
                node = SimpleASTNode(ASTNodeType.IntLiteral, token.get_text())
            elif (token.get_type() == TokenType.Identifier):
                token = tokens.read()
                node = SimpleASTNode(ASTNodeType.Identifier, token.get_text())
            elif (token.get_type() == TokenType.LeftParen):
                tokens.read()
                node = self.additive(tokens)
                if node:
                    token = tokens.peek()
                    if (token and token.get_type() == TokenType.RightParen):
                        tokens.read()
                    else:
                        raise Exception('expecting right parenthesis')
                else:
                    raise Exception('expecting an additive expression inside parenthesis')
        return node # 这个方法也做了AST的简化，就是不用构造一个primary节点，直接返回子节点。因为它只有一个子节点

    '''
    * 打印输出AST的树状结构
    * @param node
    * @param indent 缩进字符，由tab组成，每一级多一个tab
    '''
    def dump_AST(self, node, indent):
        if not node:
            return
        print("%s%s %s" %(indent, node.node_type, node.text))
        for child in node.get_children():
            self.dump_AST(child, indent + "\t")

    




    