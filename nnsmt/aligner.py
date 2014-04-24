#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

"""
"""

import sys
import logging
import heuristics


class AffilationHeuristicAligner(object):
    """
    """
    
    def __ini__(self):
        pass



HEURISCICS = {
    "affiliation": AffilationHeuristicAligner
}

DEFAULT_HEURISTIC = HEURISCICS.keys()[0]



if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-a", "--alignment",         type=str)
    argparser.add_argument("-s", "--source-text",       type=str)
    argparser.add_argument("-t", "--target-text",       type=str)
    argparser.add_argument("-g", "--heuristic",         type=str,
                                                        default=DEFAULT_HEURISTIC,
                                                        choices=HEURISCICS.keys())
    argparser.add_argument("-v", "--verbosity-level",   type=int, default=1, choices=(0, 1, 2))
    arguments = arg_parser.parse_args()

    if arguments.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)

    a_file = open(arguments.alignment,   "rb")
    s_file = open(arguments.source_text, "rb")
    t_file = open(arguments.target_text, "rb")

    a_reader = giza.GizaAlignmentReader(a3_file)

    heuristic = HEURISCICS.get(arguments.heuristic)(s_vcb, t_vcb, arguments)

    for aligment in a_reader:
        pp_aligment = heuristic.post_process(aligment)
