# coding: UTF-8
from corpus import index_embeddings


WE = "data_WSD_VS/vecs100-linear-frwiki"

em = index_embeddings(WE)
print(len(em))
print(em["le"])
