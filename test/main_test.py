# all the tests are run here

# set path to root dir

# dependencies

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

# if this was run directly, use relative imports, otherwise don't
if __name__ == '__main__':
    from unit import unit_tests
    from integration import integration_tests
else:
    from test.unit import unit_tests
    from test.integration import integration_tests

class _App():
    def __init__(self):
        self.tests = {}

        # add unit tests
        self.tests["unit"] = unit_tests

        # add integration tests
        self.tests["integration"] = integration_tests

        # universal stuff for test runner
        # array to hold errors
        self.errors = []

        # successes counter
        self.successes = 0

        # how many tests there are
        self.limit = 0
        self.test_counter = 0

    def green(self, input_str):
        """log string in green"""
        input_str = str(input_str)
        print('\033[92m'+input_str+'\033[0m')
    
    def red(self, input_str):
        """log string in red"""
        input_str = str(input_str)
        print('\033[91m'+input_str+'\033[0m')

    def count_all_tests(self):
        """return number of tests in self.tests"""
        counter = 0
        for key in self.tests:
            if type(self.tests[key]) == dict:
                sub_tests = self.tests[key]
                for test_name in sub_tests:
                    if test_name in sub_tests.keys():
                        counter +=1

        return counter

    def done(self, temp_test_name):
        """called if a test does not throw"""
        self.green(temp_test_name)
        self.test_counter += 1
        self.successes += 1
        if self.test_counter == self.limit:
            self.produce_test_report()


    def run_all_tests(self):
        """run all of the tests"""
        # how many tests there are
        self.limit = self.count_all_tests()

        for key in self.tests:
            if type(self.tests[key]) == dict:
                sub_tests = self.tests[key]
                for test_name in sub_tests:
                    if callable(sub_tests[test_name]):
                        temp_test_name = test_name
                        test_value = sub_tests[test_name]

                        # try the test
                        try:
                            test_value(self.done)
                        except AssertionError as e: # this may need to be just except
                            self.errors.append({
                                'name' : temp_test_name,
                                "error" : e
                            })
                            self.red(temp_test_name)
                            self.test_counter += 1
                            if self.test_counter == self.limit:
                                self.produce_test_report()
                
    def produce_test_report(self):
        """print out the test results"""
        # header
        print("")
        print("------------------BEGIN TEST REPORT-----------------")
        print('Tests ran: ' + str(self.limit))
        print('Test passes: ' + str(self.successes))
        print('Test fails: ' + str(len(self.errors)))
        print("")

        # print any errors in detail if there were any
        if len(self.errors) > 0:
            print("------------------BEGIN ERROR DETAILS-----------------")
            print("")

            for error in self.errors:
                self.red(error["name"])
                print(error["error"])
                print("")


        print("")
        print("------------------END TEST REPORT-----------------")

if __name__ == "__main__":
    # run tester
    tester = _App()
    tester.run_all_tests()
