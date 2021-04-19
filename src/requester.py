'''
Provide abstract class WebRequester for a general api to execute
textual search request and implementation for google json api.
Method read_key_file will load keys from keyfile.
'''
from pathlib import Path
from pickle import dump, load, HIGHEST_PROTOCOL
from os.path import exists
from googleapiclient.discovery import build, HttpError
from src.spacy_utils import PatternNotFoundException
from src.semantic_sequence import SemanticSequence

SEARCH_REQ_FOLDER = '.searchRequests'  # Savefolder of search results


class AllKeysReachLimit(Exception):
    '''
    Exception for daily search request limit is reached for all keys.
    '''


class WebRequester:
    '''
    Abstract class for a textual search api.
    '''

    def search_for_patter(self, pattern: SemanticSequence, qualia_theorem: str) -> [str]:
        '''
        Will place theorem to clue of used by semantic_seq and
        execute search request.
        :param pattern: semantic_seq with clue to search
        :param qualia_theorem: theorem that will be placed in clue of semantic_seq
        :return: search requests for clue of semantic_seq with theorem
        '''
        raise NotImplementedError('Abstract Class WebRequester has been initiated')

    def num_results(self, search_request: str) -> int:
        '''
        Return number of results for search_request.
        :param search_request request
        :return: number of results for request
        '''
        raise NotImplementedError('Abstract Class WebRequester has been initiated')

    def num_results_near(self, word_1: str, word_2: str) -> int:
        '''
        Return number of results in which word_1 is near to word_2.
        :param word_1: first word
        :param word_2: second word
        :return: number of results for word_1 near word_2
        '''
        raise NotImplementedError('Abstract Class WebRequester has been initiated')

    def num_search_and(self, word_1: str, word_2: str) -> int:
        '''
        Return number of results containing word_1 and word_2.
        :param word_1: first word
        :param word_2: second word
        :return: number of results containing word_1 and word_2
        '''
        raise NotImplementedError('Abstract Class WebRequester has been initiated')


class GoogleRequester(WebRequester):
    '''
    Implementation for the google json api. keys is a list of
    (API key, Custom Search ID) tuples. key_idx reference current
    key pair in list.
    '''

    def __init__(self, keys: [(str, str)]):
        self.keys = keys
        self.key_idx = 0
        self.api_key = self.keys[self.key_idx][0]
        self.cse_key = self.keys[self.key_idx][1]
        self.service = build('customsearch', 'v1', developerKey=self.api_key)

    def search_for_patter(self, pattern: SemanticSequence, qualia_theorem: str) -> [str]:
        search_string = "\"{}\"".format(pattern.get_search_requests(qualia_theorem))
        res = self._get_search_result(search_string)

        found_items = []
        if 'items' in res.keys():
            for item in res['items']:
                for column in ['snippet']:
                    if column in item:
                        found_items.append(item[column])
        return found_items

    def num_results(self, search_request: str):
        res = self._get_search_result(search_request)
        hits = int(res['searchInformation']['totalResults'])
        return hits

    def num_results_near(self, word_1: str, word_2: str):
        return self.num_results('{} AROUND(10) {}'.format(word_1, word_2))

    def num_search_and(self, word_1: str, word_2: str):
        return self.num_results('{} {}'.format(word_1, word_2))

    def _get_search_result(self, search_string: str):
        '''
        Will load search request from SEARCH_REQ_FOLDER if executed in the past
        or execute search request and store results to SEARCH_REQ_FOLDER.
        Automatically use next key from keyfile, if daily limit is reached.
        :param search_string: search request
        :raise AllKeysReachLimit If all combination reach the daily limit of 100
        :return: search results.
        '''

        path = SEARCH_REQ_FOLDER + '/' + search_string

        if exists(path):
            with open(path, 'rb') as file:
                res = load(file)
        else:
            res = None
            while res is None:
                try:
                    res = self.service.cse().list(q=search_string, cx=self.cse_key).execute()
                    with open(path, 'wb') as output:
                        dump(res, output, HIGHEST_PROTOCOL)

                except HttpError as http_error:
                    self._change_key(http_error)
        return res

    def _change_key(self, http_error: HttpError):
        '''
        Increase key_idx to use next key.
        :param http_error: raised by google api client
        :raise AllKeysReachLimit if all keys reached limit
        :return: None
        '''

        self.key_idx += 1
        if self.key_idx > len(self.keys) - 1:
            raise AllKeysReachLimit(http_error)

        self.api_key = self.keys[self.key_idx][0]
        self.cse_key = self.keys[self.key_idx][1]
        self.service = build('customsearch', 'v1', developerKey=self.api_key)


def read_key_file(filepath: Path) -> [(str, str)]:
    '''
    Load key pairs (API key, Custom Search ID) from text file referenced
    by filepath.
    :param filepath: filepath of text file
    :return: list of (API key, Custom Search ID) pairs
    '''
    keys = []

    with open(filepath) as file:
        keys += [tuple(line.split(' ')) for line in file.read().splitlines() if
                 line and not line.startswith('#')]
    if len(keys) == 0:
        raise AttributeError('File {} does not contain keys'.format(filepath))

    return keys
