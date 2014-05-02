#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

""""""

import sys
import logging
import argparse
import datetime

S_BEGIN = "<S>"
S_END   = "</S>"
T_BEGIN = "<T>"
T_END   = "</T>"
UNK     = "<UNK>"

if __name__ == "__main__":

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i",    "--input-data",                 type=str)
    argparser.add_argument("-tv",   "--target-vocab",               type=str)
    argparser.add_argument("-sv",   "--source-vocab",               type=str)
    argparser.add_argument("-wi",   "--write-input-vocab-file",     type=str)
    argparser.add_argument("-wo",   "--write-output-vocab-file",    type=str)
    argparser.add_argument("-tf",   "--write-train-file",           type=str)
    argparser.add_argument("-vf",   "--write-valid-file",           type=str)
    argparser.add_argument("-twf",  "--write-train-w-file",         type=str)
    argparser.add_argument("-vwf",  "--write-valid-w-file",         type=str)
    argparser.add_argument("-n",    "--target-vector-size",         type=int)
    argparser.add_argument("-m",    "--source-vector-size",         type=int)
    argparser.add_argument("-vs",   "--valid-data-size",            type=int)
    argparser.add_argument("-v",    "--verbosity-level",            type=int,
                                                                    default=1,
                                                                    choices=(0, 1, 2))
    args = argparser.parse_args()

    if args.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)


    m = args.source_vector_size
    n = args.target_vector_size
    k = m / 2


    with open(args.source_vocab, "rb") as fl:
        source_vocab = [S_BEGIN, S_END, UNK] \
                       + ["S_" + w for w in fl.read().split("\n")[4:]]
    with open(args.target_vocab, "rb") as fl:
        target_vocab = [T_BEGIN, T_END, UNK] \
                       + ["T_" + w for w in fl.read().split("\n")[4:]]

    input_vocab = {}
    output_vocab = {}

    with open(args.write_input_vocab_file, "wb") as fl:
        for word in source_vocab:
            input_vocab[word] = len(input_vocab)
            fl.write(word)
            fl.write("\n")
        for word in target_vocab:
            input_vocab[word] = len(input_vocab)
            fl.write(word)
            fl.write("\n")

    with open(args.write_output_vocab_file, "wb") as fl:
        for word in target_vocab:
            output_vocab[word] = len(output_vocab)
            fl.write(word)
            fl.write("\n")


    examples = []

    with open(args.input_data, "rb") as i_fl:
        for lineno, line in enumerate(i_fl):

            if lineno % 10000 == 0:
                logging.info("Sentence %d. Example extracted." % lineno)

            source, target, alignment = line.rstrip().split(" ||| ")
            source = ["S_" + w for w in source.split()]
            target = ["T_" + w for w in target.split()]
            alignment = [(int(a_s),int(a_t)) for a_s, a_t in
                         [a.split("-") for a in alignment.split()]]

            t_alignment = [a_s for a_s, a_t in alignment]

            for t_i in xrange(len(target)):
                example_in = []

                for k_i in xrange(1, n):
                    t_j = t_i - k_i
                    if t_j < 0:
                        example_in.append(T_BEGIN)
                    else:
                        example_in.append(target[t_j])

                s_i = t_alignment[t_i]
                for k_i in xrange(-k, k + 1):
                    s_j = s_i + k_i
                    if s_j < 0:
                        example_in.append(S_BEGIN)
                    elif s_j >= len(source):
                        example_in.append(S_END)
                    else:
                        example_in.append(source[s_j])

                examples.append([example_in, target[t_i]])

        logging.info("Sentence %d. Example extracted." % lineno)

        for i in xrange(len(examples)):
            example_in, example_out = examples[i]
            if example_out not in output_vocab:
                examples[i][1] = UNK
            for j in xrange(len(example_in)):
                if example_in[j] not in input_vocab:
                    example_in[j] = UNK


        train_file = open(args.write_train_file, "wb")
        valid_file = open(args.write_valid_file, "wb")
        train_w_file = open(args.write_train_w_file, "wb")
        valid_w_file = open(args.write_valid_w_file, "wb")

        for i, (example_in, example_out) in enumerate(examples):

            if i % 100000 == 0:
                logging.info("Write example %d." % i)

            input_w_ids = [str(input_vocab[w]) for w in example_in]
            output_w_id = str(output_vocab[example_out])

            train_w_file.write("%s %s\n" % (" ".join(example_in), example_out))
            train_file.write("%s %s\n" % (" ".join(input_w_ids), output_w_id))

        logging.info("Write example %d." % i)


