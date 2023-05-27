from lark import Lark, Transformer

# Define a custom transformer class to convert the AST to Java code
class PythonToJavaTransformer(Transformer):
    # a = 15 --> int a = 15;
    def assign_stmt(self, children):
        variable = str(children[0])
        value = str(children[1])
        java_code = f"int {variable} = {value};"
        return str(java_code)
    
    # print("hello") --> System.out.println("hello");
    def print_stmt(self,children):
        expr = str(children[0])
        java_code = f"System.out.println({expr});"
        return str(java_code)
    
    # a = input("Enter a word: ") 
    def input_stmt_str(self,children):
        variable = str(children[0])
        prompt = str(children[1])
        java_code = f"java.util.Scanner sc = new java.util.Scanner(System.in);\n"
        java_code += f"System.out.print({prompt});\n"
        java_code += f"String {variable} = sc.nextLine();"
        return str(java_code)
    
    # a = int(input("Enter a number: "))
    def input_stmt_int(self,children):
        variable = str(children[0])
        prompt = str(children[1])
        java_code = f"java.util.Scanner sc = new java.util.Scanner(System.in);\n"
        java_code += f"System.out.print({prompt});\n"
        java_code += f"int {variable} = sc.nextInt();"
        return str(java_code)

def main(python_code):

    grammar = '''start: stmt+

stmt: assign_stmt | print_stmt | input_stmt_str | input_stmt_int

assign_stmt: NAME "=" NUMBER
print_stmt: "print" "(" STRING ")"
input_stmt_str: NAME "=" "input" "(" STRING ")"
input_stmt_int: NAME "=" "int" "(" "input" "(" STRING ")" ")"

NAME: /[a-zA-Z_][a-zA-Z0-9]*/
STRING: /".*?"/
NUMBER: /\d+/

%ignore /\s+/'''

    # Create the parser with your grammar and the custom transformer
    parser = Lark(grammar, parser='lalr', transformer = PythonToJavaTransformer())

    # Parse the Python code into an AST
    #with open("demo.py","r") as f:
    #    python_code = f.read()
    ast = parser.parse(python_code)

    # Convert the AST to Java code
    java_code = PythonToJavaTransformer().transform(ast).pretty()
    result = java_code.split("\t")
    #print(result[-1])
    return result[-1]
    
