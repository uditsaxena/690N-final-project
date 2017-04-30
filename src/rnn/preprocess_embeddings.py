import os
import re

import sys
from functools import reduce

import time
from gensim.models import Word2Vec
from gensim.models.word2vec_inner import FAST_VERSION


def get_train_test_files(i):
    # print(os.getcwd())
    file_list = (os.getcwd())
    base_file = os.getcwd() + "/tasks_1-20_v1-2/en-10k/"
    file_list = (os.listdir(base_file))
    # print(file_list)
    test_file_list = []
    train_file_list = []
    for file in file_list:
        if file.startswith("qa" + str(i) + "_"):
            if file.endswith("_test.txt"):
                test_file_list.append(base_file + file)
            elif file.endswith("_train.txt"):
                train_file_list.append(base_file + file)
    # print(train_file_list)
    # print(test_file_list)

    # f_train = open(base_file + train_file_list)
    # f_test = open(base_file + test_file_list)

    return train_file_list, test_file_list


def tokenize(sent):
    '''Return the tokens of a sentence including punctuation.

    >>> tokenize('Bob dropped the apple. Where is the apple?')
    ['Bob', 'dropped', 'the', 'apple', '.', 'Where', 'is', 'the', 'apple', '?']
    '''
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]


def parse_stories(lines, only_supporting=False):
    '''Parse stories provided in the bAbi tasks format

    If only_supporting is true,
    only the sentences that support the answer are kept.
    '''
    data = []
    story = []
    for line in lines:
        # line = line.decode('utf-8').strip()
        nid, line = line.split(' ', 1)
        nid = int(nid)
        if nid == 1:
            story = []
        if '\t' in line:
            q, a, supporting = line.split('\t')
            q = tokenize(q)
            # a = tokenize(a)
            substory = None
            if only_supporting:
                # Only select the related substory
                supporting = map(int, supporting.split())
                substory = [story[i - 1] for i in supporting]
            else:
                # Provide all the substories
                substory = [x for x in story if x]
            data.append((substory, q, a))
            story.append('')
        else:
            sent = tokenize(line)
            # sent = line.strip()
            story.append(sent)
    return data


def get_stories(file_list, only_supporting=False, max_length=None):
    '''Given a file name, read the file, retrieve the stories,
    and then convert the sentences into a single story.

    If max_length is supplied,
    any stories longer than max_length tokens will be discarded.
    '''
    super_data = []
    for file in file_list:
        f = open(file)
        data = parse_stories(f.readlines(), only_supporting=only_supporting)
        # print(data[0])
        _data = data
        flatten = lambda data: reduce(lambda x, y: x + y, data)
        _data = [(flatten(story), q, answer) for story, q, answer in data if
                 not max_length or len(flatten(story)) < max_length]
        # print(_data[0])
        for item in data:
            p = item[0]
            # super_data.append(p)
            for line in p:
                super_data.append(line)

            super_data.append(item[1])
            super_data.append([item[2]])
            # print(p)
            # print(super_data)
    # print(len(super_data))
    return super_data


def main(i):
    base_filename = "w2v"
    train, test = get_train_test_files(i)
    # print("training stories:")
    train = get_stories(train)
    # print(len(train))
    # print("testing stories:")
    test = get_stories(test)
    # print(len(test))
    vocab = set()
    train_test = train + test
    # print(len(train_test))
    return train_test
    # for story, q, answer in train + test:
    #     vocab |= set(story + q + [answer])
    # vocab = sorted(vocab)
    # Reserve 0 for masking via pad_sequences
    # vocab_size = len(vocab) + 1
    # story_maxlen = max(map(len, (x for x, _, _ in train + test)))
    # query_maxlen = max(map(len, (x for _, x, _ in train + test)))
    # x, xq, y = vectorize_stories_word2vec(train, word_idx, story_maxlen, query_maxlen)
    # tx, txq, ty = vectorize_stories_word2vec(test, word_idx, story_maxlen, query_maxlen)


if __name__ == '__main__':
    fname = "word2vec_100_5.w2v"
    # model = Word2Vec.load(fname)
    # print(model)
    # print(model.vocab)
    arg_list = sys.argv[1:]
    data = []
    iterations = (int)(arg_list[1])
    if len(arg_list) > 0:
        upper = (int)(arg_list[0])
        # for i in range(upper - 1, upper):
        for i in range(upper - 19, upper+1):
            # print("File number: ", i)
            list = main(i)
            data += list
            # print(len(data))
    # print("Starting to train !")
    # print(FAST_VERSION)
    # start = time.time()
    # model = Word2Vec(data, size=100, window=3, min_count=1, workers=1, iter=iterations)
    # model.save(fname)
    # model.wv.save_word2vec_format(fname, fvocab="vocab", binary=True)
    # end = time.time()
    # print(end - start)
