Industry Standard Mandatory Guidelines
1.1. Imports, Blank Lines, and the Indentations:
. One copyright header file 
• First of all, the standard library imports like import |os et... 
• One extra line and then Third party imports 
. One Extra line and Finally, local library import 
• Two blank lines for top level functions or class declaration after all imports 
• Don't forget to add a space between different group of imports


1.2. The length of the Line and the Line Breaks:
• The length of the line should not be greater than 99 characters. and should exactly align with variable call. Pls set this up in Pycharm Settings to keep tracking of this rule.

1.3. Whitespaces, Trailing Commas, and String Quotes:
• One should avoid extra white spaces, there must be a single white space around both sides of an operator, one after the comma and none inside opening or closing of parenthesis. 
• Both single quotes and double quotes are acceptable in python, you should use both if you need quotes inside quotes to avoid syntax error and extra backslash.

1.4. Naming Conventions
• Use grammatically correct variable names, the class name(Ex.FilterAwareClientlinuxlogs) should start with an uppercase and must follow camelCase convention If more than two words are to be used.


• In the same way, a function name(Ex: model_generation) and variables (Ex: dir_path) should be joined with an underscore, and it must be lowercase. 
• In method arguments, always use self as the first argument to declare an instance variable.
. Constants are declared in all capital letters. Ex: TEST_FOLDER, INPUT_MODELS_SHEET etc.

2. Good to Have Recommendations:
There are certain coding recommendations that should be kept in mind to be consistent with an errorless and quality of code. I will list down the points and then explain them later in the code.
2.1. Exception Handling for every critical situation
2.2. Documentation of a Class & it's Methods:
Documenting every method with proper specification of parameters, return type, and data types. Try to avoid multiple returns from a function, single generic return is preferred
2.3.Use DRY (Don't Repeat Yourself):
   
Always use the DRY principle to reuse the code. The best way to do it is to use functions and classes. The common functions can be put into a separate utils.py file and can be used several times instead of creating similar functions again and again. 
Suppose if you need to read three files, instead of writing code for file read thrice, you can read it as a function and save your time.

2.4. What to use? Tuples, Lists of Dictionaries
Use tuples when data is non-changeable, dictionaries when you need to map things, and lists if your data can change later on.

2.5.Use the "with' statement while opening a file, the 'with' statement closes the file even if there is an exception raised

3. Optional Guidelines 3.1. If you are developing a code from Scratch, Try to draw Sequence diagram using Star UML feature available in Python

 4. Conclusion:
    • The quality code is one that is well structured, well documented, and well explained with comments.
    • The better the quality we write, the more readability it provides and easier it becomes to remember and to understand.
    • To keep the code consistent with PEP8, you can use various IDEs or editors. I personally use Pycharm for coding, it provides built-in linters.
    . All of them have plugins for inbuilt linters. In my view, these IDES can only help us to code better, your willingness to write good code still depends on you.
    . Short Summary.
    ◦ Functions: lower_case_with_underscores
    ○ Classes: CamelCaseFirstUpper
    ◦ Class methods: lower_case_with_underscores
    Local variables: lower. case_ with_ underscores
    ◦ Function parameters: lower_case with_underscores
    ◦ Global variables: UPPER_CASE_WITH_UNDERSCORES

--------------------------------------------------------------------------------------------------------------------------------------------------------
---

# Company Standard Python Coding Guidelines

## 1. Code Structure and Formatting

### 1.1 Imports, Blank Lines, and Indentation
- **Import Order**:
  1. Standard library imports (e.g., `import os`)
  2. Third-party library imports (e.g., `import numpy as np`)
  3. Local application/library imports (e.g., `from my_module import my_function`)
  
- **Blank Lines**:
  - Use two blank lines before top-level function or class declarations.
  - Use one blank line between different groups of imports.

- **Indentation**:
  - Use 4 spaces per indentation level.
  
### Example:
```python
# Copyright Header

import os
import sys  # Standard library imports

import numpy as np  # Third-party imports

from my_module import my_function  # Local imports


class MyClass:
    """Example class to demonstrate guidelines."""

    def __init__(self):
        self.value = 0  # Instance variable

    def increment(self):
        """Increment the value by 1."""
        self.value += 1
```

## 2. Line Length and Breaks
- Limit all lines to a maximum of 99 characters.
- Break lines before operators or after commas to maintain readability.
  
### Example:
```python
result = (some_function(argument1, argument2, argument3) +
          another_function(argument4, argument5))
```

## 3. Whitespaces, Trailing Commas, and String Quotes
- Avoid extra whitespace. Use a single space around operators and after commas. Do not use spaces inside parentheses.
- Both single quotes and double quotes are acceptable. Use them consistently throughout your code.

### Example:
```python
# Good example
my_list = [1, 2, 3, 4]

# Bad example
my_list = [1,2, 3,4]

# Use of quotes
message = "Hello, World!"  # or message = 'Hello, World!'
```

## 4. Naming Conventions
- **Functions and Variables**: Use `lower_case_with_underscores`.
- **Classes**: Use `CamelCase`.
- **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES`.
- **Method Parameters**: Use `lower_case_with_underscores`.

### Example:
```python
# Function and variable names
def calculate_area(radius):
    return 3.14 * radius ** 2

# Class name
class Circle:
    MAX_RADIUS = 100  # Constant

    def __init__(self, radius):
        self.radius = radius  # Instance variable
```

## 5. Documentation and Comments
- Use docstrings to document all public modules, functions, classes, and methods. The docstring should describe the purpose, parameters, return type, and exceptions raised.
- Use inline comments sparingly and only when necessary to explain complex logic.

### Example:
```python
def divide(a, b):
    """
    Divide two numbers.

    Parameters:
    a (float): The numerator.
    b (float): The denominator.

    Returns:
    float: The result of the division.

    Raises:
    ValueError: If the denominator is zero.
    """
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b
```

## 6. Error Handling
- Use exception handling (`try`/`except`) for error management.
- Avoid catching broad exceptions; instead, catch specific exceptions where possible.

### Example:
```python
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
```

## 7. Use of the `with` Statement
- Always use the `with` statement when working with file operations to ensure proper resource management.

### Example:
```python
with open('file.txt', 'r') as file:
    data = file.read()
# File is automatically closed here
```

## 8. Avoid Code Duplication (DRY Principle)
- Follow the DRY (Don't Repeat Yourself) principle. Use functions and classes to encapsulate reusable code and logic.

### Example:
```python
def read_file(file_path):
    """Read the contents of a file."""
    with open(file_path, 'r') as file:
        return file.read()

# Use the function to read multiple files
data1 = read_file('file1.txt')
data2 = read_file('file2.txt')
```

## 9. Unit Testing
- Write unit tests for all new features and functions. Aim for high test coverage.
- Use a testing framework like `unittest` or `pytest`.

### Example:
```python
import unittest

class TestMathFunctions(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

if __name__ == '__main__':
    unittest.main()
```

## 10. Version Control
- Use version control systems like Git for managing code changes. 
- Write meaningful commit messages and follow a branching strategy (e.g., Git Flow).

### Example Commit Message:
```
feat: add divide function for mathematical operations
```

## Conclusion
Writing high-quality Python code is essential for maintainability, readability, and collaboration. By adhering to these guidelines, you contribute to a codebase that is easier to understand, extend, and debug. Remember, the tools you use can help enforce these standards, but your commitment to writing clean code is what truly matters.

---

By following these comprehensive guidelines, your development team can create robust and maintainable Python applications that adhere to best practices.

