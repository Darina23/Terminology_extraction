#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 01.03.2021
# Mac OS
"""
Zweck: die Auswahl von Kandidaten für die Terminologie.

Autorin: Daryna Ivanova
"""

import os
import unittest
import nltk

from nltk import FreqDist
from nltk.corpus import reuters, stopwords
from nltk.tokenize import RegexpTokenizer


class CandidateSelection():
    """
    Select candidates.

    Methods
    -------
    text_files_getter(folder_name: str)
        Creates a domain corpus of candidate terms, computes candidates
        frequency across all documents and within one document.

    isNoun (code: str)
        Lists POS-Tags for a Noun.


    isAdjective (code: str)
        Lists POS-Tags for an Adjektive and Gerund.

    isVerb (code: str)
        Lists POS-Tags for a Verb.

    reuters_corpus():
        Extracts bigrams from nltk.reuters corpus. Creates reference corpus
        and computes frequency of a candidate.

    filter_text_files(corpus: list, n: int, freq_dist_filter: bool = False):
        Filter stopwords, numbers and make tokens in lower case. Then generate
        bigrams.
        If freq_dict_filter = True, call frequency_filter method.

    frequency_filter(corpus: list, n: int):
        Filter out all the tokens with occurence < n.
    """

    def text_files_getter(self, folder_name: str, filter_freq_n: int,
                          **options) -> tuple:
        """
        Convert txt files from a given directory into corpora.

        Create a corpus of bigrams, a corpus of bigrams with their frequencies
        across all documents and a corpus of bigrams and their frequencies in
        a text.


        Parameters
        ----------
        folder_path : str
            Name of a directory, where domain corpus texts are located.
        filter_freq_n: int
            Filter out the words, which occur less than n times in a corpus.
            An integer number n has to be given. Enter 0 to deactivate the
            filter.
        **options
            Needed for method testing.

        Returns
        -------
        candidates_total, candidates_per_doc, candidates : tuple
            candidates_total : dict
                Bigrams and their absolute frequencies across all texts.
            candidates_per_doc : list
                Contains dictionaries with bigrams and their absolute
                frequencies for each text.
            candidates : list
                Bigrams from all the txt files.
        """
        path = os.getcwd() + '/' + folder_name

        # list of lists with bigrams per document
        candidates_per_doc = []
        candidates_total = {}

        for file in os.listdir(path):

            with open(path + '/' + file, 'r', encoding='utf-8',
                      errors='ignore') as temp_file:

                text = temp_file.read()

            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text)

            # filter stopwords and numbers and create bigrams
            if len(options) == 0:
                bigrams_cleaned = self.filter_text_files(tokens, filter_freq_n)
            else:
                fun = options.get("function")
                bigrams_cleaned = fun(tokens, filter_freq_n)

            doc_bigrams_frequency = dict(nltk.FreqDist(bigrams_cleaned))

            # With the help of POS-tagging add only acceptable bigrams
            # to the corpus
            to_delete = []
            for bigram in doc_bigrams_frequency.keys():
                part_of_speech = nltk.pos_tag(bigram)
                combination = part_of_speech[0][1], part_of_speech[1][1]

                if len(options) == 0:
                    if (self.isNoun(combination[0]) and
                        self.isAdjective(combination[1])) or \
                        (self.isNoun(combination[1]) and
                         self.isAdjective(combination[0])) or \
                        (self.isAdjective(combination[1]) and
                         self.isAdjective(combination[0])) or \
                        (self.isNoun(combination[0]) and
                         self.isNoun(combination[1])) or \
                        (self.isVerb(combination[0]) and
                         self.isNoun(combination[1])) or \
                        (self.isVerb(combination[0]) and
                         self.isAdjective(combination[1])):
                        pass
                    else:
                        # Delete not acceptable POS-tags combinations
                        to_delete.append(bigram)

                # This block is created only for testing
                else:
                    fun_noun = options.get("is_noun")
                    fun_adj = options.get("is_adj")
                    fun_verb = options.get("is_verb")
                    if (fun_noun(combination[0]) and
                        fun_adj(combination[1])) or \
                        (fun_noun(combination[1]) and
                         fun_adj(combination[0])) or \
                        (fun_adj(combination[1]) and
                         fun_adj(combination[0])) or \
                        (fun_noun(combination[0]) and
                         fun_noun(combination[1])) or \
                        (fun_verb(combination[0]) and
                         fun_noun(combination[1])) or \
                        (fun_verb(combination[0]) and
                         fun_adj(combination[1])):
                        pass
                    else:
                        to_delete.append(bigram)

            # Delete not acceptable bigrams from another corpus
            for bigram in to_delete:
                del doc_bigrams_frequency[bigram]

            candidates_per_doc.append(doc_bigrams_frequency)

            for key, value in doc_bigrams_frequency.items():
                if key in candidates_total.keys():
                    candidates_total[key] = candidates_total[key] + value
                else:
                    candidates_total[key] = value

        # All bigrams
        candidates = candidates_total.keys()

        return candidates_total, candidates_per_doc, candidates

    def isNoun(self, code: str) -> bool:
        """
        Representation of a Noun.

        An auxiliary function for text_files_getter method.

        Parameters
        ----------
        code : str
            A POS-Tag.

        Returns
        -------
        bool
            True if a POS-Tag is a Noun.
            False if it is not a Noun.
        """
        if code == 'NNS' or code == 'NNP' or code == 'NNPS' or code == 'NN':
            return True
        else:
            return False

    def isAdjective(self, code: str) -> bool:
        """
        Representation of an Adjektiv.

        Sometimes adjektives can be misinterpreted by POS-taggs
        as gerund form of verbs.

        An auxiliary function for text_files_getter method.

        Parameters
        ----------
        code : str
            A POS-Tag.

        Returns
        -------
        bool
            True if a POS-Tag is an Adj/Gerund.
            False if it is not an Adj/Gerund.
        """
        if code == 'JJ' or code == 'VBG':
            return True
        else:
            return False

    def isVerb(self, code: str) -> bool:
        """
        Representation of a Verb/Adverb.

        An auxiliary function for text_files_getter method.

        Parameters
        ----------
        code : str
            A POS-Tag.

        Returns
        -------
        bool
            True if a POS-Tag is a Verb/Adverb.
            False if it is not a Verb/Adverb.
        """
        if code == 'VB' or code == 'VBD' or code == 'VBN' or code == 'RB' or \
                code == 'VBG':
            return True
        else:
            return False

    def reuters_corpus(self, **options) -> tuple:
        """
        Convert nltk.reuters corpus in a list of bigrams.

        Create another corpus with bigrams and their frequencies.
        Stop words, punctuation, numbers will be filtered.

        **options
            Needed for method testing.

        Returns
        -------
        reuters_freq, clean_corpus : tuple
            reuters_freq : dict
                {key: nltk.reuters candidate, value: it's absolute frequency}
            clean_corpus : list
                nltk.reuters term candidates.
        """
        # get list of file names
        doc_ids = reuters.fileids()

        # list of reuter tokens
        corpus = []

        for doc in doc_ids:
            corpus += list(reuters.words(doc))

        # create bigrams from a filtered corpus
        if len(options) == 0:
            clean_corpus = self.filter_text_files(corpus, 0)
        else:
            fun = options.get("function")
            clean_corpus = fun(corpus, 0)
        # compute absolute frequency
        reuters_freq = dict(nltk.FreqDist(clean_corpus))

        return reuters_freq, clean_corpus

    def filter_text_files(self, corpus: list, filter_freq_n: int,
                          **options) -> list:
        """
        Filter stop words and numbers out of the Domaincorpus.

        Parameters
        ----------
        corpus : list
            Takes a list of tokens.
        filter_freq_n : int
            Only the words with a given from user n frequency will be used to
            create bigrams.
            This parameter works only if freq_dist_filter = True.
        **options
            Needed for method testing.

        Returns
        -------
        output : list
        """
        corpus_lower = [w.lower() for w in corpus]
        stop_words = []

        # Expand stopword list
        with open(os.getcwd() + '/stopwords.txt', 'r', encoding='utf-8',
                  errors='ignore') as f:

            for i in f.readlines():
                tmp = i.strip()
                stop_words += tmp
        stop_words += stopwords.words('english')

        corpus_filtered = [w for w in corpus_lower if w.isalpha()
                           and w not in stop_words and len(w) >= 2]

        # remove tokens with the frequeny < n and create bigrams
        if len(options) == 0:
            output = self.frequency_filter(corpus_filtered, filter_freq_n)
        else:
            fun = options.get("function")
            output = fun(corpus_filtered, filter_freq_n)

        return output

    def frequency_filter(self, corpus: list, filter_freq_n: int) -> list:
        """
        Extract bigrams from the tokens, which occur more than n times.

        Parameters
        ----------
        corpus : list
            Takes a corpus with tokens.
        n : int
            Only the words with a given from user n frequency will be used to
            create bigrams.

        Returns
        -------
        bigrams : list
            List of bigrams.
        """
        # absolute frequency of unigrams
        unigrams_frequency = dict(FreqDist(corpus))

        # create a corpus with frequency filtration
        corpus_freq = [token for token in corpus if
                       unigrams_frequency[token] >= filter_freq_n]

        bigrams = list(nltk.bigrams(corpus_freq))

        return bigrams


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class TestCandidateSelection(unittest.TestCase):
    """A class for CandidateSelection units testing."""

    def test_text_files_getter(self):
        """
        Test that Method can get data from a given folder and convert it into
        bigrams, checking the accepted POS-Tags combinations.
        """
        folder_name = 'test_folder'
        opt = CandidateSelection().frequency_filter
        noun = CandidateSelection().isNoun
        adj = CandidateSelection().isAdjective
        v = CandidateSelection().isVerb
        res = CandidateSelection().text_files_getter(folder_name, 0,
                                                     function=opt,
                                                     is_noun=noun,
                                                     is_adj=adj,
                                                     is_verb=v)
        self.assertEqual(list(res[0].keys()), [('language', 'processing')],
                         "incorrect result may be caused by hidden files \
                        (e.g. .DS_Store on Mac OS). Make sure they are \
                        deleted.")
        print("Text files getter testing is successfully executed!")

    def test_reuters_corpus(self):
        """Check if a dictionary with frequencies was created."""
        opt = CandidateSelection().frequency_filter
        res = CandidateSelection().reuters_corpus(function=opt)
        tuple_res = type(res[0]) is dict
        self.assertTrue(tuple_res, "reuters_freq result doesn't contain \
                        dictionary.")
        print("Reuters corpus testing is successfully executed!")

    def test_filter_text_files(self):
        """Test that tokens are in lowercase and filtered."""
        corpus = ['Language', 'proceSsing', 'linguistics', 'PROVIDES',
                  'automatic', 'language', 'processing', 'the', '12345']
        opt = CandidateSelection().frequency_filter
        res = CandidateSelection().filter_text_files(corpus, 2, function=opt)
        expect = [('language', 'processing'), ('processing', 'language'),
                  ('language', 'processing')]
        self.assertEqual(expect, res, "either stop words/ numbers or \
                          punctuation were not removed or tokens are not in \
                              a lower case.")
        print("Text files filter testing is successfully executed!")

    def test_frequency_filter_tuple(self):
        """Test that a result element is a tuple."""
        tokens = ['language', 'processing', 'linguistics', 'provides',
                  'automatic', 'language', 'processing']
        res = CandidateSelection().frequency_filter(tokens, 0)
        for element in res:
            self.assertIsInstance(element, tuple,
                                  "result elements should be tuples")
        print("Frequency filter tests are successfully executed!")

    def test_frequency_filter_result(self):
        """Test that all the words with the frequency < 3 will be ignored."""
        tokens = ['language', 'processing', 'linguistics', 'provides',
                  'automatic', 'language', 'processing']
        res = CandidateSelection().frequency_filter(tokens, 3)
        self.assertCountEqual(res, [],
                              "doesn't correspond the expected result.")
        print("Frequency filter tests are successfully executed!")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def candidate_selection_demo():
    """Demonstrate how CandidateSelection class can be used."""
    print("\n")
    print("--------------------------------------")
    print("CandidateSelection Class Demonstration")
    print("--------------------------------------")
    print("\n")
    print('Tokenize txt-files: ')
    print("\n")
    print("['Machine', 'learning', 'data', 'outcome']; " +
          "['Machine', 'learning', 'analyses', 'data', 'and', 'predicts', \
            'the', 'outcome']")

    """
    Txt files tokenized:
    txt1_list = ['Machine', 'learning', 'data', 'outcome']
    txt2_list = ['Machine', 'learning', 'analyses', 'data', 'and', 'predicts',
                 'the', 'outcome']
    """

    print("\n")
    print("=======================================")
    print("\n")
    print("isNoun : ('data', 'NN') -> Noun \n isAdjective: \
          ('nice', 'JJ') -> Adjective")
    print("\n")

    # The whole corpus
    txt1_2 = ['Machine', 'learning', 'data', 'outcome', 'Machine', 'learning',
              'analyses', 'data', 'and', 'predicts', 'the', 'outcome']

    # Create bigrams for the whole coprus after filtering
    corpus = CandidateSelection().filter_text_files(txt1_2, 2)

    # Create bigrams for txt-files after filtering
    cand_doc = [
        [('machine', 'learning'), ('learning', 'data'), ('data', 'outcome')],
        [('machine', 'learning'), ('learning', 'analyses'),
         ('analyses', 'data'), ('data', 'predicts'), ('predicts', 'outcome')]]

    candidates = [('machine', 'learning'), ('learning', 'data'),
                  ('data', 'outcome'), ('machine', 'learning'),
                  ('learning', 'analyses'), ('analyses', 'data'),
                  ('data', 'predicts'), ('predicts', 'outcome')]

    candidates_total_freq = dict(nltk.FreqDist(candidates))
    candidates_per_doc_freq = []
    for doc in cand_doc:
        candidates_per_doc_freq.append(dict(nltk.FreqDist(doc)))

    print("\n")
    print("=======================================")
    print("\n")
    print('Get candidate terms for the whole corpus with the word frequency',
          'filtration = 2: ')
    print("\n")
    print(corpus)

    print("\n")
    print("=======================================")
    print("\n")
    print('Get candidates with absolute frequencies per text :')
    print("\n")
    print(candidates_per_doc_freq)

    print("\n")
    print("=======================================")
    print("\n")
    print('Get candidates with absolute frequencies across all texts :')
    print("\n")
    print(candidates_total_freq)

    print("\n")
    print("=======================================")
    print("\n")
    print('To extract data from nltk.corpus.reuters and create candidates',
          'on the same principle, use reuters_corpus() Method.')
    print("\n")
    print("==================================================================")
    print("\n")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    candidate_selection_demo()
    unittest.main()
    print("\n")
    print("CandidateSelection Class testing is done!")
