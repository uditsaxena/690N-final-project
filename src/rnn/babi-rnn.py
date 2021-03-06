

from __future__ import print_function

import re, os
import sys
from functools import reduce

import gensim
import pandas
import tensorflow as tf
import numpy as np
from gensim.models import Word2Vec, KeyedVectors
from keras import layers
from keras.engine import Model
from keras.layers import recurrent
from keras.preprocessing.sequence import pad_sequences

EMBEDDING_DIMENSION = 100


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
            story.append(sent)
    return data


def get_stories(f, only_supporting=False, max_length=None):
    '''Given a file name, read the file, retrieve the stories,
    and then convert the sentences into a single story.

    If max_length is supplied,
    any stories longer than max_length tokens will be discarded.
    '''
    data = parse_stories(f.readlines(), only_supporting=only_supporting)
    flatten = lambda data: reduce(lambda x, y: x + y, data)
    data = [(flatten(story), q, answer) for story, q, answer in data if
            not max_length or len(flatten(story)) < max_length]
    # print(len(data))
    # print(data)
    # print(data[0][0]+data[0][1] + [data[0][2]])
    return data


def vectorize_stories(data, word_idx, story_maxlen, query_maxlen):
    xs = []
    xqs = []
    ys = []
    i = 0
    for story, query, answer in data:
        x = [word_idx[w] for w in story]
        xq = [word_idx[w] for w in query]
        # let's not forget that index 0 is reserved
        y = np.zeros(len(word_idx) + 1)
        y[word_idx[answer]] = 1
        xs.append(x)
        xqs.append(xq)
        ys.append(y)
        if (i < 2):
            # print(answer, ys)
            print(story, x)
            i += 1
    return pad_sequences(xs, maxlen=story_maxlen), pad_sequences(xqs, maxlen=query_maxlen), np.array(ys)


def vectorize_stories_word2vec(model, data, story_maxlen, query_maxlen):
    xs = []
    xqs = []
    ys = []
    i = 0
    for story, query, answer in data:
        x = [model[w] for w in story]
        xq = [model[w] for w in query]
        # let's not forget that index 0 is reserved
        y = model[answer]
        # y = np.zeros(len(word_idx) + 1)
        # y[model[answer]] = 1.0
        xs.append(x)
        xqs.append(xq)
        ys.append(y)
        # if (i < 2):
        #     # print(answer, ys)
        #     print(story, x)
        #     i += 1
    return pad_sequences(xs, maxlen=story_maxlen), pad_sequences(xqs, maxlen=query_maxlen), np.array(ys)


def check_existence(vocab):
    fname = "word2vec_100_5.w2v"
    # model = Word2Vec.load(fname)
    model = KeyedVectors.load_word2vec_format(fname=fname, fvocab="vocab", binary=True)
    print(len(model.vocab.keys()), model.vocab.keys())
    for w in vocab:
        if (w in model.vocab.keys()):
            # print(w, " : Blasphemy")
            print(model[w])


def get_word_vectors_from_pretr_embeddings(train, test, vocab):
    get_pre_trained_emb(vocab)


def get_pre_trained_emb(vocab):
    model = get_model()
    # model loaded
    # print(len(model.vocab.keys()), len(vocab))
    idx_to_word = enumerate(vocab)
    word_to_idx = {}
    for i, c in idx_to_word:
        # print(i, c)
        word_to_idx[c] = i + 1  # 0 reserved for masking
    emb_dim = EMBEDDING_DIMENSION
    vocab_len = len(vocab) + 1  # 0 reserved for masking
    pre_trained_emb_weights = np.zeros((vocab_len, emb_dim))
    for word, index in word_to_idx.items():
        pre_trained_emb_weights[index, :] = model[word]
    # print(pre_trained_emb_weights)
    return pre_trained_emb_weights


def get_model():
    fname = "word2vec_100_1000.w2v"
    model = KeyedVectors.load_word2vec_format(fname=fname, fvocab="vocab", binary=True)
    return model


def main_pretrained(i, RNN_TYPE):
    # TODO: change to GRU, Recurrent, and SimpleRNN
    # print(i, RNN_TYPE)
    RNN = recurrent.LSTM
    if RNN_TYPE == "gru":
        # print("Starting a GRU: ")
        RNN = recurrent.GRU
        file_name = "history_gru_" + str(i) + ".csv"

    elif RNN_TYPE == "recurrent":
        # print("Starting a Recurrent Unit: ")
        RNN = recurrent.Recurrent
        file_name = "history_recurrent_" + str(i) + ".csv"

    elif RNN_TYPE == "simplernn":
        # print("Starting a SimpleRNN: ")
        RNN = recurrent.SimpleRNN
        file_name = "history_simple_" + str(i) + ".csv"
    else:
        # print("Starting an LSTM")
        file_name = "history_lstm_" + str(i) + ".csv"

    EMBED_HIDDEN_SIZE = 100
    SENT_HIDDEN_SIZE = 100
    QUERY_HIDDEN_SIZE = 100
    BATCH_SIZE = 50
    EPOCHS = 100
    # print('RNN / Embed / Sent / Query = {}, {}, {}, {}'.format(RNN,
    #                                                            EMBED_HIDDEN_SIZE,
    #                                                            SENT_HIDDEN_SIZE,
    #                                                            QUERY_HIDDEN_SIZE))
    # print(os.getcwd())
    file_list = (os.getcwd())
    base_file = os.getcwd() + "/tasks_1-20_v1-2/en-10k/"
    file_list = (os.listdir(base_file))
    # print(file_list)
    test_file = ""
    train_file = ""
    for file in file_list:
        if file.startswith("qa" + str(i) + "_"):
            if file.endswith("_test.txt"):
                test_file = file
                # print(test_file)
            elif file.endswith("_train.txt"):
                train_file = file
                # print(train_file)
    print(train_file)
    print(test_file)

    f_train = open(base_file + train_file)
    f_test = open(base_file + test_file)

    # try:
    #     path = get_file('babi-tasks-v1-2.tar.gz',
    #                     origin='https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz')
    # except:
    #     print('Error downloading dataset, please download it manually:\n'
    #           '$ wget http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz\n'
    #           '$ mv tasks_1-20_v1-2.tar.gz ~/.keras/datasets/babi-tasks-v1-2.tar.gz')
    #     raise
    # tar = tarfile.open(path)
    # # Default QA1 with 1000 samples
    # # challenge = 'tasks_1-20_v1-2/en/qa1_single-supporting-fact_{}.txt'
    # # QA1 with 10,000 samples
    # # challenge = 'tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_{}.txt'
    # # QA2 with 1000 samples
    # challenge = 'tasks_1-20_v1-2/en/qa2_two-supporting-facts_{}.txt'
    # # QA2 with 10,000 samples
    # # challenge = 'tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_{}.txt'

    # train = get_stories(tar.extractfile(challenge.format('train')))
    # test = get_stories(tar.extractfile(challenge.format('test')))
    # print("training stories:")
    train = get_stories(f_train)
    # print(len(train))
    # print("testing stories:")
    test = get_stories(f_test)
    # print(len(test))
    vocab = set()
    for story, q, answer in train + test:
        vocab |= set(story + q + [answer])
    vocab = sorted(vocab)
    # check_existence(vocab)
    # get_word_vectors_from_pretr_embeddings(train, test, vocab)

    # Reserve 0 for masking via pad_sequences
    vocab_size = len(vocab) + 1
    print("Vocabulary size: ", vocab_size)
    word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
    story_maxlen = max(map(len, (x for x, _, _ in train + test)))
    query_maxlen = max(map(len, (x for _, x, _ in train + test)))
    model = get_model()
    x, xq, y = vectorize_stories(train, word_idx, story_maxlen, query_maxlen)
    tx, txq, ty = vectorize_stories(test, word_idx, story_maxlen, query_maxlen)
    print('vocab = {}'.format(vocab))
    print('x.shape = {}'.format(x.shape))
    print('xq.shape = {}'.format(xq.shape))
    print('y.shape = {}'.format(y.shape))
    print('story_maxlen, query_maxlen = {}, {}'.format(story_maxlen, query_maxlen))
    print('Build model...')

    pre_trained_emb_weights = get_pre_trained_emb(vocab)
    sentence = layers.Input(shape=(story_maxlen,), dtype='float32')
    encoded_sentence = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE, mask_zero=True,
                                        weights=[pre_trained_emb_weights])(sentence)
    encoded_sentence = layers.Dropout(0.3)(encoded_sentence)
    # encoded_sentence = layers.Dropout(0.3)(sentence)
    question = layers.Input(shape=(query_maxlen,), dtype='float32')
    encoded_question = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE, mask_zero=True,
                                        weights=[pre_trained_emb_weights])(question)
    encoded_question = layers.Dropout(0.3)(encoded_question)
    # encoded_question = layers.Dropout(0.3)(question)
    encoded_question = RNN(EMBED_HIDDEN_SIZE)(encoded_question)
    encoded_question = layers.RepeatVector(story_maxlen)(encoded_question)
    merged = layers.add([encoded_sentence, encoded_question])
    merged = RNN(EMBED_HIDDEN_SIZE)(merged)
    merged = layers.Dropout(0.3)(merged)
    preds = layers.Dense(vocab_size, activation='softmax')(merged)
    # preds = layers.Dense(EMBEDDING_DIMENSION, activation='softmax')(merged)
    model = Model([sentence, question], preds)
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print('Training')
    history = model.fit([x, xq], y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.05)
    pandas.DataFrame(history.history).to_csv("pret_"+file_name)

    loss, acc = model.evaluate([tx, txq], ty,
                               batch_size=BATCH_SIZE)

    pandas.DataFrame([str(loss)+"_"+ str(acc)]).to_csv("test_"+RNN_TYPE+"_"+str(i)+".csv")
    print('Test loss / test accuracy = {:.4f} / {:.4f}'.format(loss, acc))

def main(i, RNN_TYPE):
    # TODO: change to GRU, Recurrent, and SimpleRNN
    # print(i, RNN_TYPE)
    RNN = recurrent.LSTM
    if RNN_TYPE == "gru":
        # print("Starting a GRU: ")
        RNN = recurrent.GRU
        file_name = "history_gru_" + str(i) + ".csv"

    elif RNN_TYPE == "recurrent":
        # print("Starting a Recurrent Unit: ")
        RNN = recurrent.Recurrent
        file_name = "history_recurrent_" + str(i) + ".csv"

    elif RNN_TYPE == "simplernn":
        # print("Starting a SimpleRNN: ")
        RNN = recurrent.SimpleRNN
        file_name = "history_simple_" + str(i) + ".csv"
    else:
        # print("Starting an LSTM")
        file_name = "history_lstm_" + str(i) + ".csv"

    EMBED_HIDDEN_SIZE = 100
    SENT_HIDDEN_SIZE = 100
    QUERY_HIDDEN_SIZE = 100
    BATCH_SIZE = 50
    EPOCHS = 100
    # print('RNN / Embed / Sent / Query = {}, {}, {}, {}'.format(RNN,
    #                                                            EMBED_HIDDEN_SIZE,
    #                                                            SENT_HIDDEN_SIZE,
    #                                                            QUERY_HIDDEN_SIZE))
    # print(os.getcwd())
    file_list = (os.getcwd())
    base_file = os.getcwd() + "/tasks_1-20_v1-2/en/"
    file_list = (os.listdir(base_file))
    # print(file_list)
    test_file = ""
    train_file = ""
    for file in file_list:
        if file.startswith("qa" + str(i) + "_"):
            if file.endswith("_test.txt"):
                test_file = file
                # print(test_file)
            elif file.endswith("_train.txt"):
                train_file = file
                # print(train_file)
    print(train_file)
    print(test_file)

    f_train = open(base_file + train_file)
    f_test = open(base_file + test_file)

    # try:
    #     path = get_file('babi-tasks-v1-2.tar.gz',
    #                     origin='https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz')
    # except:
    #     print('Error downloading dataset, please download it manually:\n'
    #           '$ wget http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz\n'
    #           '$ mv tasks_1-20_v1-2.tar.gz ~/.keras/datasets/babi-tasks-v1-2.tar.gz')
    #     raise
    # tar = tarfile.open(path)
    # # Default QA1 with 1000 samples
    # # challenge = 'tasks_1-20_v1-2/en/qa1_single-supporting-fact_{}.txt'
    # # QA1 with 10,000 samples
    # # challenge = 'tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_{}.txt'
    # # QA2 with 1000 samples
    # challenge = 'tasks_1-20_v1-2/en/qa2_two-supporting-facts_{}.txt'
    # # QA2 with 10,000 samples
    # # challenge = 'tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_{}.txt'

    # train = get_stories(tar.extractfile(challenge.format('train')))
    # test = get_stories(tar.extractfile(challenge.format('test')))
    # print("training stories:")
    train = get_stories(f_train)
    # print(len(train))
    # print("testing stories:")
    test = get_stories(f_test)
    # print(len(test))
    vocab = set()
    for story, q, answer in train + test:
        vocab |= set(story + q + [answer])
    vocab = sorted(vocab)
    # check_existence(vocab)
    # get_word_vectors_from_pretr_embeddings(train, test, vocab)

    # Reserve 0 for masking via pad_sequences
    vocab_size = len(vocab) + 1
    print("Vocabulary size: ", vocab_size)
    word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
    story_maxlen = max(map(len, (x for x, _, _ in train + test)))
    query_maxlen = max(map(len, (x for _, x, _ in train + test)))

    x, xq, y = vectorize_stories(train, word_idx, story_maxlen, query_maxlen)
    tx, txq, ty = vectorize_stories(test, word_idx,story_maxlen, query_maxlen)
    print('vocab = {}'.format(vocab))
    print('x.shape = {}'.format(x.shape))
    print('xq.shape = {}'.format(xq.shape))
    print('y.shape = {}'.format(y.shape))
    print('story_maxlen, query_maxlen = {}, {}'.format(story_maxlen, query_maxlen))
    print('Build model...')

    pre_trained_emb_weights = get_pre_trained_emb(vocab)
    sentence = layers.Input(shape=(story_maxlen,), dtype='float32')
    encoded_sentence = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE)(sentence)
    encoded_sentence = layers.Dropout(0.3)(encoded_sentence)
    question = layers.Input(shape=(query_maxlen,), dtype='float32')
    encoded_question = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE)(question)
    encoded_question = layers.Dropout(0.3)(encoded_question)

    encoded_question = RNN(EMBED_HIDDEN_SIZE)(encoded_question)
    encoded_question = layers.RepeatVector(story_maxlen)(encoded_question)
    merged = layers.add([encoded_sentence, encoded_question])
    merged = RNN(EMBED_HIDDEN_SIZE)(merged)
    merged = layers.Dropout(0.3)(merged)
    preds = layers.Dense(vocab_size, activation='softmax')(merged)
    model = Model([sentence, question], preds)
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    print('Training')
    history = model.fit([x, xq], y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.05)
    pandas.DataFrame(history.history).to_csv("__pre_"+file_name)

    loss, acc = model.evaluate([tx, txq], ty,
                               batch_size=BATCH_SIZE)

    pandas.DataFrame([str(loss)+"_"+ str(acc)]).to_csv("__test_"+RNN_TYPE+"_"+str(i)+".csv")
    print('Test loss / test accuracy = {:.4f} / {:.4f}'.format(loss, acc))


if __name__ == '__main__':
    arg_list = sys.argv[1:]
    if len(arg_list) > 0:
        upper = (int)(arg_list[0])
        for i in range(upper - 2, upper):
            # for i in range(upper - 20, upper):
            # print(i+1)
            for type in ["lstm", "gru", "simplernn"]:#, "recurrent"]:
                main_pretrained(i + 1, type)
                # main(i + 1, type)
                # main(1, "lstm")
                # main(2, "lstm")
