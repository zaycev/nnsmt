#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import sys
import logging
import argparse
import datetime
import decoding

if __name__ == "__main__":

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("-t",    "--t-model-fl",                 type=str)
    argparser.add_argument("-d",    "--d-model-fl",                 type=str)
    argparser.add_argument("-f",    "--f-model-fl",                 type=str)
    argparser.add_argument("-iv",   "--i-vocab-fl",                 type=str)
    argparser.add_argument("-ov",   "--o-vocab-fl",                 type=str)
    argparser.add_argument("-od",   "--observed-data",              type=str)
    argparser.add_argument("-n",    "--target-vector-size",         type=int)
    argparser.add_argument("-m",    "--source-vector-size",         type=int)
    argparser.add_argument("-v",    "--verbosity-level",            type=int,
                                                                    default=1,
                                                                    choices=(0, 1, 2))
    args = argparser.parse_args()

    if args.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)

    zdec = decoding.ZDecoder.load(t_model_fl=args.t_model_fl,
                                  d_model_fl=args.d_model_fl,
                                  f_model_fl=args.f_model_fl,
                                  i_vocab_fl=args.i_vocab_fl,
                                  o_vocab_fl=args.o_vocab_fl,
                                  s_size=args.source_vector_size,
                                  t_size=args.target_vector_size,
                                  observed_data_fl=args.observed_data)

    zdec.self_test(32, args.observed_data)
    exit(0)
    target = zdec.decode("ich kann glas essen".split())

    # for line in sys.stdin:
    #     line = line.rstrip()
    #     source = line.split()
    #     target = zdec.decode(source)
    #     # print source, target
    #     break