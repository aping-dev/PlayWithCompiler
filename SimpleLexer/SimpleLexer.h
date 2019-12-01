#ifndef _SimpleLexer_H_INCLUDED_
#define _SimpleLexer_H_INCLUDED_
#include <iostream>
#include "craft.h"

/**
 * Token的一个简单实现。只有类型和文本值两个属性。
 */
class SimpleToken: public Token
{
public:
    //Token类型
    TokenType type;

    //文本值
    string text;

public:
    TokenType getType() 
    {
        return type;
    }

    string getText() 
    {
        return text;
    }
};

/**
 * 一个简单的Token流。是把一个Token列表进行了封装。
 */
class SimpleTokenReader: public TokenReader 
{
public:
    vector<Token*> tokens;
    int pos = 0;

    SimpleTokenReader(vector<Token*> &tokens1) 
    {
        tokens = tokens1;
    }

    Token* read() 
    {
        if (pos < tokens.size()) 
        {
            return tokens[pos++];
        }
        return NULL;
    }

    Token* peek() 
    {
        if (pos < tokens.size()) 
        {
            return tokens[pos];
        }
        return NULL;
    }

    void unread() 
    {
        if (pos > 0) 
        {
            pos--;
        }
    }

    int getPosition() 
    {
        return pos;
    }

    void setPosition(int position) 
    {
        if (position >=0 && position < tokens.size())
        {
            pos = position;
        }
    }
};

/**
 * 有限状态机的各种状态。
*/
enum class DfaState 
{
    Initial,

    If, Id_if1, Id_if2, Else, Id_else1, Id_else2, Id_else3, Id_else4, Int, Id_int1, Id_int2, Id_int3, Id, GT, GE,

    Assignment,

    Plus, Minus, Star, Slash,

    SemiColon,
    LeftParen,
    RightParen,

    IntLiteral
};

/**
 * 一个简单的手写的词法分析器。
 * 能够为后面的简单计算器、简单脚本语言产生Token。
 */
class SimpleLexer 
{
public:
    vector<char> tokenText;  //临时保存token的文本
    vector<Token*> tokens;   //保存解析出来的Token
    SimpleToken *token = new SimpleToken;   //当前正在解析的Token

    ~SimpleLexer()
    {
        tokenText.clear();

        for(int i=0; i<tokens.size(); i++)
        {
            delete tokens[i];
        }
        tokens.clear();

        delete token;
    }

    string vectorToString(vector<char> &v)
    {
        string result;
        result.insert(result.begin(), v.begin(), v.end());
        return result;
    }

    //是否是字母
    bool isAlpha(int ch) 
    {
        return ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'));
    }

    //是否是数字
    bool isDigit(int ch) 
    {
        return (ch >= '0' && ch <= '9');
    }

    //是否是空白字符
    bool isBlank(int ch) 
    {
        return ch == ' ' || ch == '\t' || ch == '\n';
    }

    static void dump(SimpleTokenReader *tokenReader)
    {
        cout << "text\t\ttype" << endl;
        Token *token = NULL;
        //cout << "size: " << tokenReader->tokens.size() << endl;
        while (token = tokenReader->read())
        {
            cout << token->getText() << "\t\t" << token->getType() << endl;
        }
    }

    DfaState initToken(char ch);
    SimpleTokenReader* tokenize(string code);
};

#endif /* _SimpleLexer_H_INCLUDED_ */