#!/usr/bin/env python
# -*- coding: utf-8 -*-
from play_with_compiler.craft.simple_lexer import SimpleLexer
from play_with_compiler.craft.simple_calculator import SimpleCalculator

def test_simple_Lexer():
    lexer = SimpleLexer()

    script = "int age = 45;"
    print("parse: {}".format(script))
    tokenReader = lexer.tokenize(script)
    lexer.dump(tokenReader)

    # 测试inta的解析
    script = "inta age = 45;"
    print("\nparse: {}".format(script))
    tokenReader = lexer.tokenize(script)
    lexer.dump(tokenReader)

    # 测试in的解析
    script = "in age = 45;"
    print("\nparse: {}".format(script))
    tokenReader = lexer.tokenize(script)
    lexer.dump(tokenReader)

    # 测试>=的解析
    script = "age >= 45;"
    print("\nparse: {}".format(script))
    tokenReader = lexer.tokenize(script)
    lexer.dump(tokenReader)

    # 测试>的解析
    script = "age > 45;"
    print("\nparse: {}".format(script))
    tokenReader = lexer.tokenize(script)
    lexer.dump(tokenReader)

def test_simple_calculator():
    calculator = SimpleCalculator()

    # 测试变量声明语句的解析
    script = "int a = b+3;"
    print("解析变量声明语句: {}".format(script))
    lexer = SimpleLexer()
    tokens = lexer.tokenize(script)
    try:
        node = calculator.intDeclare(tokens)
        calculator.dump_ast(node, "")
    except Exception as e:
        print(e)

    # 测试表达式
    script = "2+3*5"
    print("\n计算: {}，看上去一切正常。".format(script))
    calculator.evaluate(script)

    # 测试语法错误
    script = "2+"
    print("\n{} ，应该有语法错误。".format(script))
    calculator.evaluate(script)

    script = "2+3+4"
    print("\n计算: {}".format(script))
    calculator.evaluate(script)

    script = "2*3*4"
    print("\n计算: {}".format(script))
    calculator.evaluate(script)

if __name__ == '__main__':
    #test_simple_lexer()
    test_simple_calculator()