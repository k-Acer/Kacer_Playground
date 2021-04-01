import math

class TokenManager:
    """manage token"""
    tokenIndex = 0
    def __init__(self, tokens):
        self.tokens = tokens
    def currentToken(self):
        """manage current token"""
        return self.tokens[self.tokenIndex]
    def next(self):
        """move to next token"""
        self.tokenIndex += 1
    def unFinish(self):
        """manage end or not"""
        return bool(self.tokenIndex < len(self.tokens))

class Calculator:
    """電卓"""
    def calc(self, formula: str) -> str:
        """計算全体"""
        print("formula")
        print(formula)
        tokens = self.lexer(formula)
        print("tokens")
        print(tokens)
        ast = self.parser(tokens)
        print("ast")
        print(ast)
        return self.calculate(ast)

    def lexer(self, formula: str) -> list:
        """字句解析"""
        if len(formula) == 0:
            raise RuntimeError("空文字列")
        else:
            token = []
            numberElements = []
            for char in formula:
                if char in [str(i) for i in range(0, 10)]:
                    numberElements.insert(0, int(char))
                elif char in ['+', '-', '*', '/', '^', '(', ')', 'e']:
                    if len(numberElements) != 0:
                        self.makeNumber(numberElements, token)
                    token.append(char)
                else:
                    raise RuntimeError("数値、演算子、括弧以外の入力")

            if len(numberElements) != 0:
                self.makeNumber(numberElements, token)

            return token

    def makeNumber(self, numberElements: list, token: list):
        """数値の処理"""
        number = 0
        for i in range(len(numberElements)):
            number = number + (numberElements[i] * (10**i))
        token.append(number)
        numberElements.clear()

    """
    BNF
    <expl> ::= <term> ( '+'<term> | '-'<term> )* 
    <term> ::= <expo> ( '*'<expo> | '/'<expo> )* 
    <expo> ::= <fact> ( '^'<fact>)*
    <fact> ::= '+'('('<expl>')' | 数値 |'e') | '-'('('<expl>')' | 数値 | 'e')  | '('<expl>')' | 数値 | 'e
    """

    def parser(self, tokens: list):
        """構文解析"""
        tokenManager = TokenManager(tokens)
        value = self.expl(tokenManager)
        if tokenManager.unFinish():
            raise RuntimeError("末尾が不正")
        else:
            return value

    def expl(self, tokenManager):
        left = self.term(tokenManager)
        while tokenManager.unFinish() and tokenManager.currentToken() in ["+", "-"]:
            inputOperator = "+"
            if (tokenManager.currentToken() == "-"):
                inputOperator = "-"
            tokenManager.next()
            right = self.term(tokenManager)  
            left = [inputOperator, left, right]
        return left
       
    def term(self, tokenManager):
        left = self.expo(tokenManager)
        while tokenManager.unFinish() and tokenManager.currentToken() in ["*", "/"]:
            inputOperator = "*"
            if (tokenManager.currentToken() == "/"):
                inputOperator = "/"
            tokenManager.next()
            right = self.expo(tokenManager)  
            left = [inputOperator, left, right]
        return left

    def expo(self,tokenManager):
        left = self.fact(tokenManager)
        while tokenManager.unFinish() and tokenManager.currentToken() == "^":
            inputOperator = "^"
            tokenManager.next()
            right = self.fact(tokenManager)  
            left = [inputOperator, left, right]
        return left

    def fact(self,tokenManager):
        # 単項演算子(+)
        if tokenManager.currentToken() == "+":
            tokenManager.next()
            if tokenManager.currentToken() == "(":
                tokenManager.next()
                value = self.expl(tokenManager)
                if tokenManager.unFinish() and tokenManager.currentToken() == ")":
                    tokenManager.next()
                    return value
                else:
                    raise RuntimeError("括弧が閉じていません")
            elif tokenManager.currentToken() in [i for i in range(0,10)]:
                value = tokenManager.currentToken()
                tokenManager.next()
                return value
            elif tokenManager.currentToken() == 'e':
                tokenManager.next()
                return math.e
            else:
                raise RuntimeError("単項演算子（プラス）の次に不正な入力")
        # 単項演算子(-)
        elif tokenManager.currentToken() == "-":
            tokenManager.next()
            if tokenManager.currentToken() == "(":
                tokenManager.next()
                value = self.expl(tokenManager)
                if tokenManager.currentToken() == ")":
                    tokenManager.next()    
                    return ["*", -1, value]
                else:
                    raise RuntimeError("括弧が閉じていません")
            elif tokenManager.currentToken() in [i for i in range(0, 10)]:
                value = tokenManager.currentToken()
                tokenManager.next()
                return value * -1
            elif tokenManager.currentToken() == 'e':
                tokenManager.next()
                return math.e * -1
            else:
                raise RuntimeError("単項演算子（マイナス）の次に不正な入力")
        # 括弧
        elif tokenManager.currentToken() == "(":
            tokenManager.next()
            value = self.expl(tokenManager)
            if tokenManager.currentToken() == ")":
                tokenManager.next()
                return value
            else:
                raise RuntimeError("括弧が閉じていません")
        # 数値
        elif type(tokenManager.currentToken()) == int:
            value = tokenManager.currentToken()
            tokenManager.next()
            return value
        elif tokenManager.currentToken() == 'e':
            tokenManager.next()
            return math.e
        # 例外処理
        else:
            raise RuntimeError("括弧の中が空文字列")

    def calculate(self,ast):
        """計算"""
        if type(ast) == int or type(ast) == float:
            return ast
        elif ast[0] == "+":
            add = self.calculate(ast[1]) + self.calculate(ast[2])
            return add
        elif ast[0] == "-":
            sub = self.calculate(ast[1]) - self.calculate(ast[2])
            return sub
        elif ast[0] == "*":
            mal = self.calculate(ast[1]) * self.calculate(ast[2])
            return mal
        elif ast[0] == "/":
            div = self.calculate(ast[1]) / self.calculate(ast[2])
            return div
        else:
            exp = self.calculate(ast[1]) ** self.calculate(ast[2])
            return exp


if __name__ == "__main__":
    calculator = Calculator()
    answer = calculator.calc("e+1*2")
    print("answer = {}".format(answer))

