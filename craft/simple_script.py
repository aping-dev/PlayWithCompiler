#!/usr/bin/env python
# -*- coding: utf-8 -*-

from play_with_compiler.craft.simple_parser import SimpleParser
from play_with_compiler.craft.base_type import ASTNodeType
import sys

'''
 * 一个简单的脚本解释器。
 * 所支持的语法，请参见simple_parser.py
 *
 * 运行脚本：
 * 在命令行下，键入：python simple_script.py
 * 则进入一个REPL界面。你可以依次敲入命令。比如：
 * > 2+3;
 * > int age = 10;
 * > int b;
 * > b = 10*2;
 * > age = age + b;
 * > exit();  //退出REPL界面。
 *
 * 你还可以使用一个参数 -v，让每次执行脚本的时候，都输出AST和整个计算过程。
 '''
class SimpleScript(object):
    def __init__(self, verbose):
       self._variables = {}
       self._verbose = verbose

    '''
    遍历AST，计算值
    '''
    def evaluate(self, node, indent):
        result = None
        if self._verbose:
            print('%s Calcalationg: %s:' %(indent, node.get_type()))
        
        if node.get_type() == ASTNodeType.Programm:
            for child in node.get_children():
                result = self.evaluate(child, indent)
        elif node.get_type() == ASTNodeType.Additive:
            child1 = node.get_children()[0]
            value1 = self.evaluate(child1, indent + "\t")
            child2 = node.get_children()[1]
            value2 = self.evaluate(child2, indent + "\t")
            if node.get_text() == '+':
                result = int(value1) + int(value2)
            else:
                result = int(value1) - int(value2)
        elif node.get_type() == ASTNodeType.Multiplicative:
            child1 = node.get_children()[0]
            value1 = self.evaluate(child1, indent + "\t")
            child2 = node.get_children()[1]
            value2 = self.evaluate(child2, indent + "\t")
            if node.get_text() == '*':
                result = int(value1) * int(value2)
            else:
                result = int(value1) / int(value2)
        elif node.get_type() == ASTNodeType.IntLiteral:
            result = int(node.get_text())
        elif node.get_type() == ASTNodeType.Identifier:
            var_name = node.get_text()
            value = self._variables.get(var_name)
            if value != None:
                result = int(value)
            else:
                raise Exception('variavle ' + var_name + ' has not been set any value')
        elif node.get_type() == ASTNodeType.AssignmentStmt:
            var_name = node.get_text()
            if var_name not in self._variables.keys():
                raise Exception('unknown variable: ' + var_name)
            # 接着执行下面的代码
        elif node.get_type() == ASTNodeType.IntDeclaration:
            var_name = node.get_text()
            var_value = None
            if len(node.get_children()) > 0:
                child = node.get_children()[0]
                result = self.evaluate(child, indent + '\t')
                var_value = int(result)
            self._variables[var_name] = var_value
        
        if self._verbose:
            print('%sResult: %s' %(indent, result))
        elif indent == '':
            if node.get_type() == ASTNodeType.IntDeclaration or node.get_type() == ASTNodeType.AssignmentStmt:
                print('%s: %s' %(node.get_text(), result))
            elif node.get_type() != ASTNodeType.Programm:
                print(result)
        return result

'''
实现一个简单的 REPL
'''
def play(args):
    verbose = False
    if (len(args) > 0 and args[0] == '-v'):
        verbose = True
        print('verbose mode')
    print('Simple script language!')

    parser = SimpleParser()
    script = SimpleScript(verbose)
    script_text = ""

    while True:
        try:
            line = raw_input(">")
            if line == 'exit();':
                print("good bye!")
                break
            script_text += line + "\n"
            if line.endswith(";"):
                tree = parser.parse(script_text)
                if verbose:
                    parser.dump_AST(tree, "")
                script.evaluate(tree, "")
                script_text = ""
        except Exception as e:
            print('119: %s' %e)
            script_text = ''

play(sys.argv[1:])