# encoding=utf-8
import jieba
import codecs
import json
import os
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.metrics import f1_score, precision_recall_fscore_support

cur_dir = os.path.dirname(os.path.realpath(__file__))

STOP_WORDS = [u'', u' ', u'\n', u'\r', u'：', u'，', u'。', u':', u',', u'.', u'[', u']',
              u'表情', u'大表情', u'图片', u'文件', u'的', u'地', u'得']

with codecs.open(os.path.join(cur_dir, 'data/staffs.json')) as f:
    staffs = json.load(f)["staffs"]
for staff in staffs:
    jieba.add_word(staff)
    jieba.add_word(staff[-2:])


class ChatRecognizer(object):

    def __init__(self, vector_method='tfidf'):
        self.vector_method = vector_method
        self.naive_bayes_model = None
        self.features = None
        self.idf = None

    @staticmethod
    def word_segmentation(docs):
        segmented_docs = []
        for doc in docs:
            jieba_res = jieba.cut(doc, cut_all=False)
            segmented_doc = []
            for word in jieba_res:
                word = word.strip()
                if word in STOP_WORDS:
                    continue
                else:
                    segmented_doc.append(word)

            segmented_docs.append(segmented_doc)
        return segmented_docs

    def init_dictionary(self, segmented_docs):
        dictionary = {}
        for segmented_doc in segmented_docs:
            for word in set(segmented_doc):
                word = word
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

        print "Size of all words:", len(dictionary)
        sorted_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        sorted_dictionary = sorted_dictionary[:2000]
        dictionary = dict(sorted_dictionary)

        self.features = dictionary.keys()
        self.idf = map(lambda x: - np.log((x + 1) / float(len(segmented_docs))), dictionary.values())

    # def gen_bow(self, segmented_docs):
    #     bow = []
    #     for segmented_doc in segmented_docs:
    #         cur_dict = dict(zip(self.dictionary.keys(), [0 for _ in range(len(self.dictionary))]))
    #         for word in segmented_doc:
    #             if word not in self.dictionary:
    #                 continue
    #             else:
    #                 cur_dict[word] += 1
    #
    #         bow.append(cur_dict.values())
    #
    #     return np.array(bow)

    def gen_tfidf(self, segmented_docs):
        tfidf = []
        for segmented_doc in segmented_docs:
            n_words = len(segmented_doc)
            if n_words == 0:
                tf = 0
            else:
                tf = map(lambda x: segmented_doc.count(x) / float(n_words), self.features)
            tfidf.append(np.array(tf) * np.array(self.idf))

        return np.array(tfidf)

    def validate(self, alpha=1.0):
        df = pd.read_csv(os.path.join(cur_dir, 'data/dataset_verified.csv')).astype('str')  # must add astype('str) to avoid codec problem
        n = df.shape[0]
        split_ratio = 0.8

        train_df = df.iloc[:int(n * split_ratio), :]
        train_segmented_docs = self.word_segmentation(train_df['value'].tolist())
        self.init_dictionary(train_segmented_docs)
        if self.vector_method == 'tfidf':
            train_X = np.array(self.gen_tfidf(train_segmented_docs))
        elif self.vector_method == 'bow':
            train_X = np.array(self.gen_bow(train_segmented_docs))
        else:
            raise KeyError("Didn't know given word embedding method: %s" % self.vector_method)
        train_y = train_df['label'].values

        test_df = df.iloc[int(n * split_ratio):, :]
        test_segmented_docs = self.word_segmentation(test_df['value'].tolist())
        test_X = np.array(self.gen_tfidf(test_segmented_docs))
        test_y = test_df['label'].values

        self.naive_bayes_model = MultinomialNB(alpha=alpha).fit(train_X, train_y)
        y_pred = self.naive_bayes_model.predict(test_X)
        pred_proba = self.naive_bayes_model.predict_proba(test_X)
        print "\n-----------  TP -----------"
        for i in range(len(y_pred)):
            if y_pred[i] == '1' and test_y[i] == '1':
                print test_df['value'].iat[i], pred_proba[i]
        print "\n-----------  FP -----------"
        for i in range(len(y_pred)):
            if y_pred[i] == '1' and test_y[i] == '0':
                print test_df['value'].iat[i], pred_proba[i]
        print "\n-----------  FN -----------"
        for i in range(len(y_pred)):
            if y_pred[i] == '0' and test_y[i] == '1':
                print test_df['value'].iat[i], pred_proba[i]
        print "\n===========  Metric ==========="
        print "F1-score:", f1_score(test_y, y_pred, labels=['0', '1'], average=None)[1]
        p_class, r_class, f_class, support_micro = precision_recall_fscore_support(test_y, y_pred, labels=['0', '1'])
        print "Precision:", p_class[1]
        print "Recall:", r_class[1]

    def train(self, alpha=1):
        df = pd.read_csv(os.path.join(cur_dir, 'data/dataset_verified.csv')).astype('str')  # must add astype('str) to avoid codec problem
        n = df.shape[0]
        split_ratio = 0.8

        train_df = df.iloc[:int(n * split_ratio), :]
        train_segmented_docs = self.word_segmentation(train_df['value'].tolist())
        self.init_dictionary(train_segmented_docs)
        if self.vector_method == 'tfidf':
            train_X = np.array(self.gen_tfidf(train_segmented_docs))
        elif self.vector_method == 'bow':
            train_X = np.array(self.gen_bow(train_segmented_docs))
        else:
            raise KeyError("Didn't know given word embedding method: %s" % self.vector_method)
        train_y = train_df['label'].values

        self.naive_bayes_model = MultinomialNB(alpha=alpha).fit(train_X, train_y)

    def test(self, docs, print_result=True):
        if self.naive_bayes_model is None:
            raise RuntimeError("Must train or load existed model before testing.")
        test_segmented_docs = self.word_segmentation(docs)
        if self.vector_method == 'tfidf':
            test_X = np.array(self.gen_tfidf(test_segmented_docs))
        elif self.vector_method == 'bow':
            test_X = np.array(self.gen_bow(test_segmented_docs))
        else:
            raise KeyError("Didn't know given word embedding method: %s" % self.vector_method)

        pred = self.naive_bayes_model.predict_proba(test_X)
        labels = []
        probs = []
        for i, doc in enumerate(docs):
            # if doc is too short, considered as negative sample
            if len(doc) < 4 * 3:  # utf-8 coding
                label = 0
                prob = 0.0
            else:
                label = np.argmax(pred[i])
                prob = pred[i][1]
            labels.append(label)
            probs.append(prob)

        if print_result:
            meaningful_label = ['否', '是']
            for i, doc in enumerate(docs):
                print_label = meaningful_label[labels[i]]
                print_prob = probs[i]
                print "Predict: %s (%.2f%%)  --- 「%s」" % (print_label, print_prob * 100, doc)

        return labels, probs

    def test_one(self, doc, print_result=False):
        return self.test([doc], print_result=print_result)

    def save(self):
        model = dict(naive_bayes_model=self.naive_bayes_model, features=self.features, idf=self.idf)
        joblib.dump(model, os.path.join(cur_dir, 'chat_recognizer.m'))

    def load(self):
        model = joblib.load(os.path.join(cur_dir, 'chat_recognizer.m'))
        self.naive_bayes_model = model['naive_bayes_model']
        self.features = model['features']
        self.idf = model['idf']


# def test_tfidf():
#     docs = [['a', 'b', 'a'],
#             ['c', 'd', 'e'],
#             ['b', 'd']]
#     dct = {'a': 1, 'b': 2, 'c': 1, 'd': 2, 'e': 1}
#     print init_dictionary(docs)
#     print gen_tfidf(docs, dct)


# validate1()
# train(save=True)
# test_one("老婆过阴历生日 早走一会")

# cr = ChatRecognizer()
# cr.validate(0.01)
# cr.train()
# cr.save()
# cr.load()
# df = pd.read_csv('data/dataset_verified.csv').astype('str')  # must add astype('str) to avoid codec problem
# n = df.shape[0]
# split_ratio = 0.8
# test_df = df.iloc[int(n * split_ratio):, :]
# cr.test(test_df['value'].tolist())
# cr.test_one("...")
# cr.test_one("……")
# cr.test_one("会")
# cr.test_one("早")
# cr.test_one("早点回家")
