.. ###########################################################################
   This file contains reStructuredText, please do not edit it unless you are
   familar with reStructuredText markup as well as Sphinx specific markup.

   For information regarding reStructuredText markup see
      http://sphinx.pocoo.org/rest.html

   For information regarding Sphinx specific markup see
      http://sphinx.pocoo.org/markup/index.html

.. ########################### SECTION HEADING REMINDER ######################
   # with overline, for parts
   * with overline, for chapters
   =, for sections
   -, for subsections
   ^, for subsubsections
   ", for paragraphs

.. ---------------------------------------------------------------------------

**********************************************
cctconvert - A Cookiecutter Template Converter
**********************************************

.. image:: https://travis-ci.org/eruber/cookiecutter-template-converter.svg?style=flat-square
         :target: https://www.travis-ci.org/eruber/cookiecutter-template-converter
         :alt: Travis Build Status

.. image:: https://img.shields.io/appveyor/ci/eruber/cookiecutter-template-converter.svg?style=flat-square
         :target: https://ci.appveyor.com/project/eruber/cookiecutter-template-converter
         :alt: Appveyor Build Status

.. image:: https://codecov.io/gh/eruber/cookiecutter-template-converter/coverage.svg?branch=master
         :target: https://codecov.io/gh/eruber/cookiecutter-template-converter
         :alt: Test Coverage


.. image:: https://pyup.io/repos/github/eruber/cookiecutter-template-converter/shield.svg
         :target: https://pyup.io/repos/github/eruber/cookiecutter-template-converter
         :alt: Package Dependencies Up-to-Date Status


.. image:: https://pyup.io/repos/github/eruber/cookiecutter-template-converter/python-3-shield.svg
         :target: https://pyup.io/repos/github/eruber/cookiecutter-template-converter/
         :alt: Python 3 Ready Status

This utility saves a little bit of editing by converting a version 1
**Cookiecutter** template file to a version 2 template file.

After that **Cookiecutter** v2.x is required to use the version 2 template.

While the **Cookiecutter** v2 pull request is being considered, you can
find **Cookiecutter** v2.0.0 (which is a fork of **Cookiecutter** v1.6.0) at
`Cookiecutter v2 Fork`_.

For additional background on the technical details of the fork & the feature
set supported by the `Cookiecutter v2 Fork`_, see the implementation notes at
`Cookiecutter v2 Dev Notes`_.


Installation
============
From PyPI:

   pip install cctconvert


From source (acquired from the `cctconvert GitHub repo`_) if current directory
is the root of the project:

    pip install .


Usage
=====
Read the User Manual::

    cctconvert --help


Usage Example
=============

If there is a version 1 **cookiecutter.json** file in the current directory,
**cctconvert** knows what to do::

   cctconvert

and the output should look very similar to this::

   cctconvert 1.0.1 Fri Nov  3 09:52:16 2017
   Renaming input file to 'cookiecutter.json.v1.bkup'...
   Writing out version 2 cookiecutter template to file 'cookiecutter.json'

So now your current directory will contain two **Cookiecutter** template
files -- a backup of the original version 1 **Cookiecutter** template file
now named **cookiecutter.json.v1.bkup** and the newly generated version 2
**Cookiecutter** template file named **cookiecutter.json**.

However, if you don't like the idea of backing up the version 1 template file
by renaming it, then you can use the **--output** option to change the name
of the generated version 2 template file like this::

   cctconvert --output cookiecutter-v2.json

and the output should look something like this::

   cctconvert 1.0.1 Fri Nov  3 10:10:11 2017
   Writing out version 2 cookiecutter template to file 'cookiecutter-v2.json'

So again your current directory contains two **Cookiecutter** template
files -- the original version 1 **Cookiecutter** template file still named
**cookiecutter.json** and the newly generated version 2 **Cookiecutter**
template file named **cookiecutter-v2.json**.


Conversion Overview
===================

Examining the details of a conversion gives you an idea what **cctconvert**
is doing under the covers -- beginning with a non-trival version 1
**Cookiecutter** template file::

   {
     "full_name": "Rick Deckard",
     "email": "rd@tyrell.com",
     "occupation": "Bladerunner",
     "project_name": "Voigt-Kampff Statistics for Greater Los Angeles",
     "project_description": "Do Andriods Dream of Electric Sheep?",
     "_private_key": "unicorn-origami",
     "replicants": ["Roy Batty", "Zhora", "Leon", "Pris", "Rachel"],
     "retired": {
         "incept date met": ["Roy Batty"],
         "bladerunner" : ["Zhora", "Leon", "Pris"],
         "childbirth": ["Rachel"]
         }
   }

The above template contains a representative sample of the different flavors
of fields available in a version 1 **Cookiecutter** template file

* a private field (**\_private_key**) - prefixed with an underscore
* a choices field (**replicants**) - a list of choices, first choice being the default
* a dictionary field (**retired**) - a dictionary of data
* a normal field (**full\_name**, **email**, **occupation**, **project\_name**, **project\_description**) - variable name & default value


The above template converted to version 2 looks like this::

   {
       "name": "cookiecutter-transformed",
       "cookiecutter_version": "2.0.0",
       "_inception": "Transformed by cctconvert 1.0.1 Fri Nov  3 17:29:18 2017",
       "variables": [
           {
               "name": "full_name",
               "default": "Rick Deckard"
           },
           {
               "name": "email",
               "default": "rd@tyrell.com"
           },
           {
               "name": "occupation",
               "default": "Bladerunner"
           },
           {
               "name": "project_name",
               "default": "Voigt-Kampff Statistics for Greater Los Angeles"
           },
           {
               "name": "project_description",
               "default": "Do Andriods Dream of Electric Sheep?"
           },
           {
               "name": "_private_key",
               "default": "unicorn-origami",
               "prompt_user": false
           },
           {
               "name": "replicants",
               "default": "Roy Batty",
               "choices": [
                   "Roy Batty",
                   "Zhora",
                   "Leon",
                   "Pris",
                   "Rachel"
               ]
           },
           {
               "name": "retired",
               "default": {
                   "incept date met": [
                       "Roy Batty"
                   ],
                   "bladerunner": [
                       "Zhora",
                       "Leon",
                       "Pris"
                   ],
                   "childbirth": [
                       "Rachel"
                   ]
               }
           }
       ]
}

If you don't like the private **\_inception** variable in the header of the
version 2 template, then you can specify the command line option **--no-incept**
to suppress it (added in **cctconvert** v1.0.1).

Development & Test Setup
========================
If you have acquired the source code, you might want to run the unit tests.

Change directory to the root of the project, create a virtual environment,
activate it, install dependencies, and install **cctconvert**
in development mode -- on a Windows console the steps are::

   > python -m venv .cct-venv
   > .cct-venv\Scripts\activate
   (.cct-venv) pip install -r test-requirements.txt
   (.cct-venv) pip instal -e .

To run all the tests::

   (.cct-venv) pytest

You should see a coverage report that is similar to the one shown below (the
number of tests might have changed since this README was written, but coverage
should still be at %100)::

   ============================= test session starts =============================
   platform win32 -- Python 3.6.2, pytest-3.2.3, py-1.4.34, pluggy-0.4.0 --
   d:\devel\python\eru\repos\cookiecutter-template-converter\.cct-venv\scripts\python.exe
   cachedir: .cache
   rootdir: D:\Devel\python\eru\repos\cookiecutter-template-converter, inifile: setup.cfg
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


   ========================== 16 passed in 0.13 seconds ======================

To run tox::

   (.cct-venv) tox

You should see an output summary that is comforting, something like this::

   ___________________________________ summary _______________________________
     py33: commands succeeded
     py34: commands succeeded
     py35: commands succeeded
     py36: commands succeeded
     flake8: commands succeeded
     congratulations :)



.. _Cookiecutter v2 Dev Notes: http://cookiecutter-v2-fork-docs.readthedocs.io/en/latest/
.. _Cookiecutter v2 Fork: https://github.com/eruber/cookiecutter/tree/new-2.0-context
.. _cctconvert GitHub repo: https://github.com/eruber/cookiecutter-template-converter
