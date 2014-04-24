#!/usr/bin/env python
# coding: utf-8
# Author: Vladimir M. Zaytsev <zaytsev@usc.edu>

"""
"""

import sys
import giza
import logging
import argparse
import heuristics


HEURISCICS = {
    "durani-pp": heuristics.DuraniPPHeuristic, #
}


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-a3", "--giza-a3-file",      type=str)
    argparser.add_argument("-sv", "--source-vocabulary", type=str)
    argparser.add_argument("-tv", "--target-vocabulary", type=str)
    argparser.add_argument("-o",  "--output-path",       type=str)
    argparser.add_argument("-h",  "--heuristic",         type=str, default="durani-pp", choices=HEURISCICS.keys())
    argparser.add_argument("-v",  "--verbosity-level",   type=int, default=1,           choices=(0, 1, 2))
    arguments = arg_parser.parse_args()

    if arguments.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)

    a3_file = open(arguments.giza_a3_file, "rb")
    s_vcb = giza.load_vcb(arguments.source_vocabulary)
    t_vcb = giza.load_vcb(arguments.target_vocabulary)

    a_reader = giza.GizaAlignmentReader(a3_file)

    heuristic = HEURISCICS.get(arguments.heuristic)(s_vcb, t_vcb, arguments)

    for aligment in a_reader:
        pp_aligment = heuristic.post_process(aligment)
