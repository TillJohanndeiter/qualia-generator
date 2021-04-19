'''
Provide creation of qualia structure by using the language model BERT.
'''

import string

import tensorflow as tf
import numpy as np
import jsonpickle
from tensorflow.python.keras.layers import Softmax
from transformers import BertTokenizer, TFBertForMaskedLM

from src.spacy_utils import LANG_MODEL, PatternNotFoundException
from src.semantic_sequence import SemanticSequence, MASK
from src.qualia_structure import CreationStrategy, QualiaElement, DebugQualiaStructure, Role

from spacy.lang.en.stop_words import STOP_WORDS

NAME_OF_MODEL = 'bert-base-cased'
tokenizer = BertTokenizer.from_pretrained(NAME_OF_MODEL)
MODEL = TFBertForMaskedLM.from_pretrained(NAME_OF_MODEL, return_dict=True)


class NumpyFloatHandler(jsonpickle.handlers.BaseHandler):
    '''
    Handler to convert numpy floats to string. Otherwise would be printed
    as None.
    '''

    def flatten(self, obj, data):
        return str(obj)


jsonpickle.handlers.registry.register(np.float, NumpyFloatHandler)
jsonpickle.handlers.registry.register(np.float32, NumpyFloatHandler)
jsonpickle.handlers.registry.register(np.float64, NumpyFloatHandler)


def clean_up_pred(pred: [str]) -> str:
    '''
    Clean prediction by joining sequence, replace punctuation and stript words
    :param pred: predicted words by bert
    :return: cleaned prediction
    '''
    cleaned_pred = ' '.join(pred)
    for character in string.punctuation:
        cleaned_pred = cleaned_pred.replace(character, '')
    cleaned_pred = cleaned_pred.strip()
    return cleaned_pred


def _append_invalid_predictions(invalid_predictions: [], sem_seq: SemanticSequence,
                                role: Role, bert_text: str):
    '''
    Append all elements of invalid_predictions to role.pattern_to_not_resolved[sem_seq].
    :param invalid_predictions: invalid predictions
    :param sem_seq: sem_seq of bert input
    :param role: role of sem_seq
    :param bert_text: input for bert
    :return: None
    '''
    for pred_words, probability in invalid_predictions:
        temp = bert_text
        for pred_word in pred_words:
            temp = temp.replace(MASK, pred_word)

        role.pattern_to_not_resolved[sem_seq].append('[CLS] ' + temp + '. [SEP]')


def _append_valid_prediction(valid_pred: [], qe_to_prob: dict, qe_to_mask: dict,
                             bert_text: str):
    '''
    Append all lemmatized elements in valid_pred to qe_to_mask[prediction]. Also
    set probability to qe_to_prob.
    :param valid_pred: list of valid predictions
    :param qe_to_prob: dictionary to map qe to maximal probabilities
    :param qe_to_mask: dictionary to map qe to bert input
    :param bert_text: bert text used as input
    :return: None
    '''
    for prediction, prob in valid_pred:

        prediction = clean_up_pred(prediction)
        prediction = ' '.join([token.lemma_ for token in LANG_MODEL(prediction)])

        if prediction not in qe_to_prob:
            qe_to_prob[prediction] = prob

        qe_to_prob[prediction] = max(qe_to_prob[prediction], prob)

        if prediction not in qe_to_mask:
            qe_to_mask[prediction] = []
        qe_to_mask[prediction].append('[CLS] ' + bert_text + '. [SEP]')


class BertStrategy(CreationStrategy):
    '''
    Strategy for using word prediction of BERT to generate qualia elements.
    '''

    def __init__(self, inflection_dict: dict):
        super().__init__(inflection_dict)

    def is_valid_prediction(self, theorem: str, pred: [str], sem_seq: SemanticSequence,
                            bert_text: str):
        '''
        Validate Prediction
        :param sem_seq: sematical sequence of bert_text
        :param theorem: theorem of created structure
        :param pred: prediction
        :param bert_text: input sequence for bert 
        :return: 
        '''
        return not (theorem in pred
                    or len(clean_up_pred(pred)) <= 1
                    or any(i.lower() in STOP_WORDS for i in pred)
                    or any(i.lower() in string.punctuation for i in pred))

    def generate_qualia_structure(self, qualia_theorem: str):
        '''
        Generate qualia structure for qualia theorem by using
        bert word prediction.
        :param qualia_theorem: qualia theorem of creat
        :return: DebugQualiaStructure of qualia_theorem
        '''
        qualia_structure = DebugQualiaStructure(qualia_theorem)

        for role in qualia_structure.all_roles:
            sem_seq_to_qe = dict()
            for sem_seq in role.get_all_pattern():

                sem_seq_to_qe[sem_seq] = []

                prob_of_qe, qe_to_mask = self.__extract_elements(qualia_theorem, sem_seq, role)

                for element in qe_to_mask:
                    qualia_element = QualiaElement(word=element.lower(),
                                                   metric_value=prob_of_qe[element],
                                                   sources=qe_to_mask[element])
                    sem_seq_to_qe[sem_seq].append(qualia_element)

            role.sem_seq_to_qe = sem_seq_to_qe

        return qualia_structure

    def _predict_masks(self, bert_text: str) -> ([str], float):
        '''
        Predict masked tokens in bert_text
        :param bert_text: input sequence for bert
        :return: Top k prediction for input sequence
        '''

        tokenized_text = tokenizer.tokenize('[CLS] ' + bert_text + '. [SEP]')
        input_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
        outputs = MODEL(tf.convert_to_tensor([input_ids]))
        mask_idx = tokenized_text.index(MASK)
        top_k_output = tf.math.top_k(outputs.logits[0][mask_idx], k=50, sorted=True, name=None)
        probabilities = Softmax()(top_k_output.values.numpy()).numpy()

        top_k_pred = [([word], prob) for word, prob in
                      zip(tokenizer.convert_ids_to_tokens(top_k_output.indices), probabilities)]

        if tokenized_text.count(MASK) > 1:
            for top_k in top_k_pred.copy():
                top_k_pred.remove(top_k)

                pred = top_k[0]
                pred_for_last_mask = pred[-1]
                results_of_next_pred = self._predict_masks(bert_text.replace(MASK,
                                                                             pred_for_last_mask,
                                                                             1))
                for pred_for_next_mask, prob in results_of_next_pred:
                    top_k_pred.append((pred + pred_for_next_mask, prob))

            return top_k_pred

        return top_k_pred

    def __extract_elements(self, theorem: str, sem_seq: SemanticSequence, role: Role) \
            -> (dict, dict):
        '''
        Extract predicted elements for the sem_seq and return dictionaries with
        probabilities for
        :param theorem: Qualia theorem of created structure
        :param sem_seq:
        :param role: role of sem_seq
        :return:
        '''

        sing, plu = self.inflect_sing_plural(theorem)
        tense = plu if sem_seq.is_plural else sing

        qe_to_mask = dict()
        qe_to_prob = dict()

        for bert_text in sem_seq.get_bert_input(tense):
            predictions = self._predict_masks(bert_text)
            valid_pred = [(pred, p) for pred, p in predictions
                          if self.is_valid_prediction(tense, pred, sem_seq, bert_text)]
            invalid_pred = [pred for pred in predictions if pred not in valid_pred]

            _append_invalid_predictions(invalid_pred, sem_seq, role, bert_text)
            _append_valid_prediction(valid_pred, qe_to_prob, qe_to_mask, bert_text)
        return qe_to_prob, qe_to_mask


class AdvBertStrategy(BertStrategy):
    '''
    Strategy for using word prediction of BERT to generate qualia elements and fitler
    prediction by using the extraction pattern of the sem_seq.
    '''

    def is_valid_prediction(self, theorem: str, pred: [str], sem_seq: SemanticSequence,
                            bert_text: str):
        '''
        Validate a prediction by replacing the prediction into the bert text. The extraction
        pattern will be applied on the result. If the extracted Token are the prediction then
        the prediction is valid.
        :param sem_seq: semantically sequence of bert_text
        :param theorem: theorem of the created qualia structure
        :param bert_text: input for bert
        :return:
        '''

        if not super(AdvBertStrategy, self).is_valid_prediction(theorem, pred, sem_seq,
                                                                bert_text):
            return False

        for pred_word in pred:
            bert_text = bert_text.replace(MASK, pred_word, 1)
        try:
            extracted_element = sem_seq.extract_qualia_elements(theorem, bert_text)
            extracted_element = [token.orth_.strip() for token in extracted_element[0]]
            return pred == extracted_element
        except PatternNotFoundException:
            return False
