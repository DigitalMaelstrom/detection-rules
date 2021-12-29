from argparse import ArgumentParser
import dataclasses as dc
import logging
from pathlib import Path
import sys
from typing import List

this_path = Path().resolve()
package_path = Path(*this_path.parts[:this_path.parts.index('detection-rules')+1])
sys.path.append(str(package_path))

from detection_rules.rule import QueryRuleData, TOMLRule
from detection_rules.rule_loader import RuleCollection

logger = logging.getLogger()


def set_namespace_for_indices(namespace: str, root_path: str = "rules", backup=False, **kwargs):
    """
    Iterates across indices within each toml file found in subtree, modifying them to use namespaced indices.
    :param namespace: string namespace to add to index like `logs-*-<slug>*`
    :param root_path: root filesystem path to replace toml data
    :param kwargs:
    :return:
    """
    for rule in RuleCollection.default():
        if isinstance(rule.contents.data, QueryRuleData):
            replacement_rule = replace_index_field(rule,
                                                   list(map(lambda x: transform_index(x, namespace),
                                                            rule.contents.data.index)))
            replacement_rule.save_toml()


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


# rule.contents.data.index
def replace_index_field(rule: TOMLRule, value: List[str]):
    data = dc.replace(rule.contents.data, index=value)
    contents = dc.replace(rule.contents, data=data)
    rule = dc.replace(rule, contents=contents)
    return rule


def main():
    """
    Main command line function
    :return:
    """
    parser = ArgumentParser()
    parser.add_argument("namespace", help='Namespace string to add to index pattern; e.g. logs-*-<namespace>*')
    parser.add_argument("--root_fs", default="rules", help='Path to root rule filesytem')
    parser.add_argument("--backup", action='store_true', default=False, help='Modify rules after backing up originals')
    args = parser.parse_args()

    set_namespace_for_indices(args.namespace, root_path=args.root_fs, backup=args.backup)


if __name__ == '__main__':
    main()
