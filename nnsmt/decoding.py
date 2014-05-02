# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import nplm
import logging
import itertools
import numpy as np
import Queue as queue

class State(object):

    def __init__(self,
        translated=None,
        s_i=None,
        score=None,
        prev_state=None,
        cover=None,
        jump=None):
        self.translated = translated
        self.score = score
        self.prev_state = prev_state
        self.cover = cover
        self.s_i = s_i
        self.jump = 0

    def is_final(self):
        return np.count_nonzero(self.cover) == len(self.cover)

    def repr(self, depth):
        return "<State(score=%.3f T='%s' s_i=%d jump=%d cover=%s p=\n%s%s)>" % (
            self.score,
            "START" if self.prev_state is None else self.translated,
            self.s_i,
            self.jump,
            "".join([str(c) for c in self.cover]),
            " "*depth,
            "" if self.prev_state is None else self.prev_state.repr(depth+1),
        )

    def __repr__(self):
        return self.repr(1)


class ZDecoder(object):

    def __init__(self):
        self.t_model = None
        self.d_model = None
        self.f_model = None
        self.s_size = None
        self.t_size = None
        self.i_vocab_w2id = None
        self.i_vocab_id2w = None
        self.o_vocab_w2id = None
        self.o_vocab_id2w = None
        self.k = None
        self.observed = None
        self.j_model = {
            -3: -2.5,
            -2: -2.0,
            -1: -1.5,
             0: -2.0,
            +1: -1.0,
            +2: -1.5,
            +3: -2.5,
        }

    def expand(self, state, aug_source, aug_source_ids):

        new_states = []
        for jump in xrange(-3, 4):

            new_s_i = state.s_i + jump

            if new_s_i < 0 or new_s_i >= len(state.cover) or state.cover[new_s_i] == 2:
                continue

            new_t_history = state.translated[:(self.t_size-1)]
            new_t_history_ids = [self.i_vocab_w2id[t_w] for t_w in new_t_history]

            new_s_context = []
            for s_k in xrange(new_s_i-self.k, new_s_i+self.k+1):
                if s_k == -1:
                    s_w = "<S>"
                elif s_k >= len(aug_source):
                    s_w = "</S>"
                else:
                    s_w = aug_source[s_k]
                new_s_context.append(s_w)
            new_s_context_ids = [self.i_vocab_w2id[w] for w in new_s_context]

            # print new_t_history_ids
            # print new_s_context_ids

            context = tuple(new_s_context_ids)

            translation_context = new_t_history_ids + new_s_context_ids + [None]

            # if context not in self.observed:
            #     # print
            #     # print "New T history", new_t_history, new_t_history_ids
            #     # print "New S context", new_s_context, new_s_context_ids
            #     # print "New state", state
            #     # print "Context", context
            #     # print "Context words", [self.i_vocab_id2w[w_id] for w_id in context]
            #     # print
            #     continue

            # for t_id in self.observed[context]:
            for t_id in self.o_vocab_id2w.iterkeys():

                translation_context[-1] = t_id
                t_score = self.t_model.lookup_ngram(translation_context)

                new_score = state.score + t_score

                new_translated = [self.o_vocab_id2w[t_id]] + state.translated
                new_cover = np.array(state.cover, copy=True)
                new_cover[new_s_i] += 1
                new_state = State(
                    prev_state=state,
                    translated=new_translated,
                    s_i=new_s_i,
                    score=new_score,
                    cover=new_cover,
                    jump=jump
                )
                new_states.append((new_state.score, new_state))

        print "Expanded %d new states." % len(new_states)

        new_states.sort(key=lambda x: x[0])

        return (state for _, state in new_states[:16])







    def decode(self, source):

        self.k = self.s_size / 2

        aug_source = ["<S>"] + ["S_" + s for s in source] + ["</S>"]
        aug_source_ids = [self.i_vocab_w2id[w] for w in aug_source]

        translated = ["<T>" for _ in xrange(self.t_size)]
        cover = np.zeros(len(aug_source)-1, dtype=np.int8)
        cover[0] = 2

        print aug_source

        initial = State(
            prev_state=None,
            translated=translated,
            s_i= 0,
            score=0.0,
            cover=cover,
            jump=0
        )

        expanded = [initial]
        leaves = []



        while len(expanded) > 0:

            new_expanded = []

            for state in expanded:
                for new_state in self.expand(state, aug_source, aug_source_ids):
                    if new_state.is_final():
                        leaves.append(new_state)
                    new_expanded.append(new_state)

            expanded = new_expanded

        leaves.sort(key=lambda state: state.score)

        for state in leaves:

            print state.is_final(), state
            print



    @staticmethod
    def load(t_model_fl=None, d_model_fl=None, f_model_fl=None, i_vocab_fl=None, o_vocab_fl=None,
             s_size=None, t_size=None, observed_data_fl=None):
        logging.info("Initializing decoder model.")
        zdec = ZDecoder()

        logging.info("Loading observed data.")
        observed = {}
        with open(observed_data_fl, "rb") as fl:
            for line in fl:
                tokens = map(int, line.rstrip().split())
                context = tuple(tokens[(t_size-1):-1])
                t = tokens[-1]
                if context not in observed:
                    observed[context] = {t}
                else:
                    observed[context].add(t)
        zdec.observed = observed

        logging.info("T-Model:      %s" % t_model_fl)
        t_model = nplm.NeuralLM()
        t_model.read(t_model_fl)

        logging.info("D-Model:      %s" % d_model_fl)
        # TODO

        logging.info("F-Model:      %s" % f_model_fl)
        # TODO

        logging.info("Input vocab:  %s" % i_vocab_fl)
        i_vocab_id2w, i_vocab_w2id = load_vocab_file(i_vocab_fl)

        logging.info("Output vocab: %s" % o_vocab_fl)
        o_vocab_id2w, o_vocab_w2id = load_vocab_file(o_vocab_fl)

        logging.info("Model size:   s=%d,t=1+%d. (%d-gram)." % (s_size, t_size-1, s_size + t_size))

        zdec.t_model = t_model
        zdec.d_model = None
        zdec.f_model = None
        zdec.s_size = s_size
        zdec.t_size = t_size
        zdec.i_vocab_w2id = i_vocab_w2id
        zdec.i_vocab_id2w = i_vocab_id2w
        zdec.o_vocab_w2id = o_vocab_w2id
        zdec.o_vocab_id2w = o_vocab_id2w

        return zdec

    def decode_context(self, full_context):
        t = full_context[-1]
        t_history = full_context[:(self.t_size-1)]
        s_context = full_context[(self.t_size-1):-1]
        decoded = []
        for w_id in t_history:
            decoded.append(self.i_vocab_id2w[w_id])
        for w_id in s_context:
            decoded.append(self.i_vocab_id2w[w_id])
        decoded.append(self.o_vocab_id2w[t])
        return decoded

    def self_test(self, k=32, observed_fl=None):

        t_words = u"man house glass book".decode("utf-8").split()
        aug_t_words = ["T_" + t for t in t_words]

        if observed_fl is not None:

            logging.info("Loading observed data: %s" % observed_fl)
            with open(observed_fl, "rb") as fl:
                observed = {}
                for line in fl:
                    tokens = [int(t) for t in line.rstrip().split()]
                    t = tokens[-1]
                    t_history = tokens[:(self.t_size-1)]
                    s_context = tokens[(self.t_size-1):-1]
                    if t in observed:
                        observed[t].append((t_history, s_context))
                    else:
                        observed[t] = [(t_history, s_context)]
                logging.info("Loaded observed data (%d target words)." % len(observed))

            for t in aug_t_words:
                t_id = self.o_vocab_w2id[t]
                logging.info("Testing t='%s' (%d)." % (t, t_id))
                best_k = queue.PriorityQueue(k)
                for t_history, s_context in observed[t_id]:
                    t_context = t_history + s_context + [t_id]
                    score = self.t_model.lookup_ngram(t_context)
                    priority = -score
                    item = (score, t_context)
                    if best_k.full():
                        prev_item = best_k.get()
                        prev_score, prev_t_context = prev_item
                        prev_priority = -prev_score
                        if priority <= prev_priority:
                            best_k.put(item, priority)
                        else:
                            best_k.put(prev_item, prev_priority)
                    else:
                        best_k.put(item, priority)
                best = []
                while not best_k.empty():
                    score, t_context = best_k.get()
                    context = self.decode_context(t_context)
                    best.append((score, " ".join(context)))
                best = reversed(best)
                for score, translation in best:
                    print score, t, "=>", translation


def load_vocab_file(file_path):
    with open(file_path, "rb") as fl:
        vocab_id2w = {int(w_id):w for w_id,w in [entry.split("\t") for entry in fl.read().rstrip().split("\n")]}
        vocab_w2id = {w:w_id for w_id,w in vocab_id2w.iteritems()}
        logging.info("Loaded %d tokens" % len(vocab_id2w))
    return vocab_id2w, vocab_w2id
