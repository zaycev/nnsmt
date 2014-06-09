#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

import sys
import logging
import argparse
import datetime
import decoding

sys.path.append("/Users/zvm/code/nnsmt/build/python")

if __name__ == "__main__":

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("--t-model-fl",          type=str)
    argparser.add_argument("--d-model-fl",          type=str)
    argparser.add_argument("--f-model-fl",          type=str)
    argparser.add_argument("--i-vocab-fl",          type=str)
    argparser.add_argument("--o-t-vocab-fl",        type=str)
    argparser.add_argument("--o-d-vocab-fl",        type=str)
    argparser.add_argument("--o-f-vocab-fl",        type=str)
    argparser.add_argument("--observed-data",       type=str)
    argparser.add_argument("--train-file",          type=str)
    argparser.add_argument("--target-vector-size",  type=int)
    argparser.add_argument("--source-vector-size",  type=int)
    argparser.add_argument("--max-jump",            type=int)
    argparser.add_argument("--max-fert",            type=int)
    argparser.add_argument("--t-cache-size",        type=int)
    argparser.add_argument("--verbosity-level",     type=int,
                                                    default=1,
                                                    choices=(0, 1, 2))
    args = argparser.parse_args()

    if args.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)

    zdec = decoding.ZDecoder.load(t_model_fl=args.t_model_fl,
                                  d_model_fl=args.d_model_fl,
                                  f_model_fl=args.f_model_fl,
                                  i_vocab_fl=args.i_vocab_fl,
                                  o_t_vocab_fl=args.o_t_vocab_fl,
                                  o_d_vocab_fl=args.o_d_vocab_fl,
                                  o_f_vocab_fl=args.o_f_vocab_fl,
                                  s_size=args.source_vector_size,
                                  t_size=args.target_vector_size,
                                  max_jump=args.max_jump,
                                  max_fert=args.max_fert,
                                  observed_data_fl=args.observed_data,
                                  t_weight=1.00,
                                  d_weight=1.00,
                                  f_weight=3.00,
                                  t_cache_size=args.t_cache_size)

    # zdec.self_test(32, args.train_file)
    # exit(0)

    for i, line in enumerate(sys.stdin):
        line = line.rstrip()
        source = line.split()
        score, target = zdec.decode(source, beam_n=100)
        print "%d %.8f %s" % (i, score, " ".join(target))