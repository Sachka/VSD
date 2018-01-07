# coding: UTF-8
"""
Verb-sense disambiguation demonstration
"""
from corpus_reading import conll_list


def feature_extraction(example_list, target_verb, window=5):
    """
    Feature extraction
    """

    # Sub lists of feats
    target_verb_index = []
    window_word_feats = []
    base_surrounding_word_feats = []

    raw_features = complex_feature_extraction(example_list, target_verb)

    # target_verb_index = get_target_verb_i(example_list, target_verb)

    # finding index of target_verb for each example
    for exemple in example_list:
        for word_tags in exemple:
            if word_tags[2] == target_verb:
                target_verb_index.append(word_tags[0])
                break

    # Extracts the linear context of the target verb (words to the left and to the right)
    window_word_feats = word_window(example_list, target_verb, window)
    base_surrounding_word_feats = base_surrounding_words(
        example_list, target_verb, window)

    # Insert the 3 first basic features at the beginning of the list of features
    raw_features.insert(0, base_surrounding_word_feats)
    raw_features.insert(0, window_word_feats)
    raw_features.insert(0, target_verb_index)

    return raw_features


def word_window(example_list, target_verb, window=5):
    """
    Extract the words surrounding the target verb WITH padding
    """
    ww_feautures = []
    beg = "@@@"
    end = "$$$"
    position = 0
    beg_idx = 0
    end_idx = 0
    c = 0
    for example in example_list:
        c += 1
        ww_example = []
        for word_elements in example:
            if word_elements[2] == target_verb:
                position = int(word_elements[0]) - 1
        beg_idx = position - window
        if beg_idx < 0:
            for idx in range(beg_idx, 0):
                ww_example.append(beg)
            beg_idx = 0
        end_idx = position + window + 1
        padding = 0
        if end_idx > len(example):
            padding = end_idx - len(example) + 1
            end_idx = len(example)
        for idx in range(beg_idx, end_idx):
            if idx == position:
                continue
            # print(idx)
            ww_example.append(example[idx][1])
        if padding > 0:
            for idx in range(padding - 1):
                ww_example.append(end)
        # ww_example.append(position + 1)
        ww_feautures.append(ww_example)
    return ww_feautures


def base_surrounding_words(example_list, target_verb, window=5):
    """
    Extract the words surrounding the target verbs (WITHOUT PADDING)
    """
    ww_feautures = []
    position = 0
    beg_idx = 0
    end_idx = 0
    for example in example_list:
        ww_example = []
        for word_elements in example:
            if word_elements[2] == target_verb:
                position = int(word_elements[0]) - 1
        beg_idx = max(position - window, 0)
        end_idx = min(position + window + 1, len(example))
        for idx in range(beg_idx, end_idx):
            ww_example.append(example[idx][1])
        ww_feautures.append(ww_example)
    return ww_feautures


def y_senseId_extraction(example_list, target_verb):
    """
    Extract the Y values, that is to say a list of IDs of the sense for each example
    ARGUMENTS : list of sentences (corpus), the target verb (aborder,abbattre or affecter)
    RETURN : a list of the IDs of senses for each sentence in the corpus
    """
    y_senseID = []

    for example in example_list:
        for word_elements in example:
            if word_elements[2] == target_verb:  # Target verb information
                # list of information in column 5
                info_list = word_elements[5].split('|')
                for e in info_list:
                    if "sense=" in e:  # information obout the sense
                        sense_list = e.split('#')
                        # we add the sense ID of the current example into the big list with all the examples
                        y_senseID.append(sense_list[1])
                break  # there is one example were there are 2 occurrences of the target verb in one sentence, we chose to select the first one only

    return y_senseID


def complex_feature_extraction(example_list, target_verb):
    """
    Gets the informations about the surface syntaxic context of the target verb (word forms and tags) and its deep syntaxic
    context (word forms and tags)
    INPUT: the list of examples (corpus), the target verb
    RETURN: 8 lists
    """

    # LIST FOR THE WHOLE CORPUS (all the examples)
    surf_dep_words = []
    surf_dep_tags = []
    surf_gov_words = []
    surf_gov_tags = []

    deep_dep_words = []
    deep_dep_tags = []
    deep_gov_words = []
    deep_gov_tags = []

    position = 0
    count = 0
    # We go through the list of examples(sentences)
    for example in example_list:
        count += 1

        # LISTS FOR THE CURRENT EXAMPLE (the current sentence)
        curr_surf_dep_words = []
        curr_surf_dep_tags = []
        curr_surf_gov_words = []
        curr_surf_gov_tags = []

        curr_deep_dep_words = []
        curr_deep_dep_tags = []
        curr_deep_gov_words = []
        curr_deep_gov_tags = []

        gov_idx_surf = []
        gov_idx_deep = []

        # Target verb position finding loop
        for word_elements in example:
            # IF WORDFORM EQUALS TARGET VERB, WE'VE FOUND ITS POSITION
            if word_elements[2] == target_verb:
                position = int(word_elements[0])
                break  # there is one example were there are 2 occurrences of the target verb in one sentence, we chose to select the first one only

        for word_elements in example:  # we go through each word in the sentence

            # index of words that are connected to the current word
            target_idx_list = word_elements[6].split('|')
            # tags of words that are connected to the current word
            target_tag_list = word_elements[7].split('|')

            for i in range(len(target_idx_list)):

                # Check to find DEPENDANTS: (that is to say, words that "points" to the target verb index)

                if int(position) == int(target_idx_list[i]):
                        # Surface syntax
                    if "S:" in target_tag_list[i]:
                        curr_surf_dep_words.append(word_elements[1])
                        curr_surf_dep_tags.append(target_tag_list[i][2:])
                    # Deep syntax
                    elif "D:" in target_tag_list[i]:
                        curr_deep_dep_words.append(word_elements[1])
                        curr_deep_dep_tags.append(target_tag_list[i][2:])
                    # if there is no 'S' or 'D', it is for both types of syntax,we add into the two lists
                    else:
                        curr_surf_dep_words.append(word_elements[1])
                        curr_surf_dep_tags.append(target_tag_list[i])
                        curr_deep_dep_words.append(word_elements[1])
                        curr_deep_dep_tags.append(target_tag_list[i])

            # Check to find GOVERNORS: (that is to say, the word indexes the target verb "points" to)

            # If it's is the target verb
            if int(position) == int(word_elements[0]):
                for i in range(len(target_idx_list)):
                        # Surface syntaxe
                    if "S:" in target_tag_list[i]:
                        gov_idx_surf.append(target_idx_list[i])
                        curr_surf_gov_tags.append(target_tag_list[i][2:])
                    # Deep syntaxe
                    elif "D:" in target_tag_list[i]:
                        gov_idx_deep.append(target_idx_list[i])
                        curr_deep_gov_tags.append(target_tag_list[i][2:])
                    # if there is no 'S' or 'D', it is for both types of syntaxe,we add into the two lists
                    else:
                        gov_idx_surf.append(target_idx_list[i])
                        gov_idx_deep.append(target_idx_list[i])
                        curr_surf_gov_tags.append(target_tag_list[i])
                        curr_deep_gov_tags.append(target_tag_list[i])

                # now that we have the indexes, we need to get the word forms
                for i in gov_idx_surf:
                    if int(i) == 0:
                        # Append "root" if i == 0
                        # curr_surf_gov_words.append(example[position - 1][7])
                        curr_surf_gov_words.append(example[int(i) - 1][1])
                    else:
                        curr_surf_gov_words.append(example[int(i) - 1][1])
                for i in gov_idx_deep:
                    if int(i) == 0:
                        # Append "root" if i == 0
                        curr_deep_gov_words.append(example[int(i) - 1][1])
                        # curr_deep_gov_words.append(example[position - 1][7])
                    else:
                        curr_deep_gov_words.append(example[int(i) - 1][1])

        # We append the information of the current example in the big list with the informations for all the examples
        surf_dep_words.append(curr_surf_dep_words)
        surf_dep_tags.append(curr_surf_dep_tags)
        surf_gov_words.append(curr_surf_gov_words)
        surf_gov_tags.append(curr_surf_gov_tags)

        deep_dep_words.append(curr_deep_dep_words)
        deep_dep_tags.append(curr_deep_dep_tags)
        deep_gov_words.append(curr_deep_gov_words)
        deep_gov_tags.append(curr_deep_gov_tags)

    return [surf_dep_words,
            surf_dep_tags,
            surf_gov_words,
            surf_gov_tags,

            deep_dep_words,
            deep_dep_tags,
            deep_gov_words,
            deep_gov_tags]


def obtain_examples(file):
    """
    Obtains a list from a connll file
    """
    example_list = conll_list(file)
    return example_list


CONLL = "data_WSD_VS/aborder.deep_and_surf.sensetagged.conll"
ex = obtain_examples(CONLL)
RAW_F = feature_extraction(ex, "aborder")

"""
RAW FEATURES :

 POSITION OF THE TARGET VERB:
 	0  target verb index

 LINEAR CONTEXT:
 	1  window words features WITH padding
 	2  base_surrounding_featsWITHOUT padding

 SURFACE SYNTAXE CONTEXT:
 	3  dependant words
 	4  dependant tags
 	5  governor words
 	6  governor tags

 DEEP SYNTAXE CONTEXTE
 	7  dependant words
 	8  dependant tags
 	9  governor words
 	10 governor tags
"""

# print("---------------------------------------------------------------------------------------------------")
# print("EXAMPLE : aborder, 219")
# print("---------------------------------------------------------------------------------------------------")
# print("target verb position: ", RAW_F[0][10])
# print("")
# print("LINEAR CONTEXT:")
# print(RAW_F[1][10])
# print(RAW_F[2][10])
# print("")
# print("SURFACE SYNTAXE CONTEXT:")
# print(RAW_F[3][10])
# print(RAW_F[4][10])
# print(RAW_F[5][10])
# print(RAW_F[6][10])
# print("")
# print("DEEP SYNTAXE CONTEXT:")
# print(RAW_F[7][10])
# print(RAW_F[8][10])
# print(RAW_F[9][10])
# print(RAW_F[10][10])
# print("")
# print("sense ID: ", y_senseId_extraction(ex, "aborder")[219])
# print("")
# print("---------------------------------------------------------------------------------------------------")
# print("WHOLE LISTS")
# print("---------------------------------------------------------------------------------------------------")
# # print(RAW_F[2])
# print("---------------------------------------------------------------------------------------------------")
# # print(RAW_F[3])
# print("---------------------------------------------------------------------------------------------------")
# # print(RAW_F[4])
# print("---------------------------------------------------------------------------------------------------")
# # print(RAW_F[5])
# print("---------------------------------------------------------------------------------------------------")
# # print(RAW_F[6])
# print("---------------------------------------------------------------------------------------------------")
