# -*- coding: utf-8 -*-

"""
cctconvert

A Cookiecutter Template Transformer Utility
-------------------------------------------
Convert a version 1 cookiecutter.json file into a version 2 file.

The only external dependency required is:

    pip install click

For the User Manual:

    python cctconvert.py --help

or if its been installed:

    cctconvert --help

"""
import os
import sys
import json
import pprint
from datetime import datetime

from collections import OrderedDict

import click

# ----------------------------------------------------------------------------
# VERSION = '1.0.0'  # Initial release
VERSION = '1.0.1'  # Added -no-incept option

IDENT = 'cctconvert ' + VERSION

V1_BACKUP_EXT = '.v1.bkup'

SET_OF_REQUIRED_FIELDS = {
    'name',
    'cookiecutter_version',
    'variables',
}


def context_is_version_2(cookiecutter_context):
    """
    Return True if the cookiecutter_context meets the current requirements for
    a version 2 cookiecutter.json file format.
    """
    # This really is not sufficient since a v1 context could define each of
    # these fields; perhaps a more thorough test would be to also check if the
    # 'variables' field was defined as a list of OrderedDict items.
    if (cookiecutter_context.keys() &
            SET_OF_REQUIRED_FIELDS) == SET_OF_REQUIRED_FIELDS:
        return True
    else:
        return False


def cc_read(cookiecutter_template_file):
    """
    Load the JSON file named cookiecutter_template_file into a Python context
    object and return it.
    """
    try:
        with open(cookiecutter_template_file, 'r', encoding='utf8') as cc:
            ctx = json.load(cc, object_pairs_hook=OrderedDict)
    except Exception as e:
        error("Exception: Unable to load cookiecutter file '{ccf}'".format(ccf=cookiecutter_template_file))  # noqa
        click.echo(str(e))
        sys.exit(-1)

    return ctx


def cc_write(context, output_file_name):
    """
    Given a Python object context and an output filename,
    write out a JSON file.
    """
    click.echo("Writing out version 2 cookiecutter template to file '{v2f}'".format(v2f=output_file_name))  # noqa
    try:
        with open(output_file_name, encoding='utf8', mode='w') as cc:
            json.dump(context, cc, indent=4)

    except Exception as e:
        error("Exception: Unable to write cookiecutter file '{ccf}'".format(ccf=output_file_name))  # noqa
        click.echo(str(e))
        sys.exit(-2)


def error(msg):
    """
    Turn msg red. Thank you click.
    """
    click.echo(click.style(msg, fg='red'))


def kvpair(key, val):
    """
    Color-ify a key/value pair.
    """
    k = click.style("{k}".format(k=key), fg='yellow')
    v = click.style("{v}".format(v=val), fg='green')
    click.echo('  ' + k + ' : ' + v)


def resolve_output_filename(input_file_name, output_file_name):
    """
    If output_file_name is not specified, then rename the input file to a
    version 1 backup file name, and use the input file name for the new
    output file name. If any file name already exists, exit with an error.
    """
    if output_file_name is None:
        # No --output FILE on the command line
        # Handle rename of input_file_name
        new_input_file_name = input_file_name + V1_BACKUP_EXT
        if os.path.exists(new_input_file_name):
            msg = "ERROR: Input file '{ifn}' cannot be renamed to '{nifn}' because that file already exists!!"  # noqa
            error(msg.format(ifn=input_file_name, nifn=new_input_file_name))
            sys.exit(-3)
        else:
            click.echo("Renaming input file to '{nifn}'...".format(nifn=new_input_file_name))  # noqa
            os.rename(input_file_name, new_input_file_name)
            # Now input filename is available for use
            output_file_name = input_file_name

    if os.path.exists(output_file_name):
        msg = "ERROR: Output file '{ofn}' already exists!!"
        error(msg.format(ofn=output_file_name))
        click.echo("Change the output filename via option --output-file or delete it")   # noqa
        sys.exit(-4)

    return output_file_name

# ----------------------------------------------------------------------------


def convert(cookiecutter, verbose, name, version, dryrun, output, clear, no_incept):   # noqa
    """
    Converts cookiecutter (version 1) file to a version 2 file.

    See main's args below for parameter definitions.
    """
    ident = '{me} {tickdock}'.format(
        me=IDENT,
        tickdock=datetime.now().strftime('%c')
    )

    click.echo(ident)
    if version:
        return 0

    if clear:
        click.clear()

    width, _ = click.get_terminal_size()
    fence = '-' * (width - 5)

    # ------------------------------------------------------------------------
    if dryrun:
        verbose = True

    if not os.path.exists(cookiecutter):
        error("Input cookiecutter file '{icf}' does not exit!!".format(icf=cookiecutter))  # noqa
        return -5

    ctx = cc_read(cookiecutter)

    if context_is_version_2(ctx):
        error("Cookiecutter file '{ccf}' is already a version 2 template!!".format(ccf=cookiecutter))  # noqa
        if verbose:
            click.echo(pprint.pformat(ctx, indent=4, width=width - 5))
        return -6

    if name is None:
        # Not specified on command line via --name TEXT option
        # Derive a name from the input file name
        name = os.path.splitext(os.path.basename(cookiecutter))[0]
        name = name + '-transformed'

    if no_incept:
        ctx_v2 = OrderedDict([
            ('name', name),
            ('cookiecutter_version', '2.0.0'),
            ('variables', []),
        ])
    else:
        ctx_v2 = OrderedDict([
            ('name', name),
            ('cookiecutter_version', '2.0.0'),
            ('_inception', 'Transformed by ' + ident),
            ('variables', []),
        ])

    if verbose:
        click.echo("Cookiecutter input '{ccf}' context:".format(ccf=cookiecutter))  # noqa
    v = None
    for k in ctx.keys():
        v = ctx[k]
        if verbose:
            kvpair(k, v)
        if isinstance(v, list):
            ctx_v2['variables'].append(OrderedDict([('name', k), ('default', v[0]), ('choices', v)]))  # noqa
        elif k.startswith('_'):
            # private variable, do not prompt user
            ctx_v2['variables'].append(OrderedDict([('name', k), ('default', v), ('prompt_user', False)]))  # noqa
        else:
            ctx_v2['variables'].append(OrderedDict([('name', k), ('default', v)]))  # noqa
    if v is None:
        # Empty input file
        click.echo('{}')

    if verbose:
        click.echo(fence)
        click.echo("Cookiecutter version 2 context:")
        click.echo(pprint.pformat(ctx_v2, indent=4, width=width - 5))
        click.echo(fence)

    if not dryrun:
        outfile = resolve_output_filename(
            input_file_name=cookiecutter,
            output_file_name=output)

        cc_write(ctx_v2, outfile)
    else:
        click.echo("Dry-run: No v2 output file produced.")

    return 0

# ----------------------------------------------------------------------------


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument(
    'cookiecutter',
    # type=click.Path(exists=True),
    default='cookiecutter.json')
@click.option(
    '--verbose', '-v', is_flag=True, default=False,
    help='Emit input context and emit output context during the transform')
@click.option(
    '--name', '-n', default=None,
    help='Name of template in v2 template header. If not specified, a name will be derived from COOKIECUTTER file name.')  # noqa
@click.option(
    '--version', '-z', is_flag=True, default=False,
    help='Emit identity information and exit')
@click.option(
    '--dryrun', '-d', is_flag=True, default=False,
    help='Do not change the file system, but display input context & generated output context')  # noqa
@click.option(
    '--output', '-o', default=None, metavar='FILE',
    help='File name of the version 2 template file being generated.')
@click.option(
    '--clear', '-c', is_flag=True, default=False,
    help='Clear that cluttered terminal screen before running.')
@click.option(
    '--no-incept', '-i', is_flag=True, default=False,
    help='Suppress writing the private _inception field to the version 2 template header')   # noqa
def main(cookiecutter, verbose, name, version, dryrun, output, clear, no_incept):
    """\b
    Transform a version 1 COOKIECUTTER file into a version 2 file.
    Default COOKIECUTTER file is 'cookiecutter.json' in current directory.

    This transform/conversion will NEVER delete a file.

    The default behavior will attempt to backup the input version 1
    cookiecutter file by renaming it with a backup extension and then
    using the original input name for the newly transformed version 2
    cookiecutter file.

    To leave the input file name unaffected, specify a version 2 template
    output name to be generated via the --output FILE option.

    If a file is found to already exits, either during the renaming of the
    input file, or the writing of the output file, an abort of the transform
    will occur and the user will be responsible for correcting the error.
    """
    sys.exit(convert(cookiecutter, verbose, name, version, dryrun, output, clear, no_incept))    # noqa


# ----------------------------------------------------------------------------
if __name__ == '__main__':  # pragma: no cover
    main()
