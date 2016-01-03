#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
  

#=====================================================================
#                    Noise
#=====================================================================
def switch_cls(given, couple):
    if given == couple[0]:
        return couple[1]
    return couple[0]
    

def split_to_folds(seq, num=10):
    seq = list(seq)
    random.shuffle(seq)
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    
    return tuple(tuple(x) for x in out)

    
def noise(fold, rate, classes):
    return [ex[:-1] + [noisy_class(ex[-1], rate, classes)] for ex in fold]
    

def noisy_class(orig_classification, rate, classes):
    rand = random.uniform(0, 1)
    if rand > rate:
        return orig_classification
    return switch_cls(orig_classification, classes)


''' get_noisy_folds parameters:
    @examples: a list of examples. each example is assumed to be a list which
        its last element is the (binary) classification of the example, and all
        the precedings elements are the feature-values of the example.
    @noise_rate: the probability to switch the classification of an example
        when creating the noisy-folds.
    @classes: a 2-tuple containing the names of the two optional
        classifications of the examples.
'''  
def get_noisy_folds(examples, noise_rate=0.3, classes=(1,0)):
    folds = split_to_folds(examples)
    noisy_folds = [noise(fold, noise_rate, classes) for fold in folds]
    return noisy_folds, folds

