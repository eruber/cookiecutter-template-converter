# -*- coding: utf-8 -*-
"""
Unit tests for cctconvert

   RC
 -----
   0  No Error
  -1  Unable to load cookiecutter.json file
  -2  Unable to write cookiecutter.json file
  -3  Input file cannot be renamed (backedup) file already exists
  -4  Output file already exists
  -5  Input file does not exist
  -6  Input file is already a version 2 file

"""

import os
import codecs
import json
import collections

import pytest


from cctconvert import cctconvert

PROG_NAME = 'cctconvert'
IDENT = '{p} {v}'.format(p=PROG_NAME, v=cctconvert.VERSION)

TEST_SUPPORT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_support',)   # noqa


def load_json_file(json_file):
    with codecs.open(json_file, 'r', encoding='utf8') as f:
        json_object = json.load(f, object_pairs_hook=collections.OrderedDict)

    return(json_object)

# ---------------------- TESTS BEGIN HERE ------------------------------------


@pytest.mark.datafiles(
    os.path.join(TEST_SUPPORT_DIR, 'input', 'bad.json'),
)
def test_unable_to_read_input_error(datafiles, runner):
    """
    Specified cookiecutter.json file is corrupt
    """
    # For info on how pytest-datafiles works...
    # See: https://pypi.python.org/pypi/pytest-datafiles
    # See: https://github.com/omarkohl/pytest-datafiles
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['bad.json'])  # default CLI args

    assert IDENT in result.output

    msg = "Exception: Unable to load cookiecutter file 'bad.json'"
    assert msg in result.output

    assert result.exit_code == -1


@pytest.mark.datafiles(
    os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json'),
)
def test_unable_to_write_output_error(mocker, datafiles, runner):
    """
    While writing output json file, the json.dump() function raises
    an exception
    """
    mocker.patch(
        'json.dump',
        side_effect=ValueError,
        autospec=True
    )

    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['empty.json', '--output', 'v2.json'])  # default CLI args

    assert IDENT in result.output

    msg = "Exception: Unable to write cookiecutter file 'v2.json'"
    assert msg in result.output

    assert result.exit_code == -2


@pytest.mark.datafiles(
    os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json'),
    os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json.v1.bkup')
)
def test_input_file_cannot_be_renamed_error(datafiles, runner):
    """
    The input file cannot be backed up because a file of the same name
    already exists.
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 2

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['empty.json'])  # default CLI args

    assert IDENT in result.output

    msg = "ERROR: Input file 'empty.json' cannot be renamed to 'empty.json.v1.bkup' because that file already exists!!"
    assert msg in result.output

    assert result.exit_code == -3


@pytest.mark.datafiles(
    os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json'),
    os.path.join(TEST_SUPPORT_DIR, 'input', 'v2.json')
)
def test_output_file_already_exists_error(datafiles, runner):
    """
    The output v2 json file cannot be written because a file of the same
    name already exists.
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 2

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['empty.json', '--output', 'v2.json'])  # default CLI args

    assert IDENT in result.output

    msg = "ERROR: Output file 'v2.json' already exists!!"
    assert msg in result.output
    msg = "Change the output filename via option --output-file or delete it"
    assert msg in result.output

    assert result.exit_code == -4


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'junk.txt'))
def test_no_specified_input_file_error(datafiles, runner):
    """
    The input template file as named, does not exist
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['whatever.json'])  # default CLI args

    assert IDENT in result.output

    msg = "Input cookiecutter file 'whatever.json' does not exit!!"
    assert msg in result.output

    assert result.exit_code == -5


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'junk.txt'))
def test_no_default_input_file_error_exits(datafiles, runner):
    """
    The default input template file does not exist
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main)  # default CLI args

    assert IDENT in result.output

    msg = "Input cookiecutter file 'cookiecutter.json' does not exit!!"
    assert msg in result.output

    assert result.exit_code == -5


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'minimal-v2.json'))   # noqa
def test_input_file_already_v2_error(datafiles, runner):
    """
    The specified input cookiecutter file is already a v2 file
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['minimal-v2.json'])  # default CLI args

    assert IDENT in result.output

    msg = "Cookiecutter file 'minimal-v2.json' is already a version 2 template!!"   # noqa
    assert msg in result.output

    assert result.exit_code == -6


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'minimal-v2.json'))   # noqa
def test_input_file_already_v2_error_with_verbose(datafiles, runner):
    """
    The specified input cookiecutter file is already a v2 file
    """
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)
    assert inpath == os.getcwd()

    result = runner.invoke(cctconvert.main, ['minimal-v2.json', '--verbose'])  # default CLI args

    assert IDENT in result.output

    msg = "Cookiecutter file 'minimal-v2.json' is already a version 2 template!!"   # noqa
    assert msg in result.output
    assert "('name', 'empty-transformed')" in result.output
    assert "('cookiecutter_version', '2.0.0')" in result.output
    assert "('variables', " in result.output

    assert result.exit_code == -6


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json'))
def test_input_is_empty_json(datafiles, runner):
    """
    Generate an v2 cookiecutter.json file from an empty json file.
    """
    # Make sure pytest-datafiles is working
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)

    cookiecutter = 'empty.json'
    assert os.path.isfile(cookiecutter)

    result = runner.invoke(cctconvert.main, [cookiecutter])

    assert IDENT in result.output

    assert result.exit_code == 0

    # correct output message
    assert cctconvert.VERSION in result.output
    assert "Renaming input file to 'empty.json.v1.bkup" in result.output
    assert "Writing out version 2 cookiecutter template to file 'empty.json'" in result.output      # noqa

    infile_backed_up = 'empty.json.v1.bkup'
    # created backup of original input file
    assert os.path.isfile(infile_backed_up)

    jfout = load_json_file(cookiecutter)
    # {
    #     "name": "empty-transformed",
    #     "cookiecutter_version": "2.0.0",
    #     "_inception": "Transformed by cctconvert 1.0.0 Wed Nov  1 21:56:23 2017",
    #     "variables": []
    # }
    # Check v2 json file
    assert jfout['name'] == 'empty-transformed'
    assert jfout['cookiecutter_version'] == '2.0.0'
    assert jfout['_inception'].startswith("Transformed by ")
    assert len(jfout['variables']) == len([])


def test_version_option_z(runner):
    """
    Test passing -z and getting version IDENT back
    """
    result = runner.invoke(cctconvert.main, ['-z'])
    assert not result.exception
    assert result.exit_code == 0
    assert IDENT in result.output


def test_version_option_version(runner):
    """
    Test passing --version and getting version IDENT back
    """
    result = runner.invoke(cctconvert.main, ['--version'])
    assert not result.exception
    assert result.exit_code == 0
    assert IDENT in result.output


def test_clear_option(mocker, runner):
    """
    Test --clear option by patching click.clear and aserting it was called.

    """
    mock_click_clear = mocker.patch(
        'click.clear',
        autospec=True
    )

    runner.invoke(cctconvert.main, ['--clear'])

    assert mock_click_clear.call_args == mocker.call()


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'empty.json'))
def test_dryrun_option(datafiles, runner):
    """
    Test passing --dryrun. Contexts are dumped, but no v2 file is written.
    """
    # Make sure pytest-datafiles is working
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)

    cookiecutter = 'empty.json'
    assert os.path.isfile(cookiecutter)

    result = runner.invoke(cctconvert.main, [cookiecutter, '--dryrun'])

    assert IDENT in result.output

    assert result.exit_code == 0

    assert "Cookiecutter input 'empty.json' context:" in result.output
    assert "{}" in result.output
    assert "Cookiecutter version 2 context:" in result.output
    assert "('name', 'empty-transformed')" in result.output
    assert "Dry-run: No v2 output file produced." in result.output


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'cookiecutter.json'))   # noqa
def test_full_processing_defaults_no_verbose_option(datafiles, runner):
    """
    Test processing a more complext 'cookiecutter.json' in the current
    directory, no other options. The JSON must contain at least one of each of
    the following variable flavars:
        - a private variable (with an underscore prefixing the variable name)
        - a choices variable
        - a dictionary variable
        - a plain ordinary run-of-the-mill variable
    """
    # Make sure pytest-datafiles is working
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)

    assert os.path.isfile('cookiecutter.json')

    result = runner.invoke(cctconvert.main)
    assert result.exit_code == 0

    assert IDENT in result.output
    assert "Renaming input file to 'cookiecutter.json.v1.bkup'..." in result.output   # noqa
    assert "Writing out version 2 cookiecutter template to file 'cookiecutter.json'" in result.output   # noqa
    assert os.path.isfile('cookiecutter.json.v1.bkup')

    jfout = load_json_file('cookiecutter.json')

    # Check v2 json file
    assert jfout['name'] == 'cookiecutter-transformed'
    assert jfout['cookiecutter_version'] == '2.0.0'
    assert jfout['_inception'].startswith("Transformed by cctconvert " + cctconvert.VERSION)    # noqa
    assert len(jfout['variables']) == 11

    assert jfout['variables'][0]['name'] == 'full_name'
    assert jfout['variables'][0]['default'] == 'Rick Deckard'

    assert jfout['variables'][1]['name'] == 'email'
    assert jfout['variables'][1]['default'] == 'rd@tyrell.com'

    assert jfout['variables'][2]['name'] == 'github_username'
    assert jfout['variables'][2]['default'] == 'rd-tyrell'

    assert jfout['variables'][3]['name'] == 'project_name'
    assert jfout['variables'][3]['default'] == 'Voigt-Kampff Statistics for Greater Los Angeles'   # noqa

    assert jfout['variables'][4]['name'] == 'project_slug'
    assert jfout['variables'][4]['default'] == "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"   # noqa

    assert jfout['variables'][5]['name'] == 'project_short_description'
    assert jfout['variables'][5]['default'] == 'Do Andriods Dream of Electric Sheep?'   # noqa

    assert jfout['variables'][6]['name'] == '_private_key'
    assert jfout['variables'][6]['default'] == '7777'
    assert jfout['variables'][6]['prompt_user'] is False

    assert jfout['variables'][7]['name'] == 'version'
    assert jfout['variables'][7]['default'] == '0.1.0'

    assert jfout['variables'][8]['name'] == 'deploy_to_read_the_docs'
    assert jfout['variables'][8]['default'] == 'y'

    assert jfout['variables'][9]['name'] == 'license'
    assert jfout['variables'][9]['default'] == 'MIT license'
    assert jfout['variables'][9]['choices'] == [
        "MIT license",
        "BSD license",
        "ISC license",
        "Apache Software License 2.0",
        "GNU General Public License v3",
        "Not open source"
    ]

    assert jfout['variables'][10]['name'] == 'file_types'
    assert jfout['variables'][10]['default'] == {
        "png": {
            "name": "Portable Network Graphic",
                    "library": "libpng",
                    "apps": [
                        "GIMP"
                    ]
        },
        "bmp": {
            "name": "Bitmap",
                    "library": "libbmp",
                    "apps": [
                        "Paint",
                        "GIMP"
                    ]
        }
    }


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'cookiecutter.json'))   # noqa
def test_full_processing_default_input_file_verbose_option(datafiles, runner):
    """
    Test processing a more complext 'cookiecutter.json' in the current
    directory, with --verbose option. The JSON must contain at least one of
    each of the following variable flavars:
        - a private variable (with an underscore prefixing the variable name)
        - a choices variable
        - a dictionary variable
        - a plain ordinary run-of-the-mill variable
    """
    # Make sure pytest-datafiles is working
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)

    assert os.path.isfile('cookiecutter.json')

    result = runner.invoke(cctconvert.main, ['--verbose'])
    assert result.exit_code == 0

    assert os.path.isfile('cookiecutter.json.v1.bkup')

    assert IDENT in result.output
    assert "Cookiecutter input 'cookiecutter.json' context:" in result.output
    assert 'full_name : Rick Deckard' in result.output
    assert 'email : rd@tyrell.com' in result.output
    assert 'github_username : rd-tyrell' in result.output
    assert 'project_name : Voigt-Kampff Statistics for Greater Los Angeles' in result.output   # noqa
    assert 'project_slug : "{{ cookiecutter.project_name.lower().replace(\' \', \'_\').replace(\'-\', \'_\') }}" in result.output'    # noqa
    assert 'project_short_description : Do Andriods Dream of Electric Sheep?' in result.output
    assert '_private_key : 7777' in result.output
    assert 'version : 0.1.0' in result.output
    assert 'deploy_to_read_the_docs : y' in result.output
    assert "license : ['MIT license', 'BSD license', 'ISC license', 'Apache Software License 2.0', 'GNU General Public License v3', 'Not open source']" in result.output   # noqa
    assert 'file_types :' in result.output

    assert "Cookiecutter version 2 context:" in result.output

    markers = ['cookiecutter-transformed', 'cookiecutter_version', '2.0.0',
        '_inception', 'Transformed by cctconvert ' + cctconvert.VERSION,
        'full_name', 'Rick Deckard', 'email', 'rd@tyrell.com',
        'github_username', 'rd-tyrell', 'project_name',
        'Voigt-Kampff Statistics for Greater Los Angeles', 'project_slug',
        "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}",  # noqa
        'project_short_description', 'Do Andriods Dream of Electric Sheep?',
        '_private_key', '7777', 'prompt_user', 'False',
        'deploy_to_read_the_docs', 'choices', 'MIT license', 'ISC license',
        'Apache Software License 2.0', 'GNU General Public License v3',
        'Not open source', 'file_types', 'Portable Network Graphic',
        'library', 'libpng', 'GIMP', 'png', 'bmp', 'libbmp', 'apps', 'Paint'
        ]
    for text in markers:
        assert text in result.output

    assert "Renaming input file to 'cookiecutter.json.v1.bkup'..." in result.output   # noqa
    assert "Writing out version 2 cookiecutter template to file 'cookiecutter.json'" in result.output   # noqa

    jfout = load_json_file('cookiecutter.json')

    # Check v2 json file
    assert jfout['name'] == 'cookiecutter-transformed'
    assert jfout['cookiecutter_version'] == '2.0.0'
    assert jfout['_inception'].startswith("Transformed by cctconvert " + cctconvert.VERSION)    # noqa
    assert len(jfout['variables']) == 11

    assert jfout['variables'][0]['name'] == 'full_name'
    assert jfout['variables'][0]['default'] == 'Rick Deckard'

    assert jfout['variables'][1]['name'] == 'email'
    assert jfout['variables'][1]['default'] == 'rd@tyrell.com'

    assert jfout['variables'][2]['name'] == 'github_username'
    assert jfout['variables'][2]['default'] == 'rd-tyrell'

    assert jfout['variables'][3]['name'] == 'project_name'
    assert jfout['variables'][3]['default'] == 'Voigt-Kampff Statistics for Greater Los Angeles'   # noqa

    assert jfout['variables'][4]['name'] == 'project_slug'
    assert jfout['variables'][4]['default'] == "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"   # noqa

    assert jfout['variables'][5]['name'] == 'project_short_description'
    assert jfout['variables'][5]['default'] == 'Do Andriods Dream of Electric Sheep?'   # noqa

    assert jfout['variables'][6]['name'] == '_private_key'
    assert jfout['variables'][6]['default'] == '7777'
    assert jfout['variables'][6]['prompt_user'] is False

    assert jfout['variables'][7]['name'] == 'version'
    assert jfout['variables'][7]['default'] == '0.1.0'

    assert jfout['variables'][8]['name'] == 'deploy_to_read_the_docs'
    assert jfout['variables'][8]['default'] == 'y'

    assert jfout['variables'][9]['name'] == 'license'
    assert jfout['variables'][9]['default'] == 'MIT license'
    assert jfout['variables'][9]['choices'] == [
        "MIT license",
        "BSD license",
        "ISC license",
        "Apache Software License 2.0",
        "GNU General Public License v3",
        "Not open source"
    ]

    assert jfout['variables'][10]['name'] == 'file_types'
    assert jfout['variables'][10]['default'] == {
        "png": {
            "name": "Portable Network Graphic",
                    "library": "libpng",
                    "apps": [
                        "GIMP"
                    ]
        },
        "bmp": {
            "name": "Bitmap",
                    "library": "libbmp",
                    "apps": [
                        "Paint",
                        "GIMP"
                    ]
        }
    }


@pytest.mark.datafiles(os.path.join(TEST_SUPPORT_DIR, 'input', 'cookiecutter.json'))   # noqa
def test_full_processing_with_name_option_and_output_option(datafiles, runner):
    """
    Test processing a more complext 'cookiecutter.json' in the current
    directory, no other options. The JSON must contain at least one of each of
    the following variable flavars:
        - a private variable (with an underscore prefixing the variable name)
        - a choices variable
        - a dictionary variable
        - a plain ordinary run-of-the-mill variable
    """
    # Make sure pytest-datafiles is working
    inpath = str(datafiles)
    assert len(os.listdir(inpath)) == 1

    os.chdir(inpath)

    assert os.path.isfile('cookiecutter.json')

    result = runner.invoke(cctconvert.main, ['--name', 'Sebastian-Template',
                                             '--output', 'cookiecutter-V2.json'
                                             ])
    assert result.exit_code == 0

    assert IDENT in result.output
    assert "Renaming input file to 'cookiecutter.json.v1.bkup'..." not in result.output   # noqa
    assert "Writing out version 2 cookiecutter template to file 'cookiecutter-V2.json'" in result.output   # noqa
    assert os.path.isfile('cookiecutter.json')
    assert os.path.isfile('cookiecutter-v2.json')
    assert len(os.listdir(inpath)) == 2

    jfout = load_json_file('cookiecutter-v2.json')

    # Check v2 json file
    assert jfout['name'] == 'Sebastian-Template'
    assert jfout['cookiecutter_version'] == '2.0.0'
    assert jfout['_inception'].startswith("Transformed by cctconvert " + cctconvert.VERSION)    # noqa
    assert len(jfout['variables']) == 11

    assert jfout['variables'][0]['name'] == 'full_name'
    assert jfout['variables'][0]['default'] == 'Rick Deckard'

    assert jfout['variables'][1]['name'] == 'email'
    assert jfout['variables'][1]['default'] == 'rd@tyrell.com'

    assert jfout['variables'][2]['name'] == 'github_username'
    assert jfout['variables'][2]['default'] == 'rd-tyrell'

    assert jfout['variables'][3]['name'] == 'project_name'
    assert jfout['variables'][3]['default'] == 'Voigt-Kampff Statistics for Greater Los Angeles'   # noqa

    assert jfout['variables'][4]['name'] == 'project_slug'
    assert jfout['variables'][4]['default'] == "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"   # noqa

    assert jfout['variables'][5]['name'] == 'project_short_description'
    assert jfout['variables'][5]['default'] == 'Do Andriods Dream of Electric Sheep?'   # noqa

    assert jfout['variables'][6]['name'] == '_private_key'
    assert jfout['variables'][6]['default'] == '7777'
    assert jfout['variables'][6]['prompt_user'] is False

    assert jfout['variables'][7]['name'] == 'version'
    assert jfout['variables'][7]['default'] == '0.1.0'

    assert jfout['variables'][8]['name'] == 'deploy_to_read_the_docs'
    assert jfout['variables'][8]['default'] == 'y'

    assert jfout['variables'][9]['name'] == 'license'
    assert jfout['variables'][9]['default'] == 'MIT license'
    assert jfout['variables'][9]['choices'] == [
        "MIT license",
        "BSD license",
        "ISC license",
        "Apache Software License 2.0",
        "GNU General Public License v3",
        "Not open source"
    ]

    assert jfout['variables'][10]['name'] == 'file_types'
    assert jfout['variables'][10]['default'] == {
        "png": {
            "name": "Portable Network Graphic",
                    "library": "libpng",
                    "apps": [
                        "GIMP"
                    ]
        },
        "bmp": {
            "name": "Bitmap",
                    "library": "libbmp",
                    "apps": [
                        "Paint",
                        "GIMP"
                    ]
        }
    }
