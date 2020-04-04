from typing import List, TextIO, Callable, Optional

from json import loads
from io import StringIO

from hit_analysis.commons.config import Config


def load_objects_from_stream(_input: TextIO, config: Config, parser: Optional[Callable[[dict], bool]] = None) -> List[dict]:
    """
    Extract objects from array in JSON.
    :param _input: input text stream
    :param config: using config.print_log
    :param parser: optional parses and filter method, when return False then not be added
    :return: list of objects
    """
    ret = []
    timing2 = timing = config.print_log('Parsing objects from JSON provided in STDIN...')
    count = 0
    skip = 0

    stage = 0
    buff = None
    for line in _input:
        for a in line:
            if stage == 0:
                if a == '[':
                    stage = 1
                    continue  # and read next character
            if stage == 1:
                if a == ']':
                    break
                if a == '{':
                    buff = StringIO()
                    stage = 2  # and continue parsing this character in stage 2
            if stage == 2:
                if a == '}':
                    buff.write(a)
                    o = loads(buff.getvalue())
                    if parser is None or parser(o):
                        ret.append(o)
                        count += 1
                    else:
                        skip += 1
                    buff.close()
                    buff = None
                    stage = 1

                    if (count + skip) % 10000 == 0:
                        timing2 = config.print_log('... just parsed %d and skip %d objects...' % (count + skip, skip), timing2)
                else:
                    buff.write(a)

    config.print_log('... done, the %d objects was parsed' % count, timing)
    return ret


def load_objects_from_str(s: str, config: Config) -> List[dict]:
    """
    Extract objects from array in JSON.
    :param s: JSON in string
    :param config: using config.print_log
    :return: list of objects
    """
    return load_objects_from_stream(StringIO(s), config)


def load_objects(source: str or TextIO, config: Config) -> List[dict]:
    """
    Extract objects from array in JSON.
    :param source: JSON in string or in text stream
    :param config: using config.print_log
    :return: list of objects
    """
    if isinstance(source, str):
        return load_objects_from_str(source, config)
    else:
        return load_objects_from_stream(source, config)
