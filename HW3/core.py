from get_features import get_ads_features
from noise import get_noisy_folds
import numpy as np
from sklearn import tree
import random
from math import ceil, floor, log2
from time import clock
import pickle
from enum import Enum

class SubsetType(Enum):
    features = 1
    examples = 2


class FeatureChooserType(Enum):
    IG = 1
    Random = 2
    Semi_Random = 3


def get_ad_dataset():
     # Load ad dataset
    ad_dataset_file = 'ad-dataset/ad.data'
    ad_dataset = np.genfromtxt(ad_dataset_file, delimiter=',', dtype=str)
    ad_dataset[ad_dataset == 'ad.'] = 1
    ad_dataset[ad_dataset == 'nonad.'] = 0
    ads_features = get_ads_features(201239480, 302629605)
    ads_features += [np.shape(ad_dataset)[1]-1]
    ad_dataset = ad_dataset[:, ads_features].astype(int)
    ad_dataset = ad_dataset.tolist()

    return get_noisy_folds(ad_dataset)


def get_har_dataset():
    # Load HAR dataset
    har_dataset_file = 'UCI HAR Dataset/train/X_train.txt'
    har_labels_file = 'UCI HAR Dataset/train/y_train.txt'
    har_dataset = np.genfromtxt(har_dataset_file, dtype=float)
    har_labels = np.genfromtxt(har_labels_file, dtype=int)
    har_labels[har_labels <= 3] = 1     # replace moving labels
    har_labels[har_labels >= 4] = 0     # replace resting labels
    har_labels.shape = (-1, 1)
    har_dataset = np.concatenate((har_dataset, har_labels), axis=1)
    har_dataset = har_dataset.tolist()

    return get_noisy_folds(har_dataset)


def dump_data_sets_to_file():
    ad_noisy_folds, ad_folds = get_ad_dataset()
    har_noisy_folds, har_folds = get_har_dataset()
    pickle.dump(ad_folds, open("ad_folds.p", "wb"))
    pickle.dump(ad_noisy_folds, open("ad_noisy_folds.p", "wb"))
    pickle.dump(har_folds, open("har_folds.p", "wb"))
    pickle.dump(har_noisy_folds, open("har_noisy_folds.p", "wb"))


def load_data_sets():
    ad_folds = pickle.load(open("ad_folds.p", "rb"))
    ad_noisy_folds = pickle.load(open("ad_noisy_folds.p", "rb"))
    har_folds = pickle.load(open("har_folds.p", "rb"))
    har_noisy_folds = pickle.load(open("har_noisy_folds.p", "rb"))
    return ad_folds, ad_noisy_folds, har_folds, har_noisy_folds


def fit(examples, classifications, features_idx_list, features_classifier, min_samples_leaf=4):
    # recursive function. builds a tree in the format [left_son, feature_idx, right_son],
    #    with the classification 0 or 1 in the leaves
    count = sum(classifications)

    # if all the classification are the same, return the class
    if count == len(classifications):
        return 1
    if count == 0:
        return 0

    # loop while the features are not meaningful (IG = 0)
    bad_feature = True
    while bad_feature:
        if len(examples) <= min_samples_leaf or len(features_idx_list) == 0:
            return round(float(count)/len(classifications))
        feature_idx = features_classifier(features_idx_list, examples, classifications)
        features_idx_list.remove(feature_idx)
        left_examples = []
        right_examples = []
        left_classifications = []
        right_classifications = []

        # split the example for the left and right sons
        for example, classification in zip(examples, classifications):
            if example[feature_idx]:
                left_examples.append(example)
                left_classifications.append(classification)
            else:
                right_examples.append(example)
                right_classifications.append(classification)

        # if the son is an empty list, return the father's classification
        if len(left_classifications) == 0 or len(right_classifications) == 0:
            bad_feature = True
        else:
            bad_feature = False
            left_son = fit(left_examples, left_classifications, features_idx_list, features_classifier)
            right_son = fit(right_examples, right_classifications, features_idx_list, features_classifier)

    return [left_son, feature_idx, right_son]


def classify_example(tree, example):
    if tree == 1 or tree == 0:
        return tree
    if example[tree[1]]:
        return classify_example(tree[0], example)
    return classify_example(tree[2], example)


def predict(tree, examples):
    return [classify_example(tree, example) for example in examples]


def calculate_entropy(classifications):
    num_classifications = len(classifications)
    if num_classifications == 0:
        return 0
    entropy_sum = 0
    pc0 = [c for c in classifications if c == 0]
    pc0 = float(len(pc0))/num_classifications
    pc1 = 1 - pc0
    if pc0 != 0:
        entropy_sum += pc0 * log2(pc0)
    if pc1 != 0:
        entropy_sum += pc1 * log2(pc1)

    return -entropy_sum


def calculate_ig(feature_idx, examples, classifications):
    entropy_sum = 0
    for feature_val in [0, 1]:
        e_i = [c for e, c in zip(examples, classifications) if e[feature_idx] == feature_val]
        if len(e_i) == 0:
            continue
        entropy_sum += (float(len(e_i))/len(examples)) * calculate_entropy(e_i)
    return calculate_entropy(classifications) - entropy_sum


def semi_random_feature_chooser(features, examples, classifications):
    features_ig = [calculate_ig(feature, examples, classifications) for feature in features]
    sum_prob = sum(features_ig)
    if sum_prob == 0:
        return random.choice(features)
    selected_prob = random.uniform(0, sum_prob)
    sum_ig_prob = 0
    for ig, f in zip(features_ig, features):
        sum_ig_prob += ig
        if selected_prob <= sum_ig_prob:
            return f
    return random.choice(features)


class FeaturesClassifier:
    def __init__(self, criterion, m):
        self.criterion = criterion
        self.tree = None
        self.m = m

    def classifier(self, features, examples, classifications):
        if self.criterion == FeatureChooserType.Random:
            return random.choice(features)
        elif self.criterion == FeatureChooserType.Semi_Random:
            return semi_random_feature_chooser(features, examples, classifications)

    def fit(self, examples, classifications, features_idx_list):
        if self.criterion == FeatureChooserType.IG:
            self.tree = tree.DecisionTreeClassifier(criterion="entropy", min_samples_leaf=self.m)
            return self.tree.fit(examples, classifications)
        else:
            self.tree = fit(examples, classifications, features_idx_list, self.classifier, self.m)
            return self

    def predict(self, examples):
        if self.tree == None:
            return None
        if self.criterion == FeatureChooserType.IG:
            return self.tree.predict(examples).tolist()
        else:
            return predict(self.tree, examples)


def k_fold_cross_validation(folds, noisy_folds, criteria, m):
    #mean_accuracy = 0.0
    features_set_size = len(folds[0][0])
    fold_size = len(folds)
    trees = []
    for test_fold_idx in range(fold_size):
        # train for all folds except for test_fold_idx
        X = []
        Y = []
        for train_fold_idx in range(fold_size):
            if train_fold_idx == test_fold_idx:
                continue
            X += [row[:-1] for row in noisy_folds[train_fold_idx]]
            Y += [row[-1] for row in noisy_folds[train_fold_idx]]
        classifier = FeaturesClassifier(criteria, m)
        tree = classifier.fit(X, Y, list(range(features_set_size)))
        '''
        # test for test_fold_idx
        X = [row[:-1] for row in folds[test_fold_idx]]
        Y = [row[-1] for row in folds[test_fold_idx]]
        results = tree.predict(X)
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        mean_accuracy += len(count)/float(len(results))
        '''
        trees += [tree]
    #mean_accuracy /= float(len(folds))
    return trees #, mean_accuracy


def select_random_features_subset(folds, noisy_folds, q):
    # folds are assumed to have the label as the last feature
    # select random features
    feature_set_size = len(noisy_folds[0][0])
    reduced_features_set_size = ceil(q*feature_set_size)
    features_range = list(range(feature_set_size-1))
    selected_features = random.sample(features_range, reduced_features_set_size)
    selected_features += [feature_set_size-1]
    reduced_features_noisy_folds = [[[row[f]for f in selected_features] for row in fold] for fold in noisy_folds]
    reduced_features_folds = [[[row[f]for f in selected_features] for row in fold] for fold in folds]
    return reduced_features_noisy_folds, reduced_features_folds


def select_random_examples_subset(folds, noisy_folds, p):
    # folds are assumed to have the label as the last feature
    # select random examples
    examples_set_size = len(noisy_folds[0])
    reduced_examples_set_size = ceil(p*examples_set_size)
    examples_range = list(range(examples_set_size))
    selected_examples = random.sample(examples_range, reduced_examples_set_size)
    reduced_examples_noisy_folds = [[fold[row] for row in selected_examples] for fold in noisy_folds]
    reduced_examples_folds = [[fold[row] for row in selected_examples] for fold in folds]
    return reduced_examples_noisy_folds, reduced_examples_folds


def learn_ensemble(folds, noisy_folds, ensemble_size, ensemble_type=(SubsetType.features, FeatureChooserType.IG)):
    p = 0.5            # train set size factor
    q = 0.5            # feature set size factor
    m = 8              # minimal number of examples in a leaf
    k = 10             # number of folds (defined by noise.py)

    # learn 10 ensemble trees
    trees = []
    reduced_noisy_folds = []
    reduced_folds = []
    num_folds = len(folds)
    for s in range(ensemble_size):
        # create the reduced folds
        if ensemble_type[0] == SubsetType.features:
            reduced_noisy_fold, reduced_fold = select_random_features_subset(folds, noisy_folds, q)
        else:
            reduced_noisy_fold, reduced_fold = select_random_examples_subset(folds, noisy_folds, p)
        reduced_folds.append(reduced_fold)
        reduced_noisy_folds.append(reduced_noisy_fold)
        # train k trees
        fold_trees = k_fold_cross_validation(reduced_fold, reduced_noisy_fold, ensemble_type[1], m)
        trees.append(fold_trees)

    # evaluate the accuracy of each ensemble for each fold and average the results
    mean_accuracy = 0
    for test_fold_idx in range(num_folds):
        # test for test_fold_idx
        results = []
        # labels should be the same for all trees (since we are taking the same examples)
        for s in range(ensemble_size):
            X = [row[:-1] for row in reduced_folds[s][test_fold_idx]]
            if ensemble_type[0] == SubsetType.features:
                Y = [row[-1] for row in reduced_folds[s][test_fold_idx]]
            else:
                Y = [row[-1] for row in folds[test_fold_idx]]
            labels = (trees[s][test_fold_idx]).predict(X)
            # sum up the labels predicted by all trees to a single vector
            if results == []:
                results = labels
            else:
                results = [x + y for x, y in zip(results, labels)]
        # take the average label (by dividing the sum by the ensemble size) and then round up to 1 or down to 0
        results = [round(label/ensemble_size) for label in results]
        # count number of matches between predicted label and true label
        count = [1 for i in range(len(results)) if results[i] == Y[i]]
        # sum up the prediction accuracy for the ensemble for each fold
        mean_accuracy += (len(count)/float(len(results)))
    # take the mean accuracy
    mean_accuracy /= float(num_folds)

    return mean_accuracy


def continuous_features_to_binary(folds):
    folds_new = []
    for fold in folds:
        fold_new = [[1*(val > 0) for val in row] for row in fold]
        folds_new += [fold_new]
    return folds_new


if __name__ == '__main__':
    dumpToFile = False
    if dumpToFile:
        dump_data_sets_to_file()
    else:
        ad_folds, ad_noisy_folds, har_folds, har_noisy_folds = load_data_sets()

        sizes = [5, 7, 9, 11, 13, 15]
        for subset_type in SubsetType:
            for features_chooser_type in FeatureChooserType:
                for ensemble_size in sizes:
                    start = clock()
                    mean_accuracy = learn_ensemble(ad_folds, ad_noisy_folds, ensemble_size, (subset_type, features_chooser_type))
                    print("Ad dataset, size: " + str(ensemble_size) + " type: " +
                          str(subset_type) + "-" + str(features_chooser_type) + " = " + str(mean_accuracy))
                    total_time = clock() - start
                    print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))

                    start = clock()
                    har_folds = continuous_features_to_binary(har_folds)
                    har_noisy_folds = continuous_features_to_binary(har_noisy_folds)
                    mean_accuracy = learn_ensemble(har_folds, har_noisy_folds, ensemble_size)
                    print("HAR dataset, size: " + str(ensemble_size) + " type: " +
                          str(subset_type) + "-" + str(features_chooser_type) + " = " + str(mean_accuracy))
                    total_time = clock() - start
                    print("Time for training and evaluating = " + str(floor(total_time / 60)) + ":" + str(floor(total_time % 60)))

