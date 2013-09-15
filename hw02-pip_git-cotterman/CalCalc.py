# Instructions: Write a module called CalCalc, with a method called "calculate" that evaluates any string passed to it,
# and can be used from either the command line (using argparse with reasonable flags) or imported within Python
# Feel free to use something like eval(), but be aware of some of the nasty things it can do, and make sure it doesn't have too much power:
# http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html


import argparse

def get_command_lines():
    parser = argparse.ArgumentParser(description='User input to parse')
    parser.add_argument('mystring', help='This is the string to evaluate')
    parser.add_argument('-t', action='store_true', default=True,
                        dest='boolean_switch',
                        help='Set a switch to true')
    parser.add_argument('-f', action='store_false', default=True,
                        dest='boolean_switch',
                        help='Set a switch to false')
    return parser.parse_args()
    

def calculate(mystring, wolfram=True):
    return eval(mystring)


def main():
    results = get_command_lines()
    evaluation = eval(results.mystring)
    print 'The expression "' , results.mystring, '" evaluates to: \n', evaluation
    print 'Evaluated using the Wolfram-Alpha API   =', results.boolean_switch

#This if statement says that this script (CalCalc.py) is run directly, then execute main.  (else do not)
if __name__ == '__main__':
    main()
