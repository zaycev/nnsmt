#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

S_BEGIN = "<S>"
S_END = "</S>"
T_BEGIN = "<T>"
T_END = "</T>"
S_UNK = "<S_UNK>"
T_UNK = "<T_UNK>"


def create_vocabularies(s_vocab_fl, t_vocab_fl, i_vocab_fl, o_vocab_fl):

    with open(s_vocab_fl, "rb") as fl:
        source_vocab = [S_BEGIN, S_END, S_UNK]
        source_vocab.extend(("S_" + w for w in fl.read().rstrip().split("\n")[4:]))
    with open(t_vocab_fl, "rb") as fl:
        target_vocab = [T_BEGIN, T_END, T_UNK]
        target_vocab.extend(("T_" + w for w in fl.read().rstrip().split("\n")[4:]))
    i2w_i_vocab = target_vocab + source_vocab
    i2w_o_vocab = target_vocab
    i_vocab = {}
    o_vocab = {}
    with open(i_vocab_fl, "wb") as vocab_fl:
        for i in xrange(len(i2w_i_vocab)):
            w = i2w_i_vocab[i]
            i_vocab[w] = i
            vocab_fl.write(w)
            vocab_fl.write("\n")
    with open(o_vocab_fl, "wb") as vocab_fl:
        for i in xrange(len(i2w_o_vocab)):
            w = i2w_o_vocab[i]
            o_vocab[w] = i
            vocab_fl.write(w)
            vocab_fl.write("\n")
    return i_vocab, o_vocab


def read_vocab_file(vocab_fl):
    i2w_vocab = None
    w2i_vocab = None
    with open(vocab_fl, "rb") as fl:
        i2w_vocab = fl.read().rstrip().split("\n")
        w2i_vocab = {w: i for i, w in enumerate(i2w_vocab)}
    return i2w_vocab, w2i_vocab


def create_jump_o_vocab(window_size=6, save_to=None):
    i2w_vocab = []
    w2i_vocab = {}
    for i, j in enumerate(xrange(-window_size, window_size + 1)):
        j_word = "J_" + str(j)
        i2w_vocab.append(j_word)
        w2i_vocab[j_word] = i
    if save_to is not None:
        with open(save_to, "wb") as fl:
            for j_word in i2w_vocab:
                fl.write(j_word)
                fl.write("\n")
    return i2w_vocab, w2i_vocab


def create_fert_o_vocab(max_fert=6, save_to=None):
    i2w_vocab = []
    w2i_vocab = {}
    for i, j in enumerate(xrange(0, max_fert + 1)):
        j_word = "F_" + str(j)
        i2w_vocab.append(j_word)
        w2i_vocab[j_word] = i
    if save_to is not None:
        with open(save_to, "wb") as fl:
            for j_word in i2w_vocab:
                fl.write(j_word)
                fl.write("\n")
    return i2w_vocab, w2i_vocab


def replace_unks(data, i_vocab, o_vocab):
    for i in xrange(len(data)):
        o_word, i_words = data[i]
        if o_word not in o_vocab:
            if o_word.startswith("T_"):
                data[i][0] = T_UNK
            else:
                raise ValueError("Strange word '%s'" % o_word)
        for j in xrange(len(i_words)):
            if i_words[j] not in i_vocab:
                if i_words[j].startswith("S_"):
                    i_words[j] = S_UNK
                elif i_words[j].startswith("T_"):
                    i_words[j] = T_UNK
                else:
                    raise ValueError("Strange word '%s'" % i_words[j])


def write_data(train_data,
               valid_data,
               train_file,
               valid_file,
               train_w_file,
               valid_w_file,
               i_vocab,
               o_vocab):
    train_fl = open(train_file, "wb")
    train_w_fl = open(train_w_file, "wb")
    for o_word, i_words in train_data:
        train_w_fl.write(" ".join(i_words))
        train_w_fl.write(" ")
        train_w_fl.write(o_word)
        train_w_fl.write("\n")
        train_fl.write(" ".join(map(str, map(i_vocab.get, i_words))))
        train_fl.write(" ")
        train_fl.write(str(o_vocab[o_word]))
        train_fl.write("\n")

    valid_fl = open(valid_file, "wb")
    valid_w_fl = open(valid_w_file, "wb")
    for o_word, i_words in valid_data:
        valid_w_fl.write(" ".join(i_words))
        valid_w_fl.write(" ")
        valid_w_fl.write(o_word)
        valid_w_fl.write("\n")
        valid_fl.write(" ".join(map(str, map(i_vocab.get, i_words))))
        valid_fl.write(" ")
        valid_fl.write(str(o_vocab[o_word]))
        valid_fl.write("\n")

    train_fl.close()
    train_w_fl.close()
    valid_fl.close()
    valid_w_fl.close()
