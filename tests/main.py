import unittest
import io
import sys
import time

class TestRunTests(unittest.TestCase):
    
    def test_output(self):
        self.assertTrue("Hello, World!", "Hello, World!")


def run_tests(code_string:str,name_func:str='', input_str:str=''):
    start_time = time.time()

    test_output = io.StringIO()
    sys.stdout = test_output

    if input_str:
        sys.stdin = io.StringIO(input_str)

    mod = type(sys)('test')
    #code_string += "\n{0}({1})".format(name_func,input_str)

    exec(code_string, mod.__dict__)
    unittest.main(module=mod,exit=False)

    sys.stdout = sys.__stdout__
    if input_str:
        sys.stdin = sys.__stdin__
    value = test_output.getvalue()
    _time = '--- %s seconds ---' % (time.time() - start_time)
    return value,_time

code_string = '''
import unittest
class TestRunTests(unittest.TestCase):
    
    def test_output(self):
        self.assertTrue("Hello, World!", "Hello, World!")

        
rows = 2000
i = 1
while i <= rows:
    j = 1
    while j <= i:
        print((i * 2 - 1), end=" ")
        j = j + 1
    i = i + 1
    print()
'''

# Запускаем тесты
results = run_tests(code_string)

# Печатаем результаты проверки
print(results[-1])
