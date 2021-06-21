unit_tests = {}

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from lib.text_to_speech import Reader
from lib.get_dictionary import Librarian
from lib.config import testing

# Reader.text_to_speech() should not throw when passed any data-type
def test1(done):
    # first create all the data types
    example_list = ["i","am","example"]
    example_dict = {"testing right now": True, "happy": False, "am i cool?" : 100}
    def example_func():
        pass
    class Getting_out_of_hand():
        do_i_really_need_to_be_testing_it_with_a_class = "nope"
        so_why = "is funny"
    all_bad_data_types = ["stringy boi", 123, 123.123, True, False, example_list, example_dict, example_func, Getting_out_of_hand, None]

    # loop through every data type, making sure the function does not throw
    reader = Reader(use_test_dir=True)
    for data_type in all_bad_data_types:
        try:
            reader.text_to_speech(data_type)
        except Exception as e:
            e = str(e)
            msg = "reader.text_to_speech threw when it was passed:\n" + str(data_type) + "\n gave error msg:\n" + e
            raise AssertionError(msg)
    #if no exceptions were raised during the loop, the test is a pass
    done("Reader.text_to_speech() should not throw when passed any data-type")
unit_tests["Reader.text_to_speech() should not throw when passed any data-type"] = test1

def test2(done):
    # define input and expected output
    test_input = "testing hurts my neck"
    expected_outcome_path = "data/test/testing_hurts_my_neck.mp3"

    # create the reader and run with the test input
    reader = Reader(use_test_dir=True)
    reader.text_to_speech(test_input)

    # check to see if the file was created
    if os.path.exists(expected_outcome_path):
        # remove the file so the test can be ran multiple times
        os.remove(expected_outcome_path)

        # the file was created so the test passes
        done("Reader.text_to_speech() should create a file in the data/test dir")
    else:
        raise AssertionError("file: " + expected_outcome_path + " was not found")
unit_tests["Reader.text_to_speech() should create a file in the data/test dir"] = test2

# Reader.play_text() should not throw when passed any data-type
def test3(done):
    # first create all the data types
    example_list = ["i","am","example"]
    example_dict = {"testing right now": True, "happy": False, "am i cool?" : 100}
    def example_func():
        pass
    class Getting_out_of_hand():
        do_i_really_need_to_be_testing_it_with_a_class = "nope"
        so_why = "is funny"
    all_bad_data_types = ["stringy boi", 123, 123.123, True, False, example_list, example_dict, example_func, Getting_out_of_hand, None]

    # loop through every data type, making sure the function does not throw
    reader = Reader(use_test_dir=True)
    for data_type in all_bad_data_types:
        try:
            reader.play_text(data_type)
        except Exception as e:
            e = str(e)
            msg = "reader.play_text() threw when it was passed:\n" + str(data_type) + "\n gave error msg:\n" + e
            raise AssertionError(msg)
    #if no exceptions were raised during the loop, the test is a pass
    done("Reader.play_text() should not throw when passed any data-type")
unit_tests["Reader.play_text() should not throw when passed any data-type"] = test3

# Reader.parse_and_play() should not throw when passed any data-type
def test4(done):
    # first create all the data types
    example_list = ["i","am","example"]
    example_dict = {"testing right now": True, "happy": False, "am i cool?" : 100}
    def example_func():
        pass
    class Getting_out_of_hand():
        do_i_really_need_to_be_testing_it_with_a_class = "nope"
        so_why = "is funny"
    all_bad_data_types = ["stringy boi", 123, 123.123, True, False, example_list, example_dict, example_func, Getting_out_of_hand, None]

    all_bad_data_types = ["stringy boi"]

    # loop through every data type, making sure the function does not throw
    reader = Reader(use_test_dir=True)
    for data_type in all_bad_data_types:
        try:
            reader.parse_and_play(data_type)
        except Exception as e:
            e = str(e)
            msg = "reader.parse_and_play() threw when it was passed:\n" + str(data_type) + "\n gave error msg:\n" + e
            raise AssertionError(msg)
    #if no exceptions were raised during the loop, the test is a pass
    done("Reader.parse_and_play() should not throw when passed any data-type")
unit_tests["Reader.parse_and_play() should not throw when passed any data-type"] = test4

# parse and play should work even when called several times a second
def test5(done):
    reader = Reader(use_test_dir=True)
    words_list = ["hi","hi","hellow","i","am","testing","here"]
    for word in words_list:
        try:
            reader.parse_and_play(word)
        except Exception as e:
            e = str(e)
            msg = f"parse and play threw when passed: {word} and gave error msg:\n\n{e}"
            raise AssertionError(msg)

    # if the for loop completes with no errors the test is a pass
    done("parse and play should work even when called several times a second")
unit_tests["parse and play should work even when called several times a second"] = test5

# purge all mp3's should delete all mp3s in a dir and leave all other file types
def test6(done):
    example_file_names = ['testing.py',"test.js","my_sound.mp4","my_sound.mp3","index.js","page.html","moon.mp3","important.txt","new.py","my_cooler_sound.mp3","essay.txt","college_app.docx"]
    excepted_output = ['testing.py',"test.js","my_sound.mp4","index.js","page.html","important.txt","new.py","essay.txt","college_app.docx"]

    # purge all mp3's is in multiple classes so i add all of those to a list here
    librar = Librarian('test',testing,use_test_dir=True)
    reader = Reader(use_test_dir=True)

    class_list = [librar, reader]

    base_dir = librar.base_dir

    for my_class in class_list:

        # create all of these files in the test dir
        for example_file_name in example_file_names:
            full_path = base_dir + example_file_name
            with open(full_path, "w") as file_object:
                file_object.write('test')

        # run the purge all mp3's function
        my_class.purge_all_mp3_files()
        output = os.listdir(base_dir)

        # remove all files from the test
        test_dir = "data/test/" # this is hardcoded to 100% prevent accidental deletion of important .py files

        files_to_delete = os.listdir(test_dir)
        for file in files_to_delete:
            full_path = test_dir + file
            if os.path.exists(full_path):
                os.remove(full_path)
            else:
                print(f"could not delete: {full_path}")

        # compare result to expected output
        if output.sort() != excepted_output.sort():
            raise AssertionError(f"{output}\ndid not match the expected output:\n{excepted_output}\nwith class:\n{str(my_class)}")

    # if the for loop exists with no errors, the test is a pass
    done("purge all mp3's should delete all mp3s in a dir and leave all other file types")
unit_tests["purge all mp3's should delete all mp3s in a dir and leave all other file types"] = test6

# no matter what happens prior to it (even file deletion), running the confirm_mp3_path function should mean mp3 paths are valid
def test7(done):
    word_list = ["abed","iridescent","hello","abed","labyrinth","indomitable"]
    class_list = []

    for word in word_list:
        librar = Librarian(word, testing, use_test_dir=True)
        class_list.append(librar)

    for my_class in class_list:
        # run confirm_mp3_path so that all of these classes should already have valid mp3_path's
        my_class.confirm_mp3_path()

        # check to make sure all mp3_path's are valid
        for my_dict in my_class.data_list:
            full_path = my_dict["mp3_path"]
            if not os.path.exists(full_path):
                # if the path does not exist confirm_mp3_path failed 
                # and so does the test
                msg = f"{full_path} did not exist for word: {my_dict['word']}\nwith dict:\n{str(my_dict)}"
                raise AssertionError(msg)
        
        # i will delete all mp3 files and then run the confirm_mp3_path 
        # the files should be recreated
        my_class.purge_all_mp3_files()
        my_class.confirm_mp3_path()

        # check again to make sure all mp3_path's are valid
        for my_dict in my_class.data_list:
            full_path = my_dict["mp3_path"]
            if not os.path.exists(full_path):
                # if the path does not exist confirm_mp3_path failed 
                # and so does the test
                msg = f"!!!Please note that this error message is after the deletion!!!\n{full_path} did not exist for word: {my_dict['word']}\nwith dict:\n{str(my_dict)}"
                raise AssertionError(msg)
    
    # get rid of any remaining mp3's
    class_list[0].purge_all_mp3_files()

    # if all of the for loop exited with no errors raised, the test is a pass
    done("no matter what happens prior to it (even file deletion), running the confirm_mp3_path function should mean mp3 paths are valid")
unit_tests["no matter what happens prior to it (even file deletion), running the confirm_mp3_path function should mean mp3 paths are valid"] = test7



"""
# example tests
def one_plus_one_is_two(done):
    outcome = 1+1
    desired_outcome = 2
    assert outcome == desired_outcome, "1+1 was not equal to two"
    done("one plus one is equal to two")
unit_tests["one plus one is equal to two"] = one_plus_one_is_two

def one_plus_one_is_three(done):
    outcome = 1+1
    desired_outcome = 3
    assert outcome == desired_outcome, "1+1 was not equal to three"
    done("one plus one is equal to three")
unit_tests["one plus one is equal to three"] = one_plus_one_is_three
"""