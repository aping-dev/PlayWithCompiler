#include "SimpleLexer.h"

int main()
{
    SimpleLexer *lexer = new SimpleLexer;

    string script = "int age = 45;";
    cout << "parse: " << script << endl;
    SimpleTokenReader *tokenReader = lexer->tokenize(script);
    lexer->dump(tokenReader);

    //测试inta的解析
    script = "inta age = 45;";
    cout << "\nparse: " << script << endl;
    tokenReader = lexer->tokenize(script);
    lexer->dump(tokenReader);

    //测试in的解析
    script = "in age = 45;";
    cout << "\nparse: " << script << endl;
    tokenReader = lexer->tokenize(script);
    lexer->dump(tokenReader);

    //测试>=的解析
    script = "age >= 45;";
    cout << "\nparse: " << script << endl;
    tokenReader = lexer->tokenize(script);
    lexer->dump(tokenReader);

    //测试>的解析
    script = "age > 45;";
    cout << "\nparse: " << script << endl;
    tokenReader = lexer->tokenize(script);
    lexer->dump(tokenReader);

    delete lexer;
    delete tokenReader;
    return 0;
}

/**
 * 有限状态机进入初始状态。
 * 这个初始状态其实并不做停留，它马上进入其他状态。
 * 开始解析的时候，进入初始状态；某个Token解析完毕，也进入初始状态，在这里把Token记下来，然后建立一个新的Token。
 * @param ch
 * @return
 */
DfaState SimpleLexer::initToken(char ch) 
{
    if (tokenText.size() > 0) {
        token->text = vectorToString(tokenText);
        tokens.push_back(token);
        //cout << "53: token->text: " << token->text << endl;

        tokenText.clear();
        token = new SimpleToken();
    }

    DfaState newState = DfaState::Initial;
    if (isAlpha(ch)) // 第一个字符是字母
    {              
        if (ch == 'i') 
        {
            newState = DfaState::Id_int1;
        } else 
        {
            newState = DfaState::Id; // 进入Id状态
        }
        token->type = TokenType::Identifier;
        tokenText.push_back(ch);
    } 
    else if (isDigit(ch))  // 第一个字符是数字
    {       
        newState = DfaState::IntLiteral;
        token->type = TokenType::IntLiteral;
        tokenText.push_back(ch);
    } 
    else if (ch == '>') // 第一个字符是>
    {         
        newState = DfaState::GT;
        token->type = TokenType::GT;
        tokenText.push_back(ch);
    } 
    else if (ch == '+') 
    {
        newState = DfaState::Plus;
        token->type = TokenType::Plus;
        tokenText.push_back(ch);
    } 
    else if (ch == '-') 
    {
        newState = DfaState::Minus;
        token->type = TokenType::Minus;
        tokenText.push_back(ch);
    } 
    else if (ch == '*') 
    {
        newState = DfaState::Star;
        token->type = TokenType::Star;
        tokenText.push_back(ch);
    } 
    else if (ch == '/') 
    {
        newState = DfaState::Slash;
        token->type = TokenType::Slash;
        tokenText.push_back(ch);
    } 
    else if (ch == ';') 
    {
        newState = DfaState::SemiColon;
        token->type = TokenType::SemiColon;
        tokenText.push_back(ch);
    } 
    else if (ch == '(') 
    {
        newState = DfaState::LeftParen;
        token->type = TokenType::LeftParen;
        tokenText.push_back(ch);
    } 
    else if (ch == ')') 
    {
        newState = DfaState::RightParen;
        token->type = TokenType::RightParen;
        tokenText.push_back(ch);
    } 
    else if (ch == '=') 
    {
        newState = DfaState::Assignment;
        token->type = TokenType::Assignment;
        tokenText.push_back(ch);
    } 
    else 
    {
        newState = DfaState::Initial; // skip all unknown patterns
    }
    return newState;
}

/**
 * 解析字符串，形成Token。
 * 这是一个有限状态自动机，在不同的状态中迁移。
 * @param code
 * @return
 */
SimpleTokenReader* SimpleLexer::tokenize(string code) 
{
    tokens.clear();
    tokenText.clear();
    token = new SimpleToken;
    int ich = 0;
    char ch = 0;
    DfaState state = DfaState::Initial;

    while (ich < code.size()) 
    {
        ch = (char) code[ich];
        switch (state) 
        {
        case DfaState::Initial:
            state = initToken(ch);          //重新确定后续状态
            break;
        case DfaState::Id:
            if (isAlpha(ch) || isDigit(ch)) 
            {
                tokenText.push_back(ch);       //保持标识符状态
            } 
            else 
            {
                state = initToken(ch);      //退出标识符状态，并保存Token
            }
            break;
        case DfaState::GT:
            if (ch == '=') 
            {
                token->type = TokenType::GE;  //转换成GE
                state = DfaState::GE;
                tokenText.push_back(ch);
            } 
            else 
            {
                state = initToken(ch);      //退出GT状态，并保存Token
            }
            break;
        case DfaState::GE:
        case DfaState::Assignment:
        case DfaState::Plus:
        case DfaState::Minus:
        case DfaState::Star:
        case DfaState::Slash:
        case DfaState::SemiColon:
        case DfaState::LeftParen:
        case DfaState::RightParen:
            state = initToken(ch);          //退出当前状态，并保存Token
            break;
        case DfaState::IntLiteral:
            if (isDigit(ch)) 
            {
                tokenText.push_back(ch);       //继续保持在数字字面量状态
            } 
            else 
            {
                state = initToken(ch);      //退出当前状态，并保存Token
            }
            break;
        case DfaState::Id_int1:
            if (ch == 'n') 
            {
                state = DfaState::Id_int2;
                tokenText.push_back(ch);
            }
            else if (isDigit(ch) || isAlpha(ch))
            {
                state = DfaState::Id;    //切换回Id状态
                tokenText.push_back(ch);
            }
            else 
            {
                state = initToken(ch);
            }
            break;
        case DfaState::Id_int2:
            if (ch == 't') 
            {
                state = DfaState::Id_int3;
                tokenText.push_back(ch);
            }
            else if (isDigit(ch) || isAlpha(ch))
            {
                state = DfaState::Id;    //切换回id状态
                tokenText.push_back(ch);
            }
            else 
            {
                state = initToken(ch);
            }
            break;
        case DfaState::Id_int3:
            if (isBlank(ch)) 
            {
                token->type = TokenType::Int;
                state = initToken(ch);
            }
            else{
                state = DfaState::Id;    //切换回Id状态
                tokenText.push_back(ch);
            }
            break;
        default:
            break;
        }
        ich++;
    }
    // 把最后一个token送进去
    if (tokenText.size() > 0) 
    {
        initToken(ch);
    }

    return new SimpleTokenReader(tokens);
}