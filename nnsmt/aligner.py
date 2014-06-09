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
<<<<<<< HEAD
    "affiliation":    alignment.AffilationHeuristicAligner,
    "affiliation-pp": alignment.AffilationPPHeuristicAligner
=======
    "affiliation": alignment.AffilationHeuristicAligner
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
}

DEFAULT_HEURISTIC = HEURISCICS.keys()[0]



if __name__ == "__main__":
<<<<<<< HEAD

    t_start = datetime.datetime.now()

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-a", "--alignment",             type=str)
    argparser.add_argument("-sv", "--giza-source-vocab",    type=str)
    argparser.add_argument("-tv", "--giza-target-vocab",    type=str)
    argparser.add_argument("-s", "--source-text",           type=str)
    argparser.add_argument("-t", "--target-text",           type=str)
    argparser.add_argument("-g", "--heuristic",             type=str,
                                                            default=DEFAULT_HEURISTIC,
                                                            choices=HEURISCICS.keys())
    argparser.add_argument("-v", "--verbosity-level",       type=int, default=1, choices=(0, 1, 2))
=======
    
    t_start = datetime.datetime.now()
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-a", "--alignment",         type=str)
    argparser.add_argument("-s", "--source-text",       type=str)
    argparser.add_argument("-t", "--target-text",       type=str)
    argparser.add_argument("-g", "--heuristic",         type=str,
                                                        default=DEFAULT_HEURISTIC,
                                                        choices=HEURISCICS.keys())
    argparser.add_argument("-v", "--verbosity-level",   type=int, default=1, choices=(0, 1, 2))
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
    arguments = argparser.parse_args()

    if arguments.verbosity_level > 0:
        logging.basicConfig(level=logging.INFO)
<<<<<<< HEAD

    logging.info("Source file: %s" % arguments.source_text)
    logging.info("Target file: %s" % arguments.target_text)
    logging.info("Source vocab: %s" % arguments.giza_source_vocab)
    logging.info("Target vocab: %s" % arguments.giza_target_vocab)
=======
        
    
    logging.info("Source file: %s" % arguments.source_text)
    logging.info("Target file: %s" % arguments.target_text)
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
    logging.info("Alignment file: %s" % arguments.alignment)

    s_file = open(arguments.source_text, "rb")
    t_file = open(arguments.target_text, "rb")
    a_file = open(arguments.alignment,   "rb")
<<<<<<< HEAD
    t_vocab = alignment.load_giza_vcb(arguments.giza_target_vocab)
    s_vocab = alignment.load_giza_vcb(arguments.giza_source_vocab)
    train_data = alignment.iter_train_data(s_file, t_file, a_file)
    heuristic = HEURISCICS.get(arguments.heuristic)(t_vocab=t_vocab, s_vocab=s_vocab)

    for i, (source, target, alignment) in enumerate(train_data):

        if i % 10000 == 0:
            logging.info("Processed %d lines." % i)

        pp_aligment = heuristic.post_process(source, target, alignment)

=======
    train_data = alignment.iter_train_data(s_file, t_file, a_file)

    heuristic = HEURISCICS.get(arguments.heuristic)

    for i, (source, target, alignment) in enumerate(train_data):
        
        # print source
        
        if i % 10000 == 0:
            logging.info("Processed %d lines." % i)
        
        pp_aligment = heuristic.post_process(source, target, alignment)
        
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        if pp_aligment is None:
            logging.info("[%d] Cannot apply heuristic: '%s', '%s', %r. Skip." % (
                i,
                " ".join(source),
                " ".join(target),
                alignment)
            )
            continue
<<<<<<< HEAD

=======
        
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01
        target_s = " ".join(target)
        source_s = " ".join(source)
        alignment_s = " ".join(["%d-%d" % a for a in pp_aligment])
        sys.stdout.write("%s ||| %s ||| %s\n" % (source_s, target_s,  alignment_s))
<<<<<<< HEAD
=======
        
>>>>>>> 58fe451a4af3d21f0a8579955cf3cae8993f8a01

    t_end = datetime.datetime.now()

    logging.info("Processed %d lines." % i)
    logging.info("Finished after %d seconds." % (t_end - t_start).seconds)
