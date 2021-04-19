'''
Simple script to parse command line arguments load inflection dict
and create qualia structure.
'''
import argparse
from pathlib import Path

import jsonpickle

from src.requester import AllKeysReachLimit
from src.qualia_structure import WordNotSupportedError, CreationStrategy, DebugQualiaStructure, \
    QualiaStructure, debug_to_normal_structure

GOOGLE_FL = ['g', 'google']
BERT_FL = ['b', 'bert']
MODIFIED_BERT_FL = ['mb', 'modifiedBert']
CREATION_FLAG = 'creation'
DEBUG_FLAG = 'debug'
FILE_FLAG = 'writeToFile'
WORDS = 'words'
INPUT_FILE_FLAG = 'inputFile'
OUTPUT_FLAG = 'output'
TOP_K_FLAG = 'topK'
METRIC_FLAG = 'metric'
KEYS_FLAG = 'keys'
INFLECTION_DICT_FLAG = 'inflectionDict'
METRIC_CHOICES = ['webP', 'webJac', 'webPMI', 'occurrenceInPattern', 'numOfSources']

PARSER = argparse.ArgumentParser(description='Generate qualia structure for given words')
PARSER.add_argument(WORDS, metavar='W', type=str, nargs='*', default=[],
                    help='Qualia theorems')
PARSER.add_argument('-c', '--creation', type=str, default='google',
                    choices=GOOGLE_FL + BERT_FL + MODIFIED_BERT_FL,
                    help='Creation strategy'
                    .format(BERT_FL, MODIFIED_BERT_FL, GOOGLE_FL))

PARSER.add_argument('-i', '--{}'.format(INPUT_FILE_FLAG), type=str, default=None,
                    help='Input file with line separated qualia theorems')
PARSER.add_argument('-w', '--{}'.format(FILE_FLAG), action='store_true',
                    help='Write output to file')
PARSER.add_argument('-o', '--{}'.format(OUTPUT_FLAG), type=str, default='results',
                    help='Output directory for created structures')
PARSER.add_argument('-d', '--debug', action='store_true',
                    help='Print or write additional debug structure with more '
                         'information\'s like metric value and source of extracted element')
PARSER.add_argument('-t', '--{}'.format(TOP_K_FLAG), type=int, default=8,
                    help='Maximal length of qualia roles')
PARSER.add_argument('--{}'.format(INFLECTION_DICT_FLAG), type=str, default='inflectionDict',
                    help='Filepath of lookup table for words which are not inflectable '
                         'by pyinflect')
PARSER.add_argument('-m', '--{}'.format(METRIC_FLAG), type=str, choices=METRIC_CHOICES,
                    default='numOfSources', help='Metric to rank qualia elements')
PARSER.add_argument('-k', '--{}'.format(KEYS_FLAG), type=str, default='apiKeys',
                    help='File with api keys')


def print_or_write_json_to_file(qs_json_str: str, qualia_theorem: str, debug_mode: bool):
    '''
    Print or write json of created qualia structure to file.
    :param qs_json_str: json string of created qualia structure
    :param qualia_theorem: qualia theorem of created structure
    :param debug_mode: true if is json of debug structure else false
    :return: None
    '''
    if write_to_file:
        if creation_arg in BERT_FL:
            model_name = BERT_FL[1]
        elif creation_arg in MODIFIED_BERT_FL:
            model_name = MODIFIED_BERT_FL[1]
        else:
            model_name = GOOGLE_FL[1]

        file_path = '{}/{}_{}{}{}.qs'.format(result_path, qualia_theorem, model_name,
                                             '_' + args[METRIC_FLAG] if model_name
                                                                        in GOOGLE_FL else ''
                                             , '_' + DEBUG_FLAG if debug_mode else '')
        with open(Path(file_path), 'w') as text_file:
            text_file.write(qs_json_str)
    else:
        print(qs_json_str)


def get_creation_strategy() -> CreationStrategy:
    '''
    Load creation strategy which is passed by creation argument.
    :return: None
    '''
    if creation_arg in BERT_FL:

        from src.bert_strategy import BertStrategy

        return BertStrategy(inflection_dict)
    elif creation_arg in MODIFIED_BERT_FL:

        from src.bert_strategy import AdvBertStrategy

        return AdvBertStrategy(inflection_dict)
    else:

        from src.qualia_structure import SearchEngineStrategy
        from src.requester import GoogleRequester, read_key_file
        from src.metrics import WebP, WebJac, WebPMI, NumberOfSources, OccurrenceInRequests

        keys = read_key_file(Path(args[KEYS_FLAG]))

        requester = GoogleRequester(keys)

        if args[METRIC_FLAG] == METRIC_CHOICES[0]:
            metric = WebP(requester)
        elif args[METRIC_FLAG] == METRIC_CHOICES[1]:
            metric = WebJac(requester)
        elif args[METRIC_FLAG] == METRIC_CHOICES[2]:
            metric = WebPMI(requester)
        elif args[METRIC_FLAG] == METRIC_CHOICES[3]:
            metric = OccurrenceInRequests()
        else:
            metric = NumberOfSources()

        return SearchEngineStrategy(inflection_dict, requester=requester, metric=metric)


def load_inflection_dict() -> dict:
    '''
    Load inflection dict from filepath passed by argument --inflectionDict.
    :return: None
    '''
    inf_dict = {}

    if Path(args[INFLECTION_DICT_FLAG]).exists():
        with open(args[INFLECTION_DICT_FLAG]) as inf_file:
            inf_dict = {line.split()[0]: line.split()[1] for line in inf_file.read().splitlines()
                        if
                        line and not line.startswith('#')}

    return inf_dict


def get_qualia_theorems() -> [str]:
    '''
    Load qualia theorems for file passed by -i arg and directly as positional
    args.
    :return: list of qualia theorems
    '''
    qualia_theorems = []

    if args[WORDS] is not None:
        qualia_theorems += args[WORDS]

    input_file = args[INPUT_FILE_FLAG]

    if input_file is not None:
        with open(input_file) as file:
            qualia_theorems += [line for line in file.read().splitlines() if
                                line and not line.startswith('#')]

    return qualia_theorems


if __name__ == '__main__':
    args = vars(PARSER.parse_args())

    result_path = args[OUTPUT_FLAG]

    Path(result_path).mkdir(parents=True, exist_ok=True)

    creation_arg = args[CREATION_FLAG]
    is_debug_mode = args[DEBUG_FLAG]
    write_to_file = args[FILE_FLAG]

    inflection_dict = load_inflection_dict()
    creation_strategy = get_creation_strategy()
    assert isinstance(creation_strategy, CreationStrategy)

    for qt in get_qualia_theorems():
        try:
            debug_qualia_structure = creation_strategy.generate_qualia_structure(qt)
            assert isinstance(debug_qualia_structure, DebugQualiaStructure)
            if is_debug_mode:
                json_str = jsonpickle.encode(debug_qualia_structure, indent=4, unpicklable=True)
                print_or_write_json_to_file(json_str, qt, True)

            qualia_structure = debug_to_normal_structure(debug_qualia_structure, args[TOP_K_FLAG])
            assert isinstance(qualia_structure, QualiaStructure)
            json_str = jsonpickle.encode(qualia_structure, indent=4, unpicklable=True)
            print_or_write_json_to_file(json_str, qt, False)

        except AllKeysReachLimit:
            print('Qualia Structure of {} failed, because '
                  'the maximal requests of all keys is reached'.format(qt))
        except WordNotSupportedError as word_not_supported_error:
            print(word_not_supported_error)
