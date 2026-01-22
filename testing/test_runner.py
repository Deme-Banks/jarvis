"""
Test Runner for JARVIS Components
"""
import unittest
import sys
import os
from typing import List, Dict
import json


class TestRunner:
    """Run tests for JARVIS components"""
    
    def __init__(self):
        self.test_results = []
    
    def run_all_tests(self) -> Dict:
        """Run all tests"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Discover tests
        test_dir = os.path.dirname(__file__)
        tests = loader.discover(test_dir, pattern='test_*.py')
        suite.addTests(tests)
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful(),
            'failures_detail': result.failures,
            'errors_detail': result.errors
        }
    
    def run_specific_test(self, test_module: str, test_class: str = None, 
                         test_method: str = None) -> Dict:
        """Run specific test"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        try:
            if test_method and test_class:
                # Specific test method
                module = __import__(test_module, fromlist=[test_class])
                test_class_obj = getattr(module, test_class)
                test = test_class_obj(test_method)
                suite.addTest(test)
            elif test_class:
                # All tests in class
                module = __import__(test_module, fromlist=[test_class])
                test_class_obj = getattr(module, test_class)
                suite.addTests(loader.loadTestsFromTestCase(test_class_obj))
            else:
                # All tests in module
                suite.addTests(loader.loadTestsFromName(test_module))
        except Exception as e:
            return {'error': str(e)}
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        }
