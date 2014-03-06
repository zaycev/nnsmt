# coding: utf-8
# Author: Vladimir M. Zaytsev <zaytsev@usc.edu>


def load_vcb(vcb_file_path):
    """
    Function which loads vocabulary into `dict` object.

    ```
        A. VOCABULARY FILES
        -------------------
        Each entry is stored on one line as follows:

         uniq_id1 string1 no_occurrences1
         uniq_id2 string2 no_occurrences2
         uniq_id3 string3 no_occurrences3
         ....

        Here is a sample from an English vocabulary file:

        627 abandon 10
        628 abandoned 17
        629 abandoning 2
        630 abandonment 12
        631 abatement 8
        632 abbotsford 2

        uniq_ids are sequential positive integer numbers.  0 is reserved for
        the special token NULL.
    ```

    Format is also described here: http://goo.gl/nFFvE8
    """
    vcb = {}
    with open(vcb_file_path, "rb") as vcb_file:
        for i, line in eunmerate(vcb_file):
            line = line.rstrip("\n")
            row = line.split()  # splits into (#, word, freq)
            vcb[row[1]] = row[2]
    logging.info("Loaded %d entries from %s." % vcb_file_path)
    return vcb

class GizaAlignmentReader(object):
    """
    This class is responsible for reading GIZA++ aliglignment (A3) files.

    A3 File Format:

    ```
        ALIGNMENT FILE ( *.A3.* )

        In each iteration of the training, and for each sentence pair in the
        training set, the best alignment (viterbi alignment) is written to the
        alignment file (if the dump parameters are set accordingly). The
        alignment file is named prob_table.An.i, where n is the model number
        ({1,2, 2to3, 3 or 4}), and i is the iteration number. The format of
        the alignments file is illustrated in the following sample:

        # Sentence pair (1)
        il s' agit de la même société qui a changé de propriétaires
        NULL ({ }) UNK ({ }) UNK ({ }) ( ({ }) this ({ 4 11 }) is ({ }) the ({ }) same ({ 6 }) agency ({ }) which
        ({ 8 }) has ({ }) undergone ({ 1 2 3 7 9 10 12 }) a ({ }) change ({ 5 }) of ({ }) UNK ({ })
        # Sentence pair (2)
        UNK UNK , le propriétaire , dit que cela s' est produit si rapidement qu' il n' en connaît pas la cause exacte
        NULL ({ 4 }) UNK ({ 1 2 }) UNK ({ }) , ({ 3 }) the ({ }) owner ({ 5 22 23 }) , ({ 6 }) says ({ 7 8 }) it ({ })
        happened ({ 10 11 12 }) so ({ 13 }) fast ({ 14 19 }) he ({ 16 }) is ({ }) not ({ 20 }) sure ({ 15 17 }) what
        ({ }) went ({ 18 21 }) wrong ({ 9 })

        The alignment file is represented by three lines for each sentence
        pair. The first line is a label that can be used, e.g., as a caption
        for alignment visualization tools.  It contains information about the
        sentence sequential number in the training corpus, sentence lengths,
        and alignment probability. The second line is the target sentence, the
        third line is the source sentence. Each token in the source sentence
        is followed by a set of zero or more numbers. These numbers represent
        the positions of the target words to which this source word is
        connected, according to the alignment.
    ```

    Format is also described here: http://goo.gl/nFFvE8
    """
    def __init__(self, a3_stream):
        pass

    def __iter__(self):
        for line in self.a3_stream:
            yield line