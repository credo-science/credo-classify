from typing import List, TextIO

from json import loads
from io import StringIO

from hit_analysis.commons.config import Config


def load_objects_from_stream(_input: TextIO, config: Config) -> List[dict]:
    ret = []
    timing2 = timing = config.print_log('Parsing objects from JSON provided in STDIN...')
    count = 0

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
                    ret.append(loads(buff.getvalue()))
                    buff.close()
                    buff = None
                    stage = 1

                    count += 1
                    if count % 10000 == 0:
                        timing2 = config.print_log('... just parsed %d objects...' % count, timing2)
                else:
                    buff.write(a)

    config.print_log('... done, the %d objects was parsed' % count, timing)
    return ret


def load_objects_from_str(s: str, config: Config) -> List[dict]:
    return load_objects_from_stream(StringIO(s), config)
