"""
Testing Framework - Unit tests, integration tests
"""
import unittest
import os
import sys
from typing import List, Dict
from datetime import datetime


class JARVISTestFramework:
    """Testing framework for JARVIS"""
    
    def __init__(self):
        self.test_results = []
        self.test_suite = unittest.TestSuite()
    
    def create_test(self, test_name: str, test_function, 
                   expected_result=None) -> Dict:
        """Create a test case"""
        class TestCase(unittest.TestCase):
            def test_method(self):
                result = test_function()
                if expected_result:
                    self.assertEqual(result, expected_result)
                else:
                    self.assertIsNotNone(result)
        
        test_case = TestCase()
        test_case.test_method.__name__ = test_name
        self.test_suite.addTest(test_case)
        
        return {
            "test_name": test_name,
            "created": datetime.now().isoformat()
        }
    
    def run_tests(self) -> Dict:
        """Run all tests"""
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(self.test_suite)
        
        return {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "success": result.wasSuccessful()
        }
    
    def create_integration_test(self, module_name: str, 
                                test_cases: List[Dict]) -> str:
        """Create integration test file"""
        test_file = f"tests/test_{module_name}_integration.py"
        os.makedirs("tests", exist_ok=True)
        
        test_code = f'''"""
Integration tests for {module_name}
"""
import unittest
import sys
sys.path.insert(0, '../')

from {module_name} import *

class Test{module_name.title()}Integration(unittest.TestCase):
'''
        
        for i, test_case in enumerate(test_cases):
            test_code += f'''
    def test_{test_case.get("name", f"case_{i}")}(self):
        """{test_case.get("description", "")}"""
        {test_case.get("code", "pass")}
'''
        
        test_code += '''
if __name__ == '__main__':
    unittest.main()
'''
        
        with open(test_file, 'w') as f:
            f.write(test_code)
        
        return test_file
