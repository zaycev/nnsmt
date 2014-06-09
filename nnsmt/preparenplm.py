#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

<<<<<<< HEAD
=======
""""""

>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
import sys
import logging
import argparse
import datetime
<<<<<<< HEAD
import preparing
=======

S_BEGIN = "<S>"
S_END   = "</S>"
T_BEGIN = "<T>"
T_END   = "</T>"
UNK     = "<UNK>"
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

if __name__ == "__main__":

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()
<<<<<<< HEAD

=======
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
    argparser.add_argument("-i",    "--input-data",                 type=str)
    argparser.add_argument("-tv",   "--target-vocab",               type=str)
    argparser.add_argument("-sv",   "--source-vocab",               type=str)
    argparser.add_argument("-wi",   "--write-input-vocab-file",     type=str)
<<<<<<< HEAD
    argparser.add_argument("-wd",   "--write-output-j-vocab-file",  type=str)
    argparser.add_argument("-wf",   "--write-output-f-vocab-file",  type=str)
    argparser.add_argument("-wo",   "--write-output-vocab-file",    type=str)


    argparser.add_argument("-ttf",  "--write-t-train-file",         type=str)
    argparser.add_argument("-tvf",  "--write-t-valid-file",         type=str)
    argparser.add_argument("-ttwf", "--write-t-train-w-file",       type=str)
    argparser.add_argument("-tvwf", "--write-t-valid-w-file",       type=str)

    argparser.add_argument("-dtf",  "--write-d-train-file",         type=str)
    argparser.add_argument("-dvf",  "--write-d-valid-file",         type=str)
    argparser.add_argument("-dtwf", "--write-d-train-w-file",       type=str)
    argparser.add_argument("-dvwf", "--write-d-valid-w-file",       type=str)

    argparser.add_argument("-ftf",  "--write-f-train-file",         type=str)
    argparser.add_argument("-fvf",  "--write-f-valid-file",         type=str)
    argparser.add_argument("-ftwf", "--write-f-train-w-file",       type=str)
    argparser.add_argument("-fvwf", "--write-f-valid-w-file",       type=str)


    argparser.add_argument("-n",    "--target-vector-size",         type=int)
    argparser.add_argument("-m",    "--source-vector-size",         type=int)
    argparser.add_argument("-vs",   "--valid-data-size",            type=int)
    argparser.add_argument("-mj",   "--max-jump-size",              type=int)
    argparser.add_argument("-mf",   "--max-fertility",              type=int)
=======
    argparser.add_argument("-wo",   "--write-output-vocab-file",    type=str)
    argparser.add_argument("-tf",   "--write-train-file",           type=str)
    argparser.add_argument("-vf",   "--write-valid-file",           type=str)
    argparser.add_argument("-twf",  "--write-train-w-file",         type=str)
    argparser.add_argument("-vwf",  "--write-valid-w-file",         type=str)
    argparser.add_argument("-n",    "--target-vector-size",         type=int)
    argparser.add_argument("-m",    "--source-vector-size",         type=int)
    argparser.add_argument("-vs",   "--valid-data-size",            type=int)
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
    argparser.add_argument("-v",    "--verbosity-level",            type=int,
                                                                    default=1,
                                                                    choices=(0, 1, 2))
    args = argparser.parse_args()

    if args.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)


    m = args.source_vector_size
    n = args.target_vector_size
    k = m / 2

<<<<<<< HEAD
    input_vocab, output_vocab = preparing.create_vocabularies(
        args.source_vocab,
        args.target_vocab,
        args.write_input_vocab_file,
        args.write_output_vocab_file
    )
    _, jump_vocab = preparing.create_jump_o_vocab(args.max_jump_size, args.write_output_j_vocab_file)
    _, fert_vocab = preparing.create_fert_o_vocab(args.max_fertility, args.write_output_f_vocab_file)


    train_data = ([], [], []) # T,D,F examples
    valid_data = ([], [], [])

=======

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
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

    with open(args.input_data, "rb") as i_fl:
        for lineno, line in enumerate(i_fl):

<<<<<<< HEAD
            if lineno < args.valid_data_size:
                t_model_examples, d_model_examples, f_model_examples = valid_data
            else:
                t_model_examples, d_model_examples, f_model_examples = train_data

            if lineno % 10000 == 0:
                logging.info("Extracting examples. Sentence %d." % lineno)
=======
            if lineno % 10000 == 0:
                logging.info("Sentence %d. Example extracted." % lineno)
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

            source, target, alignment = line.rstrip().split(" ||| ")
            source = ["S_" + w for w in source.split()]
            target = ["T_" + w for w in target.split()]
            alignment = [(int(a_s),int(a_t)) for a_s, a_t in
                         [a.split("-") for a in alignment.split()]]
<<<<<<< HEAD
            t_alignment = {a_t:a_s for a_s, a_t in alignment}
            t_alignment[-1] = -1

            # Extracting examples for T-Model.
            for t_i in xrange(len(target)):
                t_history = []
                s_window = []
                for n_i in xrange(1, n):
                    t_j = t_i - n_i
                    if t_j < 0:
                        t_history.append(preparing.T_BEGIN)
                    else:
                        t_history.append(target[t_j])
                s_i = t_alignment[t_i]
                for k_i in xrange(-k, k + 1):
                    s_j = s_i + k_i
                    if s_j < 0:
                        s_window.append(preparing.S_BEGIN)
                    elif s_j >= len(source):
                        s_window.append(preparing.S_END)
                    else:
                        s_window.append(source[s_j])
                # Example for modeling P(t_i|t_{i-1}, ..., t_{i-n+1}, s_A_i-k, ..., s_A_i+k)
                t_example = [target[t_i], t_history + s_window]
                t_model_examples.append(t_example)

            # Extracting examples for D-Model.
            for t_i in xrange(-1, len(target)-1):
                t_history = []
                s_window = []
                for n_i in xrange(1, n):
                    t_j = t_i - n_i
                    if t_j < 0:
                        t_history.append(preparing.T_BEGIN)
                    else:
                        t_history.append(target[t_j])
=======

            t_alignment = [a_s for a_s, a_t in alignment]

            for t_i in xrange(len(target)):
                example_in = []

                for k_i in xrange(1, n):
                    t_j = t_i - k_i
                    if t_j < 0:
                        example_in.append(T_BEGIN)
                    else:
                        example_in.append(target[t_j])

>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
                s_i = t_alignment[t_i]
                for k_i in xrange(-k, k + 1):
                    s_j = s_i + k_i
                    if s_j < 0:
<<<<<<< HEAD
                        s_window.append(preparing.S_BEGIN)
                    elif s_j >= len(source):
                        s_window.append(preparing.S_END)
                    else:
                        s_window.append(source[s_j])

                s_i_next = t_alignment[t_i + 1]
                jump = s_i_next - s_i
                if abs(jump) <= args.max_jump_size:
                    # Example for modeling P(jump|t_{i-1}, ..., t_{i-n+1}, s_A_i-k, ..., s_A_i+k)
                    d_example = ["J_" + str(jump), t_history + s_window]
                    d_model_examples.append(d_example)

            # Extracting examples for F-Model.
            for s_i in xrange(len(source)):
                fert = 0
                s_window = []
                for a_s, _ in alignment:
                    if a_s == s_i:
                        fert += 1
                if fert > args.max_fertility:
                    fert = args.max_fertility
                for k_i in xrange(-k, k + 1):
                    s_j = s_i + k_i
                    if s_j < 0:
                        s_window.append(preparing.S_BEGIN)
                    elif s_j >= len(source):
                        s_window.append(preparing.S_END)
                    else:
                        s_window.append(source[s_j])

                f_example = ["F_" + str(fert), s_window]
                f_model_examples.append(f_example)


        logging.info("Sentence %d. Example extracted." % lineno)


        logging.info("Replacing unknown words.")

        preparing.replace_unks(train_data[0], input_vocab, output_vocab)
        preparing.replace_unks(train_data[1], input_vocab, jump_vocab)
        preparing.replace_unks(train_data[2], input_vocab, fert_vocab)

        preparing.replace_unks(valid_data[0], input_vocab, output_vocab)
        preparing.replace_unks(valid_data[1], input_vocab, jump_vocab)
        preparing.replace_unks(valid_data[2], input_vocab, fert_vocab)


        logging.info("Writing T-model data.")
        preparing.write_data(
            train_data[0],
            valid_data[0],
            args.write_t_train_file,
            args.write_t_valid_file,
            args.write_t_train_w_file,
            args.write_t_valid_w_file,
            input_vocab,
            output_vocab)

        logging.info("Writing D-model data.")
        preparing.write_data(
            train_data[1],
            valid_data[1],
            args.write_d_train_file,
            args.write_d_valid_file,
            args.write_d_train_w_file,
            args.write_d_valid_w_file,
            input_vocab,
            jump_vocab)

        logging.info("Writing F-model data.")
        preparing.write_data(
            train_data[2],
            valid_data[2],
            args.write_f_train_file,
            args.write_f_valid_file,
            args.write_f_train_w_file,
            args.write_f_valid_w_file,
            input_vocab,
            fert_vocab)
=======
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

>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

