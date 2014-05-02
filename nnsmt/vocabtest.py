#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import sys
import logging
import argparse
import datetime
import decoding
import itertools


if __name__ == "__main__":

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("-iv",   "--i-vocab-fl",                 type=str)
    argparser.add_argument("-ov",   "--o-vocab-fl",                 type=str)

    argparser.add_argument("-niv",  "--new-i-vocab-fl",             type=str)
    argparser.add_argument("-nov",  "--new-o-vocab-fl",             type=str)

    argparser.add_argument("-tf",   "--train-file",                 type=str)
    argparser.add_argument("-twf",  "--train-w-file",               type=str)
    argparser.add_argument("-n",    "--target-vector-size",         type=int)
    argparser.add_argument("-m",    "--source-vector-size",         type=int)
    argparser.add_argument("-v",    "--verbosity-level",            type=int,
                                                                    default=1,
                                                                    choices=(0, 1, 2))

    args = argparser.parse_args()

    if args.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)


    i_vocab_id2w, i_vocab_w2id = decoding.load_vocab_file(args.i_vocab_fl)
    o_vocab_id2w, o_vocab_w2id = decoding.load_vocab_file(args.o_vocab_fl)

    w_file = open(args.train_w_file, "rb")
    i_file = open(args.train_file, "rb")

    new_i_vocab = {}
    new_o_vocab = {}

    for w_line, i_line in itertools.izip(w_file, i_file):

        words = w_line.rstrip().split()
        ids = i_line.rstrip().split()

        input_words = words[:-1]
        output_word = words[-1]

        input_ids = map(int, ids[:-1])
        output_id = int(ids[-1])

        if output_word not in new_o_vocab:
            new_o_vocab[output_word] = output_id
        else:
            if new_o_vocab[output_word] != output_id:
                logging.error("Inconsistency found %d != %d" % (new_o_vocab[output_word], output_id))


        for word, word_id in itertools.izip(input_words, input_ids):

            if word not in new_i_vocab:
                new_i_vocab[word] = word_id
            else:
                if new_i_vocab[word] != word_id:
                    logging.error("Inconsistency found %d != %d" % (new_i_vocab[word], word_id))


    with open(args.new_i_vocab_fl, "wb") as fl:
        items = new_i_vocab.items()
        items.sort(key=lambda x: x[1])
        for w, w_id in items:
            fl.write("%d\t%s" % (w_id, w))
            fl.write("\n")

    with open(args.new_o_vocab_fl, "wb") as fl:
        items = new_o_vocab.items()
        items.sort(key=lambda x: x[1])
        for w, w_id in items:
            fl.write("%d\t%s" % (w_id, w))
            fl.write("\n")