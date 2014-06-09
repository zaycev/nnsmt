# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import nplm
import logging
import itertools
<<<<<<< HEAD
<<<<<<< HEAD
import preparing
import numpy as np
import collections
import Queue as queue


=======
import numpy as np
import Queue as queue

>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
import numpy as np
import Queue as queue

>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
class State(object):

    def __init__(self,
        translated=None,
        s_i=None,
<<<<<<< HEAD
<<<<<<< HEAD
        prev_state=None,
        cover=None,
        jump=None,
        t_score=None,
        d_score=None,
        f_score=None):
        self.translated = translated
        self.prev_state = prev_state
        self.cover = cover
        self.s_i = s_i
        self.jump = jump
        self.t_score = t_score
        self.d_score = d_score
        self.f_score = f_score

    def total_score(self):
        return self.t_score + self.d_score + self.f_score
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

    def is_final(self):
        return np.count_nonzero(self.cover) == len(self.cover)

    def repr(self, depth):
<<<<<<< HEAD
<<<<<<< HEAD
        return "<State(score=%.3f[%.3f;%.3f;%.3f] T='%s' s_i=%d jump=%d cover=%s p=\n%s%s)>" % (
            self.total_score(),
            self.t_score,
            self.d_score,
            self.f_score,
=======
        return "<State(score=%.3f T='%s' s_i=%d jump=%d cover=%s p=\n%s%s)>" % (
            self.score,
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
        return "<State(score=%.3f T='%s' s_i=%d jump=%d cover=%s p=\n%s%s)>" % (
            self.score,
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
<<<<<<< HEAD
        self.max_jump = None
        self.max_fert = None
        self.i_vocab_w2id = None
        self.i_vocab_id2w = None
        self.o_t_vocab_w2id = None
        self.o_t_vocab_id2w = None
        self.o_d_vocab_w2id = None
        self.o_d_vocab_id2w = None
        self.o_f_vocab_w2id = None
        self.o_f_vocab_id2w = None
        self.observed = None
        self.k = None
        self.t_weight = None
        self.d_weight = None
        self.f_weight = None
        self.fert_words = []
        self.fert_words_ids = []

    def expand(self, state, aug_source, aug_source_ids, s_contexts, s_contexts_ids):

        new_states = []


        total_raw_d_score = 0.0


        for jump in xrange(-self.max_jump, self.max_jump + 1):

            new_s_i = state.s_i + jump

            if new_s_i < 0 or new_s_i >= len(state.cover) or state.cover[new_s_i] == self.max_fert:
                continue

            new_cover = np.array(state.cover, copy=True)
            new_cover[new_s_i] += 1
            new_t_history = state.translated[:(self.t_size-1)]
            new_t_history_ids = [self.i_vocab_w2id.get(t_w, self.i_vocab_w2id["<T_UNK>"]) for t_w in new_t_history]
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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

<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
            new_s_context = []
            for s_k in xrange(new_s_i-self.k, new_s_i+self.k+1):
                if s_k == -1:
                    s_w = "<S>"
                elif s_k >= len(aug_source):
                    s_w = "</S>"
                else:
                    s_w = aug_source[s_k]
                new_s_context.append(s_w)
<<<<<<< HEAD
<<<<<<< HEAD
            new_s_context_ids = [self.i_vocab_w2id.get(s_w, self.i_vocab_w2id["<S_UNK>"]) for s_w in new_s_context]
            # print new_t_history_ids
            # print new_s_context_ids
            # context = tuple(new_s_context_ids)
            translation_context = new_t_history_ids + new_s_context_ids + [None]
            translation_context[-1] = self.o_d_vocab_w2id["J_" + str(jump)]

            d_score = self.d_model.lookup_ngram(translation_context) * self.d_weight
            raw_d_score = np.exp(d_score)

            total_raw_d_score += raw_d_score

            f_score = self.compute_fert_score(new_cover, s_contexts, s_contexts_ids)
            # if context not in self.observed:
            # print
            # print "New T history", new_t_history, new_t_history_ids
            # print "New S context", new_s_context, new_s_context_ids
            # print "New state", state
            # print "Context", context
            # print "Context words", [self.i_vocab_id2w[w_id] for w_id in context]
            # print
            candidates = set()
            for s in new_s_context:
                s_cands = self.observed.get(s)
                # print s, s_cands
                if s_cands is not None:
                    candidates.update(s_cands)
            # print candidates
            # exit(0)

            total_raw_t_score = 0.0
            weighted_candidates = []

            for t in candidates:
                t_id = self.o_t_vocab_w2id[t]
                translation_context[-1] = t_id
                t_score = self.t_model.lookup_ngram(translation_context)
                raw_t_score = np.exp(t_score)
                total_raw_t_score += raw_t_score
                new_translated = [self.o_t_vocab_id2w[t_id]] + state.translated
                weighted_candidates.append((
                    new_translated,
                    raw_t_score,
                    t_score
                ))


            for new_translated, raw_t_score, t_score in weighted_candidates:

                new_t_score = np.log(raw_t_score / total_raw_t_score)

                # print new_translated, t_score, "=>", new_t_score, total_raw_t_score

=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
                new_state = State(
                    prev_state=state,
                    translated=new_translated,
                    s_i=new_s_i,
<<<<<<< HEAD
<<<<<<< HEAD
                    cover=new_cover,
                    jump=jump,
                    t_score=state.t_score + new_t_score,
                    d_score=raw_d_score,
                    f_score=f_score
                )
                new_states.append(new_state)

            # exit(0)
            # print "Expanded %d new states." % len(new_states)
            # new_states.sort(key=lambda x: -x.score)
            # for s in new_states[:3]:
            #     print s

        for s in new_states:
            s.d_score = state.d_score + np.log(s.d_score / total_raw_d_score)

        return new_states




    def precompute_s_contexts(self, source):
        contexts = []
        for i in xrange(0, len(source)-self.s_size+1):
            s_context = source[i:(i+self.s_size)]
            contexts.append(s_context)
        contexts_ids = []
        for context in contexts:
            context_ids = [self.i_vocab_w2id.get(w, self.i_vocab_w2id["<S_UNK>"]) for w in context] + [None]
            contexts_ids.append(context_ids)
            # print context, context_ids
            # for fert in xrange(self.max_fert+1):
            #     fert_w = "F_"+str(fert)
            #     fert_w_id = self.o_f_vocab_w2id[fert_w]
            #     vector = context_ids+[fert_w_id]
            #     print "\t", fert, fert_w, fert_w_id, vector, self.f_model.lookup_ngram(vector)

        for j in xrange(0, self.max_fert):
            fert_w = "F_" + str(j)
            fert_id = self.o_f_vocab_w2id[fert_w]
            self.fert_words.append(fert_w)
            self.fert_words_ids.append(fert_id)

        return contexts, contexts_ids

    def compute_fert_score(self, cover, contexts, contexts_ids):
        total_trans_fert_score = 0.0
        fert_i_score = 0.0
        for i in xrange(1, len(cover)):

            total_fert_score = 0.0
            context_ids = contexts_ids[i-1]

            # print contexts[i-1]

            for j, fert_id in enumerate(self.fert_words_ids):
                context_ids[-1] = fert_id
                fert_score = self.f_model.lookup_ngram(context_ids)
                if j == cover[i]:
                    fert_i_score = fert_score

                raw_fert_score = np.exp(fert_score)
                total_fert_score += raw_fert_score

                # print j, fert_score, raw_fert_score, total_fert_score


            # print
            raw_fert_score = np.exp(fert_i_score)
            new_raw_fert_score = raw_fert_score / total_fert_score
            new_fert_score = np.log(new_raw_fert_score)
            # print fert_i_score, raw_fert_score, new_raw_fert_score, fert_i_score, "=>", new_fert_score
            # fert_id = self.o_f_vocab_w2id[fert_w]
            # # context = contexts[i-1]
            # context_ids[-1] = fert_id

            total_trans_fert_score += new_fert_score
            # print
            # print

        # print total_trans_fert_score
        # exit(0)

        for f in cover:
            total_trans_fert_score -= self.f_weight * f
            if f > 1:
                total_trans_fert_score -= self.f_weight * f

        return total_trans_fert_score

    def decode(self, source, beam_n=100):
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
                    score=new_score,
                    cover=new_cover,
                    jump=jump
                )
                new_states.append((new_state.score, new_state))

        print "Expanded %d new states." % len(new_states)

        new_states.sort(key=lambda x: x[0])

        return (state for _, state in new_states[:16])







    def decode(self, source):
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

        self.k = self.s_size / 2

        aug_source = ["<S>"] + ["S_" + s for s in source] + ["</S>"]
<<<<<<< HEAD
<<<<<<< HEAD
        aug_source_ids = [self.i_vocab_w2id.get(w, self.i_vocab_w2id["<S_UNK>"]) for w in aug_source]

        translated = ["<T>" for _ in xrange(self.t_size)]
        cover = np.zeros(len(aug_source)-1, dtype=np.int8)
        cover[0] = self.max_fert

        # print aug_source
        # print self.compute_fert_score(cover, s_contexts, s_contexts_ids)

        s_contexts, s_contexts_ids = self.precompute_s_contexts(aug_source)
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        aug_source_ids = [self.i_vocab_w2id[w] for w in aug_source]

        translated = ["<T>" for _ in xrange(self.t_size)]
        cover = np.zeros(len(aug_source)-1, dtype=np.int8)
        cover[0] = 2

        print aug_source
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

        initial = State(
            prev_state=None,
            translated=translated,
<<<<<<< HEAD
<<<<<<< HEAD
            s_i=0,
            cover=cover,
            jump=0,
            t_score=0,
            d_score=0,
            f_score=0,
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
            s_i= 0,
            score=0.0,
            cover=cover,
            jump=0
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        )

        expanded = [initial]
        leaves = []


<<<<<<< HEAD
<<<<<<< HEAD
        iteration = 1
        while len(expanded) > 0:
            logging.info("Iteration %d. New states %d." % (iteration, len(expanded)))
            iteration += 1
=======

        while len(expanded) > 0:
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======

        while len(expanded) > 0:
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

            new_expanded = []

            for state in expanded:
<<<<<<< HEAD
<<<<<<< HEAD
                for new_state in self.expand(state, aug_source, aug_source_ids, s_contexts, s_contexts_ids):
=======
                for new_state in self.expand(state, aug_source, aug_source_ids):
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
                for new_state in self.expand(state, aug_source, aug_source_ids):
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
                    if new_state.is_final():
                        leaves.append(new_state)
                    new_expanded.append(new_state)

<<<<<<< HEAD
<<<<<<< HEAD

            stacks = {}
            for s in new_expanded:
                cover_str = " ".join(map(str, (1 if x > 0 else 0 for x in s.cover)))
                if cover_str in stacks:
                    stacks[cover_str].append(s)
                else:
                    stacks[cover_str] = [s]
            for stack in stacks.itervalues():
                stack.sort(key=lambda s: -s.total_score())

            expanded = []
            for i in xrange(beam_n):
                for stack in stacks.itervalues():
                    if len(stack) > i:
                        expanded.append(stack[i])
                    if len(expanded) >= beam_n:
                        break
                if len(expanded) >= beam_n:
                    break

            # expanded = new_expanded
            # expanded.sort(key=lambda s: -s.total_score())
            # expanded = expanded[:beam_n]

            expanded.sort(key=lambda s: -s.total_score())
            for s in expanded:
                cover_str = "".join(map(str, s.cover))
                trans_str = " ".join(list(reversed(s.translated))[3:])
                logging.info("%f %s:  '%s'" % (s.total_score(), cover_str, trans_str))

        leaves.sort(key=lambda s: -s.total_score())

        # logging.info("TOP K")
        # for s in leaves[:5]:
        #     words = list(reversed(s.translated))[3:]
        #     words = (w[2:] for w in words)
        #     logging.info("'%s' %.3f%.3f%.3f=%.4f %r" % (
        #         " ".join(words),
        #         s.t_score,
        #         s.d_score,
        #         s.f_score,
        #         s.total_score(),
        #         s,
        #     ))

        best_translation = leaves[0]
        words = list(reversed(best_translation.translated))[3:]
        words = [w[2:] for w in words]
        return best_translation.total_score(), words


    @staticmethod
    def load(t_model_fl=None,
             d_model_fl=None,
             f_model_fl=None,
             i_vocab_fl=None,
             o_t_vocab_fl=None,
             o_d_vocab_fl=None,
             o_f_vocab_fl=None,
             s_size=None,
             t_size=None,
             max_jump=None,
             max_fert=None,
             observed_data_fl=None,
             t_weight=None,
             d_weight=None,
             f_weight=None,
             t_cache_size=10):

        logging.info("Initializing decoder model.")
        zdec = ZDecoder()

        logging.info("Loading observed data (cache size is %d)." % t_cache_size)
        observed = {}
        with open(observed_data_fl, "rb") as fl:
            for line in fl:
                source, target, alignment = line.rstrip().split(" ||| ")
                source, target = source.split(), target.split()
                alignment = ((int(a_s),int(a_t)) for a_s,a_t in (a.split("-") for a in alignment.split()))
                for a_s, a_t in alignment:
                    s = "S_" + source[a_s]
                    t = "T_" + target[a_t]
                    if s in observed:
                        observed[s][t] += 1
                    else:
                        observed[s] = collections.Counter()
                        observed[s][t] += 1
        for s, t_words in observed.items():
            observed[s] = set([w for w,_ in t_words.most_common(t_cache_size)])
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        zdec.observed = observed

        logging.info("T-Model:      %s" % t_model_fl)
        t_model = nplm.NeuralLM()
        t_model.read(t_model_fl)

        logging.info("D-Model:      %s" % d_model_fl)
<<<<<<< HEAD
<<<<<<< HEAD
        d_model = nplm.NeuralLM()
        d_model.read(d_model_fl)

        logging.info("F-Model:      %s" % f_model_fl)
        f_model = nplm.NeuralLM()
        f_model.read(f_model_fl)

        logging.info("Input vocab:  %s" % i_vocab_fl)
        i_vocab_id2w, i_vocab_w2id = preparing.read_vocab_file(i_vocab_fl)

        logging.info("Output T vocab: %s" % o_t_vocab_fl)
        o_t_vocab_id2w, o_t_vocab_w2id = preparing.read_vocab_file(o_t_vocab_fl)

        logging.info("Output D vocab: %s" % o_d_vocab_fl)
        o_d_vocab_id2w, o_d_vocab_w2id = preparing.read_vocab_file(o_d_vocab_fl)

        logging.info("Output F vocab: %s" % o_f_vocab_fl)
        o_f_vocab_id2w, o_f_vocab_w2id = preparing.read_vocab_file(o_f_vocab_fl)

        logging.info("Model size:   s=%d,t=1+%d. (%d-gram)." % (s_size, t_size-1, s_size + t_size))
        logging.info("Jump size:    %d." % max_jump)
        logging.info("Fert size:    %d." % max_fert)

        zdec.t_model = t_model
        zdec.d_model = d_model
        zdec.f_model = f_model
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        zdec.s_size = s_size
        zdec.t_size = t_size
        zdec.i_vocab_w2id = i_vocab_w2id
        zdec.i_vocab_id2w = i_vocab_id2w
<<<<<<< HEAD
<<<<<<< HEAD
        zdec.o_t_vocab_w2id = o_t_vocab_w2id
        zdec.o_t_vocab_id2w = o_t_vocab_id2w
        zdec.o_d_vocab_w2id = o_d_vocab_w2id
        zdec.o_d_vocab_id2w = o_d_vocab_id2w
        zdec.o_f_vocab_w2id = o_f_vocab_w2id
        zdec.o_f_vocab_id2w = o_f_vocab_id2w
        zdec.max_jump = max_jump
        zdec.max_fert = max_fert
        zdec.t_weight = t_weight
        zdec.d_weight = d_weight
        zdec.f_weight = f_weight
=======
        zdec.o_vocab_w2id = o_vocab_w2id
        zdec.o_vocab_id2w = o_vocab_id2w
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
        zdec.o_vocab_w2id = o_vocab_w2id
        zdec.o_vocab_id2w = o_vocab_id2w
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

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
<<<<<<< HEAD
<<<<<<< HEAD
        decoded.append(self.o_t_vocab_id2w[t])
        return decoded

    def self_test(self, k=256, observed_fl=None):

        t_words = u"i live".decode("utf-8").split()
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        decoded.append(self.o_vocab_id2w[t])
        return decoded

    def self_test(self, k=32, observed_fl=None):

        t_words = u"man house glass book".decode("utf-8").split()
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
<<<<<<< HEAD
                t_id = self.o_t_vocab_w2id[t]
=======
                t_id = self.o_vocab_w2id[t]
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
                t_id = self.o_vocab_w2id[t]
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01


def load_vocab_file(file_path):
    with open(file_path, "rb") as fl:
        vocab_id2w = {int(w_id):w for w_id,w in [entry.split("\t") for entry in fl.read().rstrip().split("\n")]}
        vocab_w2id = {w:w_id for w_id,w in vocab_id2w.iteritems()}
        logging.info("Loaded %d tokens" % len(vocab_id2w))
    return vocab_id2w, vocab_w2id
<<<<<<< HEAD
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
