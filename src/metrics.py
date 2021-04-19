'''
Provide all metrics that are use to rank qualia elements.
'''
from itertools import chain
from math import log
from src.requester import WebRequester

MAX_PAGES = 25270000000  # Maximum of search Results


class OccurrenceMetric:
    '''
    Abstract class for metric, which use generated text artefacts.
    '''

    def calc_metric_value(self, db_qualia_element, debug_role) -> float:
        '''
        Calculate metric value of db_qualia_element in role.
        :param db_qualia_element: debug qualia element for which a metric
        value will be calculated
        :param debug_role: role of the qualia element
        :return: metric value of db_qualia_element
        '''
        raise NotImplementedError('Abstract Class OccurrenceMetric has been initiated')


class NumberOfSources(OccurrenceMetric):
    '''
    Calculate metric value by number of sources/search results from which
    the qualia element was extracted.
    '''

    def calc_metric_value(self, db_qualia_element, debug_role) -> float:
        qualia_elements_of_roles = chain.from_iterable(
            debug_role.sem_seq_to_qe.values())

        return sum(len(d_q_e.sources) for d_q_e in
                   [d_q_e for d_q_e in qualia_elements_of_roles if d_q_e == db_qualia_element])


class OccurrenceInRequests(OccurrenceMetric):
    '''
    Calculate metric value by number of semantic_seq which extracted
    the qualia element.
    '''

    def calc_metric_value(self, db_qualia_element, db_role) -> float:
        qualia_elements_for_roles = chain.from_iterable(
            db_role.sem_seq_to_qe.values())

        return len([d_q_e for d_q_e in qualia_elements_for_roles
                    if d_q_e == db_qualia_element])


class WebBasedMetric:
    '''
    Abstract class for metrics which use the relation between the number of
    search results to approximate probability distribution. To execute
    search requests an instance of WebRequester is used.L
    '''

    def __init__(self, web_requester: WebRequester):
        self.web_requester = web_requester

    def calc_metric_value(self, qualia_element: str, qualia_theorem: str):
        '''
        Calculate metric value by using the relation between the results of multiple
        search requests.
        :param qualia_element: string of qualia element
        :param qualia_theorem: string of qualia theorem
        :return: metric value for qualia element
        '''

        raise NotImplementedError('Abstract Class WebBasedMetric has been initiated')


class WebJac(WebBasedMetric):

    def calc_metric_value(self, qualia_element: str, qualia_theorem: str) -> float:
        '''
        Calculate metric value by approximate P(qualia_element | theorem)
        / (P(qualia_element) + P(theorem) -  P(qualia_element, theorem)).
        :param qualia_element: string of qualia element
        :param qualia_theorem: string of qualia theorem
        :return: metric value for qualia element
        '''
        return self.web_requester.num_results_near(qualia_element, qualia_theorem) \
               / (self.web_requester.num_results(qualia_element)
                  + self.web_requester.num_results(qualia_theorem)
                  - self.web_requester.num_search_and(qualia_element, qualia_theorem))


class WebPMI(WebBasedMetric):

    def calc_metric_value(self, qualia_element: str, qualia_theorem: str) -> float:
        temp = self.web_requester.num_search_and(qualia_element, qualia_theorem) * MAX_PAGES / \
               (self.web_requester.num_results(qualia_element)
                * self.web_requester.num_results(qualia_theorem))

        return 0 if temp == 0 else log(temp, 2)


class WebP(WebBasedMetric):

    def calc_metric_value(self, qualia_element: str, qualia_theorem: str):
        '''
        Calculate metric value by approximate P(qualia_element | theorem)
        :param qualia_element: string of qualia element
        :param qualia_theorem: string of qualia theorem
        :return: metric value for qualia element
        '''

        return self.web_requester.num_results_near(qualia_element, qualia_theorem) / \
               self.web_requester.num_results(qualia_theorem)
