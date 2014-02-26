NNSMT Translation Model
=======================


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

### 1. Word Alignment

Word alignments are given. Some heuristic need to be used to make one-to-one alignments.

### 2. Training

Generate training examples for the distortion and translation model.
Train the neural networks using NPLM toolkit.

### 3. Decoding

The design of the decoder would be very similar to a phrase-based decoder, except that we only generate a single English word at a time.

### Related Links
	
* N. Durrani, A. Fraser, H. Schmid [Model With Minimal Translation Units, But DecodeWith Phrases](http://www.cis.uni-muenchen.de/~fraser/pubs/durrani_naacl2013.pdf)

