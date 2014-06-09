Word Bases MT System with NN
============================

#### Generative Story

```
1. i <- 1, j <- 0
2. Choose \delta j from [-h, h] with the following probability:
	 P_d(\delta j | f_{j - h}, ..., f_{j+h}, e_{i-g}, ..., e_{i + j})
3. Let j <- j + \delta j
4. Generate e_i with probability:
    P_t(e_i | f_{j - h}, ..., f_{j+h}, e_{i-g}, ..., e_{i + j})
5. If e_i = </s>, stop; otherwise go to 2.
```

### 0. Data Preparation

Input data is Target-Source parallel corpus, word-aligned using GIZA++. You can test this MT pipeline with a sample dataset stored in contrib `directory`.

Before run the training pipeline, first open `sbin/run-env.sh` and change environment variables `WORK_DIR` to make it point to your working directory path.


### 1. Word Alignment

Word alignments are given (generated by GIZA++ or any other tool), but our model requires that every target word has to be aligned with exactly one not null source word. The algorithm of PP rules is explained in [4,3], here is a brief idea:

**Affiliation Heuristic**
* If `t_i` aligns to exactly one source word, `A_i` is the index of the word it aligns to.
* If `t_i` align to multiple source words, `A_i` is the index of the aligned word in the middle (round
down).
* If `t_i` is unaligned, we inherit its affiliation from the closest aligned word, starting with the right.

**Run word aligner**

* Use script `./run-align.sh`.

Or:

```
cd ./sbin/
source run-env.sh
$PYTHON $ROOT/nnsmt/aligner.py          \
    --source-text $TRAIN_SRC_TEXT       \
    --target-text $TRAIN_TRG_TEXT       \
    --alignment   $TRAIN_ALIGNMENT      \
    --giza-source-vocab $GIZA_SRC_VC    \
    --giza-target-vocab $GIZA_TRG_VC    \
    --heuristic "affiliation-pp"        \
    --verbosity-level 1                 \
    > $WORK_DIR/pp-alignment.txt
```

The result file will contain target sentence, source sentence and new alignment on every line, separated by ` ||| ` . For example:
```
wiederaufnahme der sitzungsperiode ||| resumption of the session ||| 0-0 1-1 1-2 2-3
die aussprache ist geschlossen . ||| the debate is closed . ||| 0-0 1-1 2-2 3-3 4-4
...
```


### 2. Training MT Model

Generate training examples for the distortion and translation model.
Train the neural networks using NPLM toolkit.

### 3. Decoding

The design of the decoder would be very similar to a phrase-based decoder, except that we only generate a single English word at a time.

### Related Links

1. N. Durrani, A. Fraser, H. Schmid. 2013. [Model With Minimal Translation Units, But DecodeWith Phrases](http://www.cis.uni-muenchen.de/~fraser/pubs/durrani_naacl2013.pdf)
2. H. Zhang, K. Toutanova, C. Quirk, J. Gao. 2013. [Beyond Left-to-Right: Multiple Decomposition Structures for SMT](http://research.microsoft.com/en-us/um/people/jfgao/paper/2013/mtu.pdf)
3. N. Durrani, H. Schmid, A. Fraser. 2011. [A Joint Sequence Translation Model with Integrated Reordering](http://aclweb.org/anthology//P/P11/P11-1105.pdf)
4. J. Devlin, R. Zbib, Z. Huang, T. Lamar, R. Schwartz, J. Makhoul. 2014. Fast and Robust Neural Network Joint Models for Statistical Machine Translation.

