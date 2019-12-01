#ifndef _Craft_H_INCLUDED_
#define _Craft_H_INCLUDED_
#include <string>
#include <vector>
#include <queue>
using namespace std;

/**
 * Token的类型
 */
enum class TokenType
{
    Plus,   // +
    Minus,  // -
    Star,   // *
    Slash,  // /

    GE,     // >=
    GT,     // >
    EQ,     // ==
    LE,     // <=
    LT,     // <

    SemiColon, // ;
    LeftParen, // (
    RightParen,// )

    Assignment,// =

    If,
    Else,
    
    Int,

    Identifier,     // 标识符

    IntLiteral,     // 整型字面量
    StringLiteral   // 字符串字面量
};


std::ostream& operator << (std::ostream& os, TokenType t)
{
	switch (t) 
    {
		case TokenType::Plus: os << "Plus"; break;  // +
        case TokenType::Minus: os << "Minus"; break;  // -
        case TokenType::Star: os << "Star"; break;   // *
        case TokenType::Slash: os << "Slash"; break;  // /

        case TokenType::GE: os << "GE"; break;     // >=
        case TokenType::GT: os << "GT"; break;    // >
        case TokenType::EQ: os << "EQ"; break;     // ==
        case TokenType::LE: os << "LE"; break;     // <=
        case TokenType::LT: os << "LT"; break;     // <

        case TokenType::SemiColon: os << "SemiColon"; break; // ;
        case TokenType::LeftParen: os << "LeftParen"; break; // (
        case TokenType::RightParen: os << "RightParen"; break;// )

        case TokenType::Assignment: os << "Assignment"; break;// =

        case TokenType::If: os << "If"; break;
        case TokenType::Else: os << "Else"; break;
        
        case TokenType::Int: os << "Int"; break;

        case TokenType::Identifier: os << "Identifier"; break;     // 标识符

        case TokenType::IntLiteral: os << "IntLiteral"; break;    // 整型字面量
        case TokenType::StringLiteral: os << "StringLiteral"; break;  // 字符串字面量
        default: os.setstate(std::ios_base::failbit); break;
	}
 
	return os;
}

/**
 * 一个简单的Token。
 * 只有类型和文本值两个属性。
 */
class Token
{
public:
    virtual TokenType getType() = 0;  // Token的类型
    virtual string getText() = 0;     // Token的文本值
    virtual ~Token(){}
};

/**
 * AST节点的类型。
 */
enum class ASTNodeType
{
    Programm,           //程序入口，根节点

    IntDeclaration,     //整型变量声明
    ExpressionStmt,     //表达式语句，即表达式后面跟个分号
    AssignmentStmt,     //赋值语句

    Primary,            //基础表达式
    Multiplicative,     //乘法表达式
    Additive,           //加法表达式

    Identifier,         //标识符
    IntLiteral          //整型字面量
};

/**
 * AST的节点。
 * 属性包括AST的类型、文本值、下级子节点和父节点
 */
class ASTNode
{
public:
    virtual ASTNode* getParent() = 0;            // 父节点
    virtual vector<ASTNode*> getChildren() = 0;  // 子节点
    virtual ASTNodeType getType() = 0;           // AST类型
    virtual string getText() = 0;                // 文本值
};

/**
 * 一个Token流。由Lexer生成。Parser可以从中获取Token。
 */
class TokenReader
{
public:
    /**
     * 返回Token流中下一个Token，并从流中取出。 如果流已经为空，返回null;
     */
    virtual Token* read() = 0;

    /**
     * 返回Token流中下一个Token，但不从流中取出。 如果流已经为空，返回null;
     */
    virtual Token* peek() = 0;

    /**
     * Token流回退一步。恢复原来的Token。
     */
    virtual void unread() = 0;

    /**
     * 获取Token流当前的读取位置。
     */
    virtual int getPosition() = 0;

    /**
     * 设置Token流当前的读取位置
     */
    virtual void setPosition(int position) = 0;
};

#endif /* _Craft_H_INCLUDED_ */