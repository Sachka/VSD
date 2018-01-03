# coding: UTF8
"""
TESTS
"""
from corpus import conll_list
from vsd import base_surrounding_words

EXO = "data_WSD_VS/example.conll"
EXO2 = "data_WSD_VS/affecter.deep_and_surf.sensetagged.conll"
EL = conll_list(EXO)
EL2 = conll_list(EXO2)

w_feat = base_surrounding_words(EL2, "affecter")
print(EL)
print(w_feat)
