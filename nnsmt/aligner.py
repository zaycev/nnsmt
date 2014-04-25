#!/usr/bin/env python
# coding: utf-8
# Author: Vova Zaytsev <zaytsev@usc.edu>

"""This script modifies input word alignment according to the Affiliation heuristic:
* If t_i aligns to exactly one source word, A_i is the index of the word it aligns to.
* If t_i align to multiple source words, A_i is the index of the aligned word in the middle (round
down).
* If t_i is unaligned, we inherit its affiliation from the closest aligned word, starting with the right.
"""

import sys
import logging
import argparse
import datetime

import alignment

HEURISCICS = {
    "affiliation": alignment.AffilationHeuristicAligner
}

DEFAULT_HEURISTIC = HEURISCICS.keys()[0]



if __name__ == "__main__":
    
    t_start = datetime.datetime.now()
    
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
        
    
    logging.info("Source file: %s" % arguments.source_text)
    logging.info("Target file: %s" % arguments.target_text)
    logging.info("Alignment file: %s" % arguments.alignment)

    s_file = open(arguments.source_text, "rb")
    t_file = open(arguments.target_text, "rb")
    a_file = open(arguments.alignment,   "rb")
    train_data = alignment.iter_train_data(s_file, t_file, a_file)

    heuristic = HEURISCICS.get(arguments.heuristic)

    for i, (source, target, alignment) in enumerate(train_data):
        
        # print source
        
        if i % 10000 == 0:
            logging.info("Processed %d lines." % i)
        
        pp_aligment = heuristic.post_process(source, target, alignment)
        
        if pp_aligment is None:
            logging.info("[%d] Cannot apply heuristic: '%s', '%s', %r. Skip." % (
                i,
                " ".join(source),
                " ".join(target),
                alignment)
            )
            continue
        
        target_s = " ".join(target)
        source_s = " ".join(source)
        alignment_s = " ".join(["%d-%d" % a for a in pp_aligment])
        sys.stdout.write("%s ||| %s ||| %s\n" % (source_s, target_s,  alignment_s))
        

    t_end = datetime.datetime.now()

    logging.info("Processed %d lines." % i)
    logging.info("Finished after %d seconds." % (t_end - t_start).seconds)
