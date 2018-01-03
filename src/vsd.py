# coding: UTF-8
"""
Verb-sense disambiguation demonstration
"""
from corpus import conll_list


def feature_extraction(example_list, target_verb):
    """
    Feature extraction
    """
    raw_features = []
    target_verb_index = []
    window_words_features = []
    base_surrounding_features = []
    surf_deep_dependant_feats = []
    surf_deep_gouvernor_feats = []
    # target_verb_index = get_target_verb_i(example_list, target_verb)

    # finding index of target_verb for each example
    for exemple in example_list:
        for word_tags in exemple:
            if word_tags[2] == target_verb:
                target_verb_index.append(word_tags[0])
                break
    window_words_features = word_window(example_list, target_verb)
    base_surrounding_features = base_surrounding_words(
        example_list, target_verb)
    surf_deep_dependant_feats, surf_deep_gouvernor_feats = surf_and_deep_extraction(
        example_list, target_verb)

    raw_features.append(target_verb_index)
    raw_features.append(window_words_features)
    raw_features.append(base_surrounding_features)
    raw_features.append(surf_deep_dependant_feats)
    raw_features.append(surf_deep_gouvernor_feats)

    # print(len(example_list))
    # print(len(raw_features))
    # print(len(raw_features[0]))
    # print(len(raw_features[1]))
    # for i in range(222):
    #     print(i, raw_features[0][i], raw_features[1]
    #           [i][len(raw_features[1][i]) - 1])
    # print(raw_features[1][39])
    # print(raw_features[1][40])
    return raw_features


def word_window(example_list, target_verb, window=5):
    """
    Feature creation
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
        # print("\nexample #", c)
        # print("len of example:", len(example))
        # print("target verb:", example[position][2])
        # print("position of target verb:", position)
        # print("begining index:", beg_idx)
        # print("end index:", end_idx)
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
    Feature creation
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
            # print(idx)
            ww_example.append(example[idx][1])
        ww_feautures.append(ww_example)
    return ww_feautures


def surf_and_deep_extraction(example_list, target_verb):
    """
    Feature creation
    """
    surf_dependant_words = []
    surf_gouvernor_words = []
    deep_gouvernor_words = []
    deep_dependant_words = []
    surf_and_deep_dependant_words = []
    surf_and_deep_gouvernor_words = []

    position = 0
    c = 0
    for example in example_list:
        c += 1
        curr_surf_deep_dep_words = []
        curr_surf_deep_gov_words = []
        curr_surf_gov_words = []
        curr_deep_gov_words = []
        # Target verb position finding loop
        for word_elements in example:
            if word_elements[2] == target_verb:
                position = int(word_elements[0])

        # if c == 222:
        #     print("idx g_s", gov_idx_surf, len(gov_idx_surf))
        #     print("idx g_d", gov_idx_deep, len(gov_idx_deep))
        #     print("idx g_sd", gov_idx_surf_deep, len(gov_idx_surf_deep))
        #     exit(0)

        # Surf and deep dependant finding loop
        print("example:", c)
        print("lenght of example:", len(example))
        for word_elements in example:
            target_word = word_elements[6]
            # print(c, word_elements[0], word_elements[6], position)
            if target_word.split('|'):
                for i in range(len(target_word.split('|'))):
                    # Check to find dependants
                    if int(position) == int(target_word.split('|')[i]):
                        curr_surf_deep_dep_words.append(word_elements[1])
                    # Check to find gouvernors

            elif int(word_elements[6]) == int(position):
                # print("true")
                curr_surf_deep_dep_words.append(word_elements[1])
            if int(position) == int(word_elements[0]):
                gov_idx_surf = []
                gov_idx_deep = []
                gov_idx_surf_deep = []
                idx_list = word_elements[6].split('|')
                if idx_list:
                    for i in range(len(idx_list)):
                        if "S:" in word_elements[7].split('|')[i]:
                            print("S")
                            gov_idx_surf.append(idx_list[i])
                        elif "D:" in word_elements[7].split('|')[i]:
                            print("D")
                            gov_idx_deep.append(idx_list[i])
                        else:
                            print("_")
                            gov_idx_surf_deep.append(idx_list[i])
                for i in gov_idx_surf_deep:
                    print(i)
                    if int(i) == 0:
                        print(i)
                        curr_surf_deep_gov_words.append("root")
                        break
                    curr_surf_deep_gov_words.append(example[int(i) - 1][1])
                for i in gov_idx_surf:
                    curr_surf_gov_words.append(example[int(i) - 1][1])
                for i in gov_idx_deep:
                    print(i)
                    curr_deep_gov_words.append(example[int(i) - 1][1])

        surf_and_deep_dependant_words.append(curr_surf_deep_dep_words)
        surf_and_deep_gouvernor_words.append(curr_surf_deep_gov_words)
    # print(surf_and_deep_dependant_words)
    return (surf_and_deep_dependant_words, surf_and_deep_gouvernor_words)


def obtain_examples(file):
    """
    Obtains a list from a connll file
    """
    example_list = conll_list(file)
    return example_list


CONLL = "data_WSD_VS/aborder.deep_and_surf.sensetagged.conll"
ex = obtain_examples(CONLL)
raw_features = feature_extraction(ex, "aborder")
print(raw_features[0][221])
print(raw_features[1][221])
print(raw_features[2][221])
print(raw_features[3][221])
print(raw_features[4][221])
