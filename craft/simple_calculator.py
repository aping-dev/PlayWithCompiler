#!/usr/bin/env python
# -*- coding: utf-8 -*-
from play_with_compiler.craft.base_type import ASTNode
from play_with_compiler.craft.base_type import Token, TokenReader, TokenType, ASTNodeType
from play_with_compiler.craft.simple_lexer import SimpleLexer

'''
一个简单的AST节点的实现。
属性包括：类型、文本值、父节点、子节点。
'''
class SimpleASTNode(ASTNode):
    def __init__(self, node_type, text):
        self.parent = None
        self.children = []
        self.node_type = node_type
        self.text = text

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

'''
实现一个计算器，但计算的结合性是有问题的。因为它使用了下面的语法规则：
additive -> multiplicative | multiplicative + additive
multiplicative -> primary | primary * multiplicative    
递归项在右边，会自然的对应右结合。我们真正需要的是左结合。
'''
class SimpleCalculator(object):
    '''
    执行脚本，并打印输出AST和求值过程。
    '''
    def evaluate(self, script):
        try:
            tree = self.parse(script)
            self.dump_ast(tree, "@")
            self._evaluate(tree, "|")
        except Exception as e:
            print(e)

    '''
    解析脚本，并返回根节点
    '''
    def parse(self, code):
        lexer = SimpleLexer()
        tokens = lexer.tokenize(code)
        rootNode = self.prog(tokens)
        return rootNode

    '''
    打印输出AST的树状结构
    '''
    def dump_ast(self, node, indent):
        if node == None:
            return
        print('{}{} {}'.format(indent, node.node_type, node.text))
        for item in node.children:
            self.dump_ast(item, indent + "\t")

    '''
    对某个AST节点求值，并打印求值过程。
    @param indent  打印输出时的缩进量
    '''
    def _evaluate(self, node, indent):
        print("{} Calculating: {}".format(indent, node.node_type))
        result = 0
        children = node.children
        value1 = 0
        value2 = 0
        child1 = None
        child2 = None

        if (node.node_type == ASTNodeType.Programm):
            for child in children:
                result = self._evaluate(child, indent + "\t")
        elif (node.node_type == ASTNodeType.Additive):
            child1 = children[0]
            value1 = self._evaluate(child1, indent + "\t")
            child2 = children[1]
            value2 = self._evaluate(child2, indent + "\t")
            if (node.text == "+"):
                result = int(value1) + int(value2)
            else:
                result = int(value1) - int(value2)
        elif (node.node_type == ASTNodeType.Multiplicative):
            child1 = children[0]
            value1 = self._evaluate(child1, indent + "\t")
            child2 = children[1]
            value2 = self._evaluate(child2, indent + "\t")
            if (node.text == "*"):
                result = int(value1) * int(value2)
            else:
                result = int(value1) / int(value2)
        elif (node.node_type == ASTNodeType.IntLiteral):
            result = node.text
        print("{} Result: {}".format(indent, result))
        return result

    '''
    语法解析：根节点
    '''
    def prog(self, tokens):
        node = SimpleASTNode(ASTNodeType.Programm, "Calculator")

        child = self.additive(tokens)

        if (child != None):
            node.addChild(child)
        return node

    '''
    整型变量声明语句，如：
    int a;
    int b = 2*3;
    '''
    def intDeclare(self, tokens):
        node = None
        token = tokens.peek()    # 预读
        if (token != None and token.token_type == TokenType.Int): # 匹配Int
            token = tokens.read()      # 消耗掉int
            if (tokens.peek().token_type == TokenType.Identifier): # 匹配标识符
                token = tokens.read()  # 消耗掉标识符
                # 创建当前节点，并把变量名记到AST节点的文本值中，这里新建一个变量子节点也是可以的
                node = SimpleASTNode(ASTNodeType.IntDeclaration, token.token_text)
                token = tokens.peek()  # 预读
                if (token != None and token.token_type == TokenType.Assignment):
                    tokens.read()      # 消耗掉等号
                    child = self.additive(tokens)  # 匹配一个表达式
                    if (child == None):
                        raise "invalide variable initialization, expecting an expression"
                    else:
                        node.addChild(child)
            else:
                raise "variable name expected"

            if (node != None):
                token = tokens.peek()
                if (token != None and token.token_type == TokenType.SemiColon):
                    tokens.read()
                else:
                    raise "invalid statement, expecting semicolon"
        return node

    '''
    语法解析：加法表达式
    '''
    def additive(self, tokens):
        child1 = self.multiplicative(tokens) # 应用add规则
        node = child1
        if (child1 != None):
            while True:  # 循环应用add'
                token = tokens.peek()
                if (token != None and (token.token_type == TokenType.Plus or token.token_type == TokenType.Minus)):
                    token = tokens.read() # 读出加号
                    child2 = self.multiplicative(tokens)  # 计算下级节点
                    node = SimpleASTNode(ASTNodeType.Additive, token.token_text)
                    node.addChild(child1)  # 注意，新节点在顶层，保证正确的结合性
                    node.addChild(child2)
                    child1 = node
                else:
                    break
        return node

    '''
    语法解析：乘法表达式
    '''
    def multiplicative(self, tokens):
        child1 = self.primary(tokens)
        node = child1
        if (child1 != None):
            while True:
                token = tokens.peek()
                if (token != None) and (token.token_type == TokenType.Star or token.token_type == TokenType.Slash):
                    token = tokens.read()
                    child2 = self.primary(tokens)
                    if (child2 != None):
                        node = SimpleASTNode(ASTNodeType.Multiplicative, token.token_text)
                        node.addChild(child1)
                        node.addChild(child2)
                        child1 = node
                    else:
                        raise "invalid additive expression, expecting the right part."
                else:
                    break
        return node

    '''
    语法解析：基础表达式
    '''
    def primary(self, tokens):
        node = None
        token = tokens.peek()
        if (token != None):
            if (token.token_type == TokenType.IntLiteral):
                token = tokens.read()
                node = SimpleASTNode(ASTNodeType.IntLiteral, token.token_text)
            elif (token.token_type == TokenType.Identifier): 
                token = tokens.read()
                node = SimpleASTNode(ASTNodeType.Identifier, token.token_text)
            elif (token.token_type == TokenType.LeftParen):
                tokens.read()
                node = self.additive(tokens)
                if (node != None):
                    token = tokens.peek()
                    if (token != None and token.token_type == TokenType.RightParen):
                        tokens.read()
                    else:
                        raise "expecting right parenthesis"
                else:
                    raise "expecting an additive expression inside parenthesis"
        return node  # 这个方法也做了AST的简化，就是不用构造一个primary节点，直接返回子节点。因为它只有一个子节点
