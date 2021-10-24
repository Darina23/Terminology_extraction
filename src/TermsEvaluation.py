#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 25.03.2021
# Mac OS
"""
Zweck: die Bewertung von den Ergebnissen.

Autorin: Daryna Ivanova
"""

import unittest


class TermsEvaluation():
    """
    Evaluation of results.

    Methods
    -------
     gold_terminology(goldstandard_file: str)
         Gets terminology from a txt file.

    precision_and_recall(final_terms: dict, gold_terminology_bigrams: list)
        Calculates measures of quality and quantity.
    """

    def gold_terminology(self, goldstandard_file: str) -> list:
        """
        Convert a txt file in a list of bigrams.

        Parameters
        ----------
        goldstandard_file : str
            A file name.

        Returns
        -------
        gold_term_bigrams : list
            Terms from the gold standard.
        """
        gold_term_bigrams = []

        with open(goldstandard_file, 'r', encoding='utf-8',
                  errors='ignore') as f:

            for i in f.readlines():
                tmp = i.strip()
                gold_term_bigrams.append(tuple(tmp.split()))

        return gold_term_bigrams

    def precision_and_recall(self, final_terms: dict,
                             gold_terminology_bigrams: list) -> tuple:
        """
        Calculate precision and recall.

        Parameters
        ----------
        final_terms : list
            Final terminology for a combination with the decision scores.
        gold_terminology_bigrams : list
            Gold standard terms.

        Returns
        -------
        precision, recall : tuple
            precision : float
                The fraction of retrieved terms that are relevant to the query.
            recall : float
                 The fraction of the relevant terms that are successfully
                 retrieved.
        """
        n_of_relevant_terms = len(gold_terminology_bigrams)
        n_of_retrieved_terms = len(final_terms)
        n_of_retrieved_relevant_terms = 0

        final_terms_keys = final_terms.keys()

        for key in final_terms_keys:

            if key in gold_terminology_bigrams:
                n_of_retrieved_relevant_terms += 1

        precision = n_of_retrieved_relevant_terms / n_of_retrieved_terms
        recall = n_of_retrieved_relevant_terms / n_of_relevant_terms

        return precision, recall


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class TermsEvaluationTest(unittest.TestCase):
    """A class for TermsEvaluation units testing."""

    def test_gold_terminology(self):
        """Test gold_termiology(goldstandard_file: str) method."""
        path_to_file = "toy_goldstandard.txt"
        self.assertEqual(TermsEvaluation().gold_terminology(path_to_file),
                         [('computational', 'linguistics'),
                          ('language', 'processing'),
                          ('automatic', 'processing'),
                          ('data', 'driven'),
                          ('machine', 'learning'),
                          ('applied', 'linguistics'),
                          ('data', 'mining')], "incorrect data extraction!")
        print("Gold terminology convertation test is successfully executed!")

    def test_precision_and_recall(self):
        """Test that precision and recall return correct results."""
        final_terms = {('machine', 'learning'): 0.8, ('data', 'mining'): 0.75}
        gold_terms = [('computational', 'linguistics'),
                      ('language', 'processing'),
                      ('automatic', 'processing'),
                      ('data', 'driven'),
                      ('machine', 'learning'),
                      ('applied', 'linguistics'),
                      ('data', 'mining')]
        self.assertTupleEqual(TermsEvaluation().precision_and_recall(
            final_terms, gold_terms), (1.0, 0.2857142857142857),
            "incorrect result.")
        print("Precision and recall test is successfully executed!")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def terms_evaluation_demo():
    """Demonstrate how TermsEvaluation class can be used."""
    print("\n")
    print("-------------------------------------")
    print("TermsEvaluation Class Demonstration")
    print("-------------------------------------")
    print("\n")

    # toy_goldstandard.txt after applying gold_terminology() Method:
    toy_goldstandard = [('computational', 'linguistics'),
                        ('language', 'processing'),
                        ('computational', 'models'),
                        ('statistical', 'processes'),
                        ('automatic', 'processing'),
                        ('data', 'driven'), ('machine', 'learning'),
                        ('applied', 'linguistics'), ('big', 'data'),
                        ('computational', 'semantics'), ('data', 'mining')]

    print("\t", "Converted data from a gold standard file for the result",
          "evaluation step: ")
    print("\n")
    print(str(toy_goldstandard))
    print("\n")

    print("=======================================")
    print("\n")

    n_of_relevant_terms = 11
    n_of_retrieved_terms = 40
    n_of_retrieved_relevant_terms = 5

    precision = n_of_retrieved_relevant_terms / n_of_retrieved_terms
    recall = n_of_retrieved_relevant_terms / n_of_relevant_terms

    print('\t', "Compute precision and recall: ")
    print("\n")
    print("Precision = n_of_retrieved_relevant_terms / n_of_retrieved_terms")
    print("Recall = n_of_retrieved_relevant_terms / n_of_relevant_terms")
    print("\n")
    print('\t', '\t', "###   ###   ###")
    print("\n")

    # toy values
    print('\t', '\t', "Number of relevant terms: 11")
    print('\t', '\t', "Number of retrieved terms: 40")
    print('\t', '\t', "Number of retrieved and relevant terms: 5")
    print("\n")
    print('\t', '\t', "###   ###   ###")
    print("\n")

    print("===========================================")
    print('\t', '\t', "Precision: ", "\t", precision)
    print('\t', '\t', 'Recall: ', '\t', recall)
    print("===========================================")
    print("\n")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    terms_evaluation_demo()
    unittest.main()
    print("\n")
    print("TermsEvaluation Class testing is done!")
