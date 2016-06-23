import math
import re


class Indexer:

    def __init__(self, words_in_files):
        self.words_in_files = words_in_files
        self.index = {}
        self.build_index()
        self.tf_idf = {}
        self.compute_tf_idf()

    def build_index(self):
        for filename in self.words_in_files.keys():
            for word in self.words_in_files[filename].keys():
                if word in self.index:
                    self.index[word][filename] = (
                        self.words_in_files[filename][word])
                else:
                    self.index[word] = (
                        {filename: self.words_in_files[filename][word]})

    def compute_tf(self):
        tf = {}
        for filename in self.words_in_files.keys():
            euclidean_norm = sum(
                [len(self.words_in_files[filename][word]) ** 2 for word
                 in self.words_in_files[filename].keys()]
            ) ** 0.5
            tf[filename] = {}
            for word in self.words_in_files[filename].keys():
                tf[filename][word] = (
                    len(self.words_in_files[filename][word]) / euclidean_norm)
        return tf

    def compute_idf(self):
        idf = {}
        n = len(self.words_in_files)
        for word in self.index:
            idf[word] = math.log(n / len(self.index[word]))
        return idf

    def compute_tf_idf(self):
        tf = self.compute_tf()
        idf = self.compute_idf()
        for filename in self.words_in_files:
            self.tf_idf[filename] = {}
            for word in self.index:
                if word in self.words_in_files[filename].keys():
                    self.tf_idf[filename][word] = idf[word] * tf[filename][word]
                else:
                    self.tf_idf[filename][word] = 0

    def one_word_query(self, word):
        word = re.match(ur'\w+', word, flags=re.UNICODE).group()
        if word in self.index:
            return self.index[word].keys()
        else:
            return []

    def free_text_query(self, text):
        words = re.findall(ur'\b\w+\b', text, flags=re.UNICODE)
        result = []
        for word in words:
            result.extend(self.one_word_query(word))
        return result

    def phrase_query(self, query):
        words = re.findall(ur'\b\w+\b', query)
        results, files_list = [], []
        for word in words:
            files_list.append(self.one_word_query(word))
        shared_files = set(files_list[0]).intersection(*files_list)
        for filename in shared_files:
            words_positions = []
            for word in words:
                words_positions.append(self.index[word][filename])
            for i in xrange(len(words_positions)):
                for j in xrange(len(words_positions[i])):
                    words_positions[i] -= i
            if set(words_positions[0]).intersection(*words_positions):
                results.append(filename)
        return results