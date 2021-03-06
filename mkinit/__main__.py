def main():
    from mkinit import static_mkinit
    import textwrap
    import argparse
    import logging
    description = textwrap.dedent(
        '''
        discover and run doctests within a python package

        Respects the varaibles:
            `__submodules__`, `__explicit__`, `__protected__`, `__private__`
        ''').strip('\n')

    parser = argparse.ArgumentParser(prog='python -m mkinit', description=description)
    parser.add_argument('modname_or_path', nargs='?', help='module or path to generate __init__.py for', default='.')

    parser.add_argument('--dry', dest='_dry_old', action='store_true', default=True)

    parser.add_argument(*('-i', '-w', '--write', '--inplace'),
                        dest='dry', action='store_false',
                        help='modify / write to the file inplace',
                        default=True)

    parser.add_argument('--noattrs',
                        dest='with_attrs', action='store_false', default=True,
                        help='Do not generate attribute from imports')
    parser.add_argument('--nomods',
                        dest='with_mods', action='store_false', default=True,
                        help='Do not generate modules imports')
    parser.add_argument('--noall',
                        dest='with_all', action='store_false', default=True,
                        help='Do not generate an __all__ variable')

    parser.add_argument('--relative',
                        action='store_true', default=False,
                        help='Use relative . imports instead of <modname>')

    parser.add_argument('--norespect_all',
                        dest='respect_all',
                        action='store_false', default=True,
                        help='if False does not respect __all__ attributes of submodules when parsing')

    parser.add_argument('--verbose', nargs='?', default=0, type=int,
                        help='Verbosity level')

    parser.add_argument('--version', action='store_true',
                        help='print version and exit')

    args, unknown = parser.parse_known_args()
    ns = args.__dict__.copy()

    if ns['version']:
        import mkinit
        print(mkinit.__version__)
        return

    modname_or_path = ns['modname_or_path']
    if ns['verbose'] is None:
        ns['verbose'] = 1

    respect_all = ns['respect_all']
    verbose = ns['verbose']
    dry = ns['dry']

    # Formatting options
    options = {
        'with_attrs': ns['with_attrs'],
        'with_mods': ns['with_mods'],
        'with_all': ns['with_all'],
        'relative': ns['relative'],
    }

    if verbose == 0:
        level = logging.WARNING
    elif verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=level,
    )

    static_mkinit.autogen_init(modname_or_path, respect_all=respect_all,
                               options=options, dry=dry)

if __name__ == '__main__':
    main()
