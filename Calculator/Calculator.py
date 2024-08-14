import re
import math
from fractions import Fraction

#This is a calculator as an excuse to begin learning python
#It can ideally handle any function/operation in any order or complexity using the following symbols: +-*/^()
#It is not terribly efficient code, but it seems to work and I certainly learned a lot about python doing this

tOp = 0 #Global Variable for Test Mode Operations No. for the Calculator test

class basic_calculator:

    #Functions
    def introduction(self):
        print("\nWelcome to my Python Calculator!\n")
        print("Currently the calculator can handle computation within the following parameters:")
        print("Any arithmetic using the following symbols/operations: +-*/^()\nStandard python float value limits(approx. +- 1.7*10^308)\n=============\n\n")
        
    def CalculatorTest(self, tOp): #Tests calculator functionality
            tOperation = [
                #Addition/Subtraction Tests
                "2+2",
                "2.1+2.5",
                "1000+100",
                "-1000+100",
                "-1000+-100",
                "-1000.128+-100.125",
                "2.1+2.5002000",
                "(1+1)",
                "((1+1))",
                "2+-1",
                "-2+1",
                "2-2",
                "2.1-2.5",
                "2-1",
                "2-3",
                "2--2",
                "(1+1)-2",
                "2-(1+1)",
                "(1-2)-(1+1)",
                "(1+1)+2",
                "2+(1+1)",
                "(1-2)+(1+1)",
                "1000-100",
                "-1000-100",

                #Division Tests
                "2/2",
                "2.1/2.5",
                "2/1",
                "2/3",
                "2/0",
                "0/2",

                #Multiplication Tests
                "2*2",
                "2.1*2.5",
                "2*-2",
                "-2*2",
                "-2*-2",

                #Exponent Tests
                "2^2",
                "2.1^2.5",
                "999^999", #Should result in a computation error as implementation may be set in the future.
                "2^0",
                "2^1",
                "2^-2",
                "-2^2",
                "-2^-2",
                "2^(2+1)",
                "2^-(2+1)",
                
                #Complex Parentheses Test
                "20^-(2+1)(1-2.56902^(2+1))+(1+1)-2.13/2.523*((1.21+13))-100+10-750"
            ]
            print("Test No. %d\nTested Operation: %s" % (tOp, tOperation[tOp-1]))
            return tOperation[tOp-1]

    #Validates requests and formats as needed
    def calculationRequest(self):
        global tOp
        if tOp > 0:
            strReq = 'TEST'
        else:
            strReq = input() #Allows user to enter a request via cmd prompt
            if strReq == "": #Formats for when 'nothing' is entered
                strReq = '0'
        if strReq == 'TEST': #Sends Calculator into test mode to help ensure proper functionality
            if tOp == 0: tOp =+ 1
            strReq = self.CalculatorTest(tOp)
        strReq = str(strReq.replace(" ", "")) #Eliminates white space from input
        request = list(strReq) #Turns the userinput into a list
        rightP = leftP = pCount = epcount = eptarget = i = 0
        negative_power = False
        symbols = ['.', '(', ')']
        operations = ['^', '+', '-', '*', '/']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', '-9']
        allowed_characters = numbers + symbols + operations

        #Checks for disallowed characters *(ARITHMETIC 1)*
        if not all(char in allowed_characters for char in request):
            print("ERROR: Incorrect Arithmetic 1")
            return False, request, 0
        
        while i != len(request): #Enumerates through the request to check for validity (Use of while loop instead of for to manipulate value i)

            #Inserts a "*" between numbers and parentheses that are without other operations present
            if i < len(request)-1: #Checks index range
                if (request[i] in numbers and request[i+1] == '(') or (request[i+1] in numbers and request[i] == ')'):
                    request.insert(i+1, '*')

            #Ensures user input begins and ends with a number or parenthesis (including negative numbers) *(ARITHMETIC 2)*
            try:
                int(request[0])
                int(request[-1])
            except:
                try:
                    float(request[0])
                    float(request[-1])
                except:
                    if request[0] != '(' and request[0] != '-' and request[-1] != ')':
                        print("ERROR: Incorrect Arithmetic 2")
                        return False, request, 0

            #Adjusts request for negative numbers
            if request[i] == '-' and request[i+1] in numbers: #For turning '#-#' to #+(-#)
                j = request[i] + request[i+1]
                request[i+1] = j
                request.pop(i)
                try:
                    num = float(request[i-1])
                    if i != 0 and isinstance(num, float):
                        request.insert(i, '+')
                except:
                    ''
                if '.' in str(request[i-1]): #For turning '#-#' to #+(-#) for decimal values being compared
                    fractionVar, intVar = math.modf(float(request[i-1]))
                    if fractionVar > 0 and request[i+1] != '+' and request[i] != '+':
                        request.insert(i, '+')
                if i != 0 and request[i-1] == ')':
                    request.insert(i, '+')
            if request[i] == '-' and request[i+1] == '-' and request[i+2] in numbers: #For turning '#--#' to #-(-#)
                j = request[i+1] + request[i+2]
                request[i+2] = j
                request.pop(i+1)
            if (request[i] == '+' or request[i] == '^') and (request[i+1] == '-' and request[i+2] in numbers): #For turning '#+-#' to #+(-#)
                j = request[i+1] + request[i+2]
                request[i+2] = j
                request.pop(i+1)
            if request[i] == '^' and (request[i+1] == '-' and request[i+2] in numbers): #For turning '#^-#' to #^(-#)
                j = request[i+1] + request[i+2]
                request[i+2] = j
                request.pop(i+1)
            
            #Adjusts request for negative powers encapsulated in parentheses @Ex: turning '#^-(#)' to '#^((-1)*(#))' including '#^-(#^-(#))' formats
            if i < len(request)-3: #Checks index range
                if request[i] == '^' and request[i+1] == '-' and request[i+2] == '(' and negative_power == False:
                    power_start = i+1
                    request.pop(i+1)
                    negative_power = True
                if negative_power == True and request[i+1] == '(':
                    epcount += 2
                if negative_power == True and request[i+3] == ')':
                    eptarget += 1
                if negative_power == True and request[i+3] == ')' and eptarget == epcount/2:
                    request.insert(i+3, ')')
                    request.insert(power_start, '(')
                    request.insert(power_start+1, '(')
                    request.insert(power_start+2, '-1')
                    request.insert(power_start+3, ')')
                    negative_power = False
                    leftP = rightP = i = 0

            #Ensures an alternating symbol/number pattern in entry *(ARITHMETIC 3)*
            if i < len(request)-1: #Checks index range
                if request[i] in operations and request[i+1] in operations: #Note that a "--" never gets seen here due to being processed earlier into a "+"
                    if request[i] == '^' and request[i+1] == '-' or request[i] == '*' and request[i+1] == '-': #Omits '^-' patterns
                        ''
                    else:
                        print("ERROR: Incorrect Arithmetic 3")
                        return False, request, 0
            
            #Adjusts the list for multidigit integers
            if i < len(request)-1: #Checks index range
                try:
                    while isinstance(int(request[i]), int) and request[i+1] in numbers: #Attempts to convert string index to int and compare to the next index
                            j = request[i] + request[i+1]
                            request[i] = j
                            request.pop(i+1)
                            if i >= len(request)-1: #Exits loop if it reaches the last index
                                break
                except:
                    ''

            #Adjusts the list for decmial numbers
            if i < len(request)-2: #Checks index range
                try:
                    if isinstance(int(request[i]), int) and request[i+1] == '.': #Attempts to convert string index to int and compare to the next index

                        #Combines the integer and decimal into 1 index
                        j = request[i] + request[i+1]
                        request[i] = j
                        request.pop(i+1)

                        #Combines the fractional place values into the index
                        while request[i+1] in numbers: #i+1 at this point is now after the decimal point
                            j = request[i] + request[i+1]
                            request[i] = j
                            request.pop(i+1)
                            if i >= len(request)-1: #Exits loop if it reaches the last index
                                break
                except:
                    ''

            if ')' in request or '(' in request:
                if request[i] == ')': #Counts right parentheses and Ensures (...) Parentheses Formatting
                    rightP += 1
                    if leftP < rightP: #Ensures a right parenthesis always follows a left parenthesis
                        print("ERROR: Incorrect Arithmetic 5")
                        return False, request, 0
                if request[i] == '(': #Counts left parentheses and replaces any '()' with '(0)' and any ..(..) with ..*(..)
                    leftP += 1
                    if request[i] == '(' and request[i + 1] == ')': #Repalce "()" with "(0)"
                        request.insert(i+1, '0')
                    if (i > 0 and request[i-1].isdigit() and request[i] == '(') or (0 < i and request[i-1] == ')' and request[i] == '('): #Repalce ..(..) with ..*(..)
                        request.insert(i, '*')
                        leftP -= 1
            
            i += 1

        #Adjusts the input formatting for beginning with a negative value
        if request[0] == '-':
                j = request[0] + request[1]
                request[0] = j
                request.pop(1)

        #Encapsulates the request in parenthesis for processing order purposes
        request.insert(0, '(')
        request.append(')')
        leftP += 1
        rightP += 1

        pCount = leftP + rightP #Adds up the total number of parentheses
        if not pCount % 2 == 0: #Ensures there is an even amt of parentheses present
            print("ERROR: Uneven Parenthesis")
            return False, request, 0

        #If conditions met, make calculations
        return True, request, pCount

    #Performs calculations within parentheses and updates/simplifies original request until the answer is found
    def performCalculation(self, userInput, pCount):
        userInput = list(userInput)
        result = lengthOfPart = startOfPart = leftP = x = addCount = subCount = multCount = divCount = expoCount = 0

        #Calculations Using PEMDAS
        while pCount > 0:
            for i, charac in enumerate(userInput):
                targetP = pCount/2

                #Repeats a simplification process until an answer is found
                if pCount > 0:
                    if charac == '(':
                        leftP += 1
                        if leftP == targetP: #Identifies right most '('
                            partialInput = []
                            startOfPart = i
                            for j in range(i, len(userInput)): #Iterates from i to end of user input but actually stops once the next '(' is found
                                partialInput.append(userInput[j])
                                
                                #Counts each operation in the partial
                                if partialInput[x] == '+':
                                    addCount += 1
                                if partialInput[x] == '-':
                                    subCount += 1
                                if partialInput[x] == '*':
                                    multCount += 1
                                if partialInput[x] == '/':
                                    divCount += 1
                                if partialInput[x] == '^':
                                    expoCount += 1

                                x += 1
                                    
                                if userInput[j] == ')': #Stops loop once parentheses are isolated
                                    leftP -= 1
                                    lengthOfPart = len(partialInput)
                                    break
                            
                            #Calculates partialInput by simplification and reinsertion into original request
                            while len(partialInput) != 1: #Simplifies partial input as much as possible
                                for i, partialC in enumerate(partialInput):

                                    #Calculate and simplify
                                    if partialC == '^': # E in PEMDAS
                                        base = float(partialInput[i-1])
                                        power = float(partialInput[i+1])
                                        fractionPower, intPower = math.modf(power)
                                        if fractionPower == 0: #Base raised to integer powers calculation
                                            result = pow(base, power)
                                        if fractionPower != 0: #Base raised to fractional powers calculation
                                            fraction = Fraction(partialInput[i+1]).limit_denominator()
                                            if base != abs(base) and fraction.denominator % 2 == 0: #Returns an error if result is an imaginary number (May implement compatibility later)
                                                return 'ERROR'
                                            else:
                                                result = base ** power
                                                if isinstance(result, complex): #Manually calculates negatives to fractional powers with odd denominators
                                                    result = -(-base) ** power
                                        expoCount -= 1
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.insert(i-1, result)
                                    if expoCount == 0 and partialInput[i] == '*': # M in PEMDAS
                                        result = float(partialInput[i-1]) * float(partialInput[i+1])
                                        multCount -= 1
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.insert(i-1, result)
                                    if multCount == expoCount == 0 and partialInput[i] == '/': # D in PEMDAS
                                        if float(partialInput[i+1]) == 0: #Error returned when dividing by 0
                                            return 'ERROR'
                                        result = float(partialInput[i-1]) / float(partialInput[i+1])
                                        divCount -= 1
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.insert(i-1, result)                                        
                                    if multCount == divCount == 0 and partialInput[i] == '+': # A in PEMDAS
                                        result = float(partialInput[i-1]) + float(partialInput[i+1])
                                        addCount -= 1
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.insert(i-1, result)
                                    if addCount == 0 and partialInput[i] == '-': # S in PEMDAS
                                        result = float(partialInput[i-1]) - float(partialInput[i+1])
                                        subCount -= 1
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.pop(i-1)
                                        partialInput.insert(i-1, result)

                                    if len(partialInput) == 3: #Once partial is reduced, turns (#) into just the number #
                                        partialInput.pop(0)
                                        partialInput.pop(-1)
                                        userInput.insert(startOfPart, str(partialInput[0]))
                                        for i in range (lengthOfPart):
                                            userInput.pop(startOfPart+1)
                            pCount -= 2
                            leftP = x = 0
        return partialInput[0]
    
    
#****************************************************************************************************************************************************************************


    def main(self):
        global tOp
        tErrors = []

        #Beginning of calculator
        self.introduction()

        while 1==1:

            validReq, userInput, pCount = self.calculationRequest()

            if validReq == True:
                try:
                    answer = self.performCalculation(userInput, pCount)

                    #Formats Answer
                    if answer == 'ERROR':
                            print("ERROR")
                    else:
                        answer = float(answer) #Converts to float first to avoid type comparison errors with int
                        if answer != int(answer):
                            answer = ('{:.10f}'.format(answer)).rstrip('0')
                            print("Answer: %s" % answer) #Prints float answer
                        else:
                                print("Answer: %s" % int(answer)) #Prints integer answer

                except:
                    if tOp > 0:
                        tErrors.append(tOp)
                        print("Error on Test No. %d\nOperation: %s" % (tOp, userInput))
                    print("Float value limits reached. Implementation possibly planned in the future.")

            else: 
                print("Please enter a valid request.")

            print() #Prints new line
            
            if tOp > 0: #Increments the test operation counter if the test mode was initiated
                        tOp += 1
                        if tOp == 47: #Resets the test operation counter if it reaches the end of the test
                            if tErrors != []:
                                for i in tErrors: #Prints out all testing errors
                                    print("Error on Test No. %d" % i)
                            print("\n=============\n\n")
                            tOp = 0
                            tErrors = []
            answer = ''

#******************************************************

#Executes main method
if __name__ == "__main__":
    calculator = basic_calculator()
    calculator.main()