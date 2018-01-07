# coding: UTF-8
"""
NEURAL NETWORK MODEL
"""
import numpy as np
from keras.utils import to_categorical
from keras.preprocessing import text
from corpus_reading import conll_list, read_embeddings
from feature_extraction import feature_extraction


def encode_features(raw_features, embeddings_file):
    """
    types: (list) -> list
    structure: ("raw features") -> "encoded features"
    """
    encoded_features = []
    embeddings_index = read_embeddings(embeddings_file)
    # We obtain a list of possible tags for dependency trees

    def cat_list(tag_list):
        out = []
        if isinstance(tag_list[0], list):
            for sublist in tag_list:
                for element in sublist:
                    out.append(element)
            return out
        return tag_list

    tag_cat = cat_list(raw_features[4]) + cat_list(raw_features[6]) + \
        cat_list(raw_features[8]) + cat_list(raw_features[10])
    # We create a vocabulary of dependency tags
    tag_vocab = set(tag_cat)
    vocab_list = list(tag_vocab)

    print(len(raw_features))
    print(len(raw_features[0]))
    # First feature list corresponds to target verb position
    # encoded to int
    encoded_features.append(list(map(int, raw_features[0])))

    # Second feature list corresponds to base surrounding words with padding
    # encoded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[1], embeddings_index))

    # Third feature list corresponds to base surrounding words without padding
    # including the target verb in the middle.
    # encoded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[2], embeddings_index))

    # Fourth feature list corresponds to surface dependant words
    # encoded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[3], embeddings_index))

    # Fifth feature list corresponds to surface dependant tags
    # encoded to one hot vectors
    encoded_features.append(one_hot_encoding(
        raw_features[4], vocab_list))

    # Sixth feature list corresponds to surface governor words
    # econded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[5], embeddings_index))

    # Seventh feature list corresponds to surface governor tags
    # encoded to one hot vectors
    encoded_features.append(one_hot_encoding(
        raw_features[6], vocab_list))

    # Eighth feature list corresponds to deep dependant words
    # encoded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[7], embeddings_index))

    # Ninth feature list corresponds to deep dependant tags
    # encoded to one hot vectors
    encoded_features.append(one_hot_encoding(
        raw_features[8], vocab_list))

    # Tenth feature list corresponds to deep governor words
    # econded to word embeddings
    encoded_features.append(embedding_encoding(
        raw_features[9], embeddings_index))

    # Eleventh feature list corresponds to deep governor tags
    # encoded to one hot vectors
    encoded_features.append(one_hot_encoding(
        raw_features[10], vocab_list))
    return encoded_features


def embedding_encoding(word_list, embeddings_index):
    """
    types: (list) -> list
    structure: ("raw features") -> "encoded features"
    """
    def context_mapping(word_list):
        """
        Embedding mapping sub func
        """
        emb_map = np.zeros(100)
        wordc = 0
        for word in word_list:
            if word in embeddings_index:
                wordc += 1
                emb_map = np.add(emb_map, embeddings_index[word])
        if wordc > 0:
            emb_map /= wordc
        # emb_map = [embeddings_index[word] for word in word_list if word in embeddings_index]
        return emb_map

    context_embeddings = list(map(context_mapping, word_list))
    return context_embeddings


def one_hot_encoding(tag_list, vocab_list):
    """
    types: (list, list) -> list
    structure: ("raw features") -> "encoded features"
    """
    enc_tag_list = []
    for tags in tag_list:
        enc_tags = []
        for tag in tags:
            enc_tag = text.hashing_trick(tag, len(
                vocab_list), hash_function='md5', filters='!"#$%&()*+,-/;<=>?@[\\]^_`{|}~\t\n', lower=False)
            enc_tags.append(enc_tag[0])
        enc_tag_list.append(enc_tags)
    # enc_tag_list = np.array(enc_tag_list)
    bin_enc_tag_list = []
    for enc_list in enc_tag_list:
        bin_enc_tag_list.append(to_categorical(enc_list, len(vocab_list)))

    return bin_enc_tag_list
    # bin_enc_tag_list = list(map(to_categorical, enc_tag_list))
    print(tag_list[0:5])
    print(enc_tag_list[0:5])
    print(bin_enc_tag_list[0:5])
    print(len(enc_tag_list))
    print(len(enc_tag_list[0:5]))
    print(len(tag_list[0:5]))
    exit(0)


def obtain_examples(file):
    """
    Obtains a list from a connll file
    """
    example_list = conll_list(file)
    return example_list


CONLL = "data_WSD_VS/aborder.deep_and_surf.sensetagged.conll"
WE = "data_WSD_VS/vecs100-linear-frwiki"
ex = obtain_examples(CONLL)
RAW_F = feature_extraction(ex, "aborder")
ENC_F = encode_features(RAW_F, WE)
FN = ["index", "window1", "window2", "surface dep words", "surface dep tags", "surface gov words",
      "surface gov tags", "deep dep words", "deep dep tags", "deep gov wods", "deep gov tags"]

for i in range(11):
    print(FN[i])
    print(RAW_F[i][216])
    print(ENC_F[i][216])
    print("____________________________________________________________")
