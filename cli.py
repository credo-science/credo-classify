import argparse
import re
import sys
from argparse import Namespace

from hit_analysis.batch.load_detections import analyse_detections_batch
from hit_analysis.commons.config import Config
from hit_analysis.image.image_utils import detection_load_parser
from hit_analysis.io.csv_write import gen_csv_header, write_to_csv
from hit_analysis.io.load_write import load_objects_from_stream


def main():
    parser = argparse.ArgumentParser(description='Execution CREDO filters without database (only test and PNG/CSV output)')
    parser.add_argument('-d', '--datatype', help='data to import from input: users, devices, teams, hits or pings')
    parser.add_argument('-o', '--out-dir', help='path to store debug data. For hits: png files accepterd, rejected and suspicious (but inserted)', default='')
    parser.add_argument('-i', '--input-file', help='input JSON file, default: stdin', default='-')
    options = parser.parse_args()  # type: Namespace

    datatype = options.datatype
    out_dir = options.out_dir
    input_file = options.input_file

    if datatype != 'hits':
        print('Other datatypes than hits is not supported yet')

    config = Config(out_dir)
    inp = sys.stdin if input_file == '-' else open(input_file, 'r')

    if datatype == 'hits':
        objects = load_objects_from_stream(inp, config, detection_load_parser)
        analyse_detections_batch(objects, config)

        with open('%s/output.csv' % out_dir, 'w', newline='') as csvfile:
            opt = gen_csv_header(objects)
            write_to_csv(csvfile, objects, opt, exclude={'frame_content'}, regex_exclude=[re.compile('image_brighter_count_\\d\\d\\d')])

    if input_file != '-':
        inp.close()


if __name__ == "__main__":
    main()
