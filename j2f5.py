# -*- coding: utf-8 -*-
import sys
from os import path
from argparse import ArgumentError
from j2cli import main as j2cli_main

"""
support reading templating start/end strings from the user supplied configuration
alter_context is called before j2_environment_params:
1. Read and save context (based on user supplied configuration) in alter_context
2. Read start/end strings from context in j2_environment_params
https://github.com/kolypto/j2cli/blob/26a67e9419d96b7f92871e8b93dba00306c5df0b/j2cli/cli.py#L183-L186
"""

_context = dict()

# constants
_TEMPLATING_NAMESPACE = "templating_settings"


def ansible_filters():

    _ansible_filters = dict()

    try:
        from ansible.plugins.filter import core as ansible_core_filters
        from ansible.plugins.filter import urls as ansible_urls_filters
        from ansible.plugins.filter import urlsplit as ansible_urlsplit_filters
        from ansible.plugins.filter import mathstuff as ansible_mathstuff_filters

        _ansible_filters.update(ansible_core_filters.FilterModule().filters())
        _ansible_filters.update(ansible_urls_filters.FilterModule().filters())
        _ansible_filters.update(ansible_urlsplit_filters.FilterModule().filters())
        _ansible_filters.update(ansible_mathstuff_filters.FilterModule().filters())
    except ImportError:
        pass

    return _ansible_filters


def alter_context(context):
    """modify jinja2 context"""
    # register context in _context for later use in j2_environment_params
    global _context
    _context = context

    # start other modifications below
    return context


def extra_filters():
    """extra jinja2 filters"""
    _extra_filters = dict()

    # load ansible filters when ansible is available
    _extra_filters.update(ansible_filters())

    return _extra_filters


def j2_environment_params():
    """jinja2 environment parameters"""

    custom_params = dict(
        # use this dict to further customize or overwrite params
    )

    # read templating parameters from _context
    templating_params = dict(
        # Custom block start/end strings
        block_start_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "block_start_string"
        ),
        block_end_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "block_end_string"
        ),
        # Custom variable start/end strings
        variable_start_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "variable_start_string"
        ),
        variable_end_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "variable_end_string"
        ),
        # Custom comment start/end strings
        comment_start_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "comment_start_string"
        ),
        comment_end_string=_context.get(_TEMPLATING_NAMESPACE, {}).get(
            "comment_end_string"
        ),
        # Remove whitespace around blocks
        trim_blocks=True,
        lstrip_blocks=True,
        # Keep \n at the end of a file
        keep_trailing_newline=True,
    )
    # remove None's
    templating_params = {k: v for (k, v) in templating_params.items() if v is not None}

    templating_params.update(custom_params)
    return templating_params


def main():
    """wrap j2 command line and automatically add j2f5.py via --customize"""
    if "--customize" in sys.argv:
        raise ArgumentError(
            None,
            "j2f5 sets --customize, hence it is not allowed as an argument. Use j2 directly to use your own customization.",
        )

    # inject args which will be read by j2cli main()
    sys.argv.insert(1, "--customize")
    sys.argv.insert(2, path.abspath(__file__))
    j2cli_main()


if __name__ == "__main__":
    main()
