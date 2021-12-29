from argparse import ArgumentParser
import logging
from pathlib import Path

import pytoml as toml

logger = logging.getLogger()


def set_namespace_for_indices(namespace: str, root_path: str = "rules", **kwargs):
    """
    Iterates across indices within each toml file found in subtree, modifying them to use namespaced indices.
    :param namespace: string namespace to add to index like `logs-*-<slug>*`
    :param root_path: root filesystem path to replace toml data
    :param kwargs:
    :return:
    """
    for file in Path(root_path).rglob("*.toml"):
        with open(file, 'w+') as fb:
            data = toml.load(fb)
            if 'rule' in data and 'index' in data['rule']:
                data['rule']['index'] = list(map(lambda x: transform_index(x, namespace), data['rule']['index']))
            toml.dump(data, file)


def transform_index(index, namespace):
    """
    Transforms a single index to <index>-<namespace>*
    :param index: string describing index pattern
    :param namespace: string describing namespace pattern
    :return: modified index pattern
    """
    if namespace not in index:
        logger.debug(f'Transforming "{index}" to "{index}-{namespace}*"')
        return f'{index}-{namespace}*'
    else:
        return index


def main():
    """
    Main command line function
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("namespace", help='Namespace string to add to index pattern; e.g. logs-*-<namespace>*')
    parser.add_argument("--root_fs", default="rules", help='Path to root rule filesytem')
    args = parser.parse_args()

    set_namespace_for_indices(args.namespace, args.root_fs)


if __name__ == '__main__':
    main()
