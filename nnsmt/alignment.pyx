#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

"""
"""

import sys
import logging
import argparse
import itertools

class AffilationHeuristicAligner(object):
    """
    """
    
    def __ini__(self):
        pass


def iter_train_data(source_sents_fl, target_sents_fl, a3_fl):
    for s_line, t_line, a_line in itertools.izip(source_sents_fl, target_sents_fl, a3_fl):
        source = s_line.rstrip().split()
        target = s_line.rstrip().split()
        alignment = [(int(a_s), int(a_t)) for a_s,a_t in [a.split("-") for a in a_line.rstrip().split()]]
        yield source, target, alignment

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
    arguments = argparser.parse_args()

    if arguments.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)

    s_file = open(arguments.source_text, "rb")
    t_file = open(arguments.target_text, "rb")
    a_file = open(arguments.alignment,   "rb")
    train_data = iter_train_data(s_file, t_file, a_file)

    heuristic = HEURISCICS.get(arguments.heuristic)()

    for i, (source, target, alignment) in enumerate(train_data):
        
        print source
        
        if i % 10000 == 0:
            logging.info("Processed %d lines." % i)
        
        # pp_aligment = heuristic.process(aligment)

    logging.info("Processed %d lines." % i)
    logging.info("Finished.")
