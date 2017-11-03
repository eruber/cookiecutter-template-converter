# cctconvert #

Converts cookiecutter v1 template to a v2 template.

After that Cookiecutter v2.x is required to use the v2 template.


# Installation #

From PyPI:

   $ pip install cctconvert

From source if current directory is the root of the project:

    $ pip install .


# Usage #

Read the User Manual:

    $ cctconvert --help
                                            
# Manual Conversion # 

Is best illustrated with an example, beginning with a simple version 1 Cookiecutter template::
	
	{
	    "full_name": "Raphael Pierzina",
	    "github_username": "hackebrot",
	    "project_name": "Kivy Project",
	    "repo_name": "{{cookiecutter.project_name|lower}}",
	    "orientation": ["all", "landscape", "portrait"]
	}

The above template converted to version 2 would look like this::
	
	{
	    "name": "cookiecutter-kivy-project",
	    "cookiecutter_version": "2.0.0",
	    "variables" : [
	        {
	            "name": "full_name",
	            "default": "Raphael Pierzina",
	        },
	        {
	            "name": "github_username",
	            "default": "hackebrot",
	        },
	        {
	            "name": "project_name",
	            "default": "Kivy Project",
	        },
	        {
	            "name": "repo_name",
	            "default": "{{cookiecutter.project_name|lower}}",
	        },
	        {
	            "name": "orientation",
	            "default": "all",
	            "choices": ["all", "landscape", "portrait"]
	        },
	    ]
	}

#  Deveopment & Test Env Setup #

Change directory to the root of the project and do:

	pip install -r dev-requirements.txt
	pip install -r test-requirements.txt
	pip instal -e .

To Run all the tests:

	pytest

You should see a coverage report that is similar to this (the number of tests, might have changed,
but coverage should be at %100):
	
	============================= test session starts =============================
	platform win32 -- Python 3.6.2, pytest-3.2.3, py-1.4.34, pluggy-0.4.0 -- d:\devel\_python\__eru\___repos\cookiecutter-template-converter\.cct-venv\scripts\python.exe
	cachedir: .cache
	rootdir: D:\Devel\_python\__eru\___repos\cookiecutter-template-converter, inifile: setup.cfg
	plugins: mock-1.6.3, datafiles-1.0, cov-2.5.1
	collected 16 items
	
	tests/test_convert.py::test_unable_to_read_input_error PASSED
	tests/test_convert.py::test_unable_to_write_output_error PASSED
	tests/test_convert.py::test_input_file_cannot_be_renamed_error PASSED
	tests/test_convert.py::test_output_file_already_exists_error PASSED
	tests/test_convert.py::test_no_specified_input_file_error PASSED
	tests/test_convert.py::test_no_default_input_file_error_exits PASSED
	tests/test_convert.py::test_input_file_already_v2_error PASSED
	tests/test_convert.py::test_input_file_already_v2_error_with_verbose PASSED
	tests/test_convert.py::test_input_is_empty_json PASSED
	tests/test_convert.py::test_version_option_z PASSED
	tests/test_convert.py::test_version_option_version PASSED
	tests/test_convert.py::test_clear_option PASSED
	tests/test_convert.py::test_dryrun_option PASSED
	tests/test_convert.py::test_full_processing_defaults_no_verbose_option PASSED
	tests/test_convert.py::test_full_processing_default_input_file_verbose_option PASSED
	tests/test_convert.py::test_full_processing_with_name_option_and_output_option PASSED
	
	----------- coverage: platform win32, python 3.6.2-final-0 -----------
	Name                       Stmts   Miss  Cover   Missing
	--------------------------------------------------------
	cctconvert\__init__.py         0      0   100%
	cctconvert\cctconvert.py     113      0   100%
	--------------------------------------------------------
	TOTAL                        113      0   100%
	
	
	========================== 16 passed in 0.13 seconds ==========================
