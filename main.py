from sympy import sympify, symbols, Eq, solve
import matplotlib.pyplot as plt
import numpy as np
import sys

class SimpleInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program):
        lines = program.split('\n')
        for line in lines:
            self.execute_line(line)

    def execute_line(self, line):
        tokens = line.split()

        if tokens[0] == 'get':
            expression = input("Enter an expression: ")
            x, y = symbols('x y')
            expression = expression.replace(" ", "")
            beforeEqual = expression
            afterEqual = expression
            flag = True
            for i in range(len(expression)):
                if i != len(expression) - 1:
                    if expression[i].isalpha() and expression[i+1].isdigit():
                        beforeEqual = beforeEqual.replace(expression[i] + expression[i+1], expression[i] + '**' + expression[i+1])
                if i != len(expression) - 1:
                    if expression[i].isdigit() and expression[i+1].isalpha():
                        beforeEqual = beforeEqual.replace(expression[i] + expression[i+1], expression[i] + '*' + expression[i+1])
                if i != len(expression) - 1:
                    if expression[i].isalpha() and expression[i+1] == '*' and expression[i+2].isdigit():
                        beforeEqual = beforeEqual.replace(expression[i] + expression[i+1], expression[i] + '*' + expression[i+1])
                if i != len(expression) - 1:
                    if (expression[i].isalpha() and expression[i+1].isalpha()) or (expression[i].isalpha() and expression[i+1] == '*' and expression[i+2].isalpha()) or (expression[i] == '*' and expression[i+1].isdigit() and expression[i+2].isalpha()):
                        print("Wrong Input!!")
                        flag = False
                        break;
                if expression[i] == '=':
                    afterEqual = expression[i+1:]
                    beforeEqual = beforeEqual.replace(expression[i:], '')
                
            tempAfterEqual = afterEqual
            if flag == True:
                for i in range(len(afterEqual)):
                    if i != len(afterEqual) - 1:
                        if afterEqual[i].isalpha() and afterEqual[i+1].isdigit():
                            tempAfterEqual = tempAfterEqual.replace(afterEqual[i] + afterEqual[i+1], afterEqual[i] + '**' + afterEqual[i+1])
                    if i != len(afterEqual) - 1:
                        if afterEqual[i].isdigit() and afterEqual[i+1].isalpha():
                            tempAfterEqual = tempAfterEqual.replace(afterEqual[i] + afterEqual[i+1], afterEqual[i] + '*' + afterEqual[i+1])
                    if i != len(afterEqual) - 1:
                        if afterEqual[i].isalpha() and afterEqual[i+1] == '*' and afterEqual[i+2].isdigit():
                            tempAfterEqual = tempAfterEqual.replace(afterEqual[i] + afterEqual[i+1], afterEqual[i] + '*' + afterEqual[i+1])
                    if i != len(afterEqual) - 1:
                        if afterEqual[i].isalpha() and afterEqual[i+1].isalpha():
                            print("Wrong Input!!")
                            flag = False
                            break;
                            

                completeExpression = beforeEqual + tempAfterEqual
                expressionBeforeEqual = sympify(beforeEqual)
                expressionAfterEqual = sympify(tempAfterEqual)
                equation = Eq(expressionBeforeEqual, expressionAfterEqual)
                equation = Eq(equation.lhs - equation.rhs, 0)

            self.variables[tokens[1]] = equation
            self.variables['completeExpression'] = completeExpression
            self.variables['xLoc'] = x
            self.variables['yLoc'] = y
            
        elif tokens[0] == 'eval':
            solutions = []
            for i in np.arange(int(tokens[2]), int(tokens[3]) + 0.5, 0.5):
                equation_x = self.variables['exp'].subs(self.variables['xLoc'], i)
                solution_y = solve(equation_x, self.variables['yLoc'])
                if solution_y:
                    solutions.append((i, solution_y[0]))
            if 'y**2' not in self.variables['completeExpression']:
                xValues = []
                yValues = []
                for solution in solutions:
                    xValues.append(solution[0])
                    yValues.append(solution[1].evalf())
            else:
                xValues = []
                yValues = []
                for solution in solutions:
                    xValues.append(solution[0])
                    yValues.append(solution[1].evalf())
                for solution in solutions:
                    xValues.append(solution[0])
                    yValues.append(-solution[1].evalf())

            yValues = [val if val.is_real else float('nan') for val in yValues]
            self.variables['xValuesLoc'] = xValues
            self.variables['yValuesLoc'] = yValues

        elif tokens[0] == 'plot':
            plt.plot(self.variables['xValuesLoc'], self.variables['yValuesLoc'])
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.xlim(-20, 20)
            plt.ylim(-20, 20)
            plt.show()  
                      
        elif tokens[0] == 'exit':
            exit()
import sys

file_path = "program.na"
with open(file_path, 'r') as file:
    program = file.read()

interpreter = SimpleInterpreter()
interpreter.interpret(program)