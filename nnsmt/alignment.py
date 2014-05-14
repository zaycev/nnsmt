#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import logging
import itertools

class AffilationHeuristicAligner(object):
    """This script modifies input word alignment according to the Affiliation heuristic:
    * If t_i aligns to exactly one source word, A_i is the index of the word it aligns to.
    * If t_i align to multiple source words, A_i is the index of the aligned word in the middle (round
    down).
    * If t_i is unaligned, we inherit its affiliation from the closest aligned word, starting with the right.
    """

    def __init__(self, *args, **kwargs):
        pass

    def select_index(self, t_affiliated, source):
        if len(t_affiliated) > 0:
            return len(t_affiliated) / 2 - 1
        raise ValueError("Cannot select index from no choices.")

    def find_affiliated(self, i, a_t2s, source):

        for radius in xrange(0, len(a_t2s)):

            # Check right first
            index = i + radius
            if index < len(a_t2s):
                if len(a_t2s[index]) > 0:
                    affilated = a_t2s[index]
                    selected_i = self.select_index(affilated, source)
                    return affilated[selected_i]

            # Check left.
            index = i - radius
            if index >= 0:
                if len(a_t2s[index]) > 0:
                    affilated = a_t2s[index]
                    selected_i = self.select_index(affilated, source)
                    return affilated[selected_i]

        raise ValueError("Cannot find any affiliated target word.")

    def post_process(self, source, target, alignment):

        if len(alignment) == 0:
            return None

        a_t2s = [None] * len(target)
        for i in xrange(len(target)):
            a_t2s[i] = []
        for s_i, t_i in alignment:
            a_t2s[t_i].append(s_i)

        new_alignment_t2s = [None] * len(target)
        unaligned_n = 0
        for i in xrange(len(a_t2s)):


            if len(a_t2s[i]) == 1:
                new_alignment_t2s[i] = a_t2s[i][0]

            if len(a_t2s[i]) > 1:
                index = self.select_index(a_t2s[i], source)
                new_alignment_t2s[i] = a_t2s[i][index]

            else:
                try:
                    new_alignment_t2s[i] = self.find_affiliated(i, a_t2s, source)
                except ValueError:
                    error_msg = "Error while inheriting nearest affiliation. \n"        \
                                "Source sent: %s.\nTarget sent: %s.\nAlignment %r.\n:"   \
                                "A_t2s: %r.\nTarget index: %d." % (
                                    " ".join(target),
                                    " ".join(source),
                                    alignment,
                                    a_t2s,
                                    i,
                                )
                    logging.error(error_msg)

        new_alignment = [(new_alignment_t2s[t], t) for t in xrange(len(new_alignment_t2s))]
        new_alignment.sort()

        return new_alignment


class AffilationPPHeuristicAligner(AffilationHeuristicAligner):
    """This script modifies input word alignment according to the Affiliation heuristic:
    * If t_i aligns to exactly one source word, A_i is the index of the word it aligns to.
    * If t_i align to multiple source words, A_i is the index of the aligned word in the middle (round
    down).
    * If t_i is unaligned, we inherit its affiliation from the closest aligned word, starting with the right.
    """

    def __init__(self, s_vocab=None, t_vocab=None, **kwargs):
        self.s_vocab = s_vocab
        self.t_vocab = t_vocab

    def select_index(self, t_affiliated, source):
        if len(t_affiliated) > 0:
            if len(t_affiliated) == 1:
                return 0
            else:
                best_f = self.s_vocab.get(source[t_affiliated[0]])
                best_w = 0
                for i in xrange(1, len(source)):
                    f = self.s_vocab.get(source[i], 0)
                    if f > 1 and f < best_f:
                        best_f = f
                        best_w = i
                return len(t_affiliated) / 2 - 1
        raise ValueError("Cannot select index from no choices.")


def iter_train_data(source_sents_fl, target_sents_fl, a3_fl):
    for s_line, t_line, a_line in itertools.izip(source_sents_fl, target_sents_fl, a3_fl):
        source = s_line.rstrip().split()
        target = t_line.rstrip().split()
        alignment = [(int(a_s), int(a_t)) for a_s,a_t in [a.split("-") for a in a_line.rstrip().split()]]
        alignment.sort()
        yield source, target, alignment

def load_giza_vcb(file_path):
    vcb = {}
    with open(file_path, "rb") as fl:
        for line in fl:
            _, word, freq = line.rstrip().split("\t")
            freq = int(freq)
            vcb[word] = freq
    return vcb
