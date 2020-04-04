from sys import stdin

from django.core.management import BaseCommand

from hit_analysis.batch.load_detections import analyse_detections_batch
from hit_analysis.commons.config import Config
from hit_analysis.image.image_utils import detection_load_parser
from hit_analysis.io.load_write import load_objects_from_stream


class Command(BaseCommand):
    help = 'Create and initialize admin user and init build-in attributes'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--datatype', help='data to import from input: users, devices, teams, hits or pings')
        parser.add_argument('-o', '--out-dir', help='path to store debug data. For hits: png files accepterd, rejected and suspicious (but inserted)', default='')
        parser.add_argument('-i', '--input-file', help='input JSON file, default: stdin', default='-')

    def handle(self, *args, **options):
        datatype = options['datatype']
        out_dir = options['out_dir']
        input_file = options['input_file']

        if datatype != 'hits':
            print('Other datatypes than hits is not supported yet')

        config = Config(out_dir)
        inp = stdin if input_file == '-' else open(input_file, 'r')

        if datatype == 'hits':
            objects = load_objects_from_stream(inp, config, detection_load_parser)
            analyse_detections_batch(objects, config)

        if input_file != '-':
            inp.close()
