#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 03.03.2021
# Mac OS
"""
Zweck: die Verteilung eines Begriffs allein im Domänekorpus zu messen.

Autorin: Daryna Ivanova
"""

import unittest
import math


class DomainConsensus():
    """
    Measure the distributed use of a candidate term in the domain corpus.

    Methods
    -------
    term_distr(candidates_total: dict, candidates_per_doc: list,
               candidates: list)
        Stores a list with distribution values per document for each candidate.

    domain_consensus(ptd_per_candidate: dict, candidates: list)
        Computes the domain consensus.

    consensus_for_term(ptds_of_some_term: list)
        A procedure for domain consensus computation.
    """

    def term_distr(self, candidates_total: dict, candidates_per_doc: list,
                   candidates: list) -> dict:
        """
        Create a dict with a candidate and its distribution values.

        {key: candidate term, value: list of Pt(d) values from each document}

        Parameters
        ----------
        candidates_total : dict
            Full corpus of bigrams and their frequencies.
        candidates_per_doc : list
            Corpus of bigrams per document and their frequency values.
        candidates : list
            Bigrams from the whole corpus.

        Returns
        -------
        ptd_per_candidate : dict
            Distribution of a term across all documents.
        """
        ptd_per_candidate = {}

        # create a dict with an empty list values for each candidate in keys
        for candidate in candidates:
            ptd_per_candidate[candidate] = []

        # frequency distribution of terms per document
        for doc in candidates_per_doc:

            # calculate term distributions and store it in a list
            for key, value in doc.items():
                ptd_per_candidate[key].append(value / candidates_total[key])

        return ptd_per_candidate

    def domain_consensus(self, ptd_per_candidate: dict,
                         candidates: list) -> dict:
        """
        Measure the distributed use of a candidate in the domain corpus only.

        Parameters
        ----------
        ptd_per_candidate : dict
            Terms and list of their dictribution values.
        candidates : list
            All term candidates.

        Returns
        -------
        consensus : dict
            Terms and their consensus results.
        """
        consensus = {}

        for candidate in candidates:

            domain_consensus = \
                        self.consensus_for_term(ptd_per_candidate[candidate])

            consensus[candidate] = domain_consensus

        return consensus

    def consensus_for_term(self, ptds_of_some_term: list) -> float:
        """
        Calculate the domain consensus.

        Parameters
        ----------
        ptds_of_some_term : list
            Term distribution values from every document.

        Returns
        -------
        entropy_for_some_term : float
            Outcome.
        """
        entropy_for_some_term = 0

        for ptd in ptds_of_some_term:

            entropy_for_some_term += ptd * math.log2(1 / ptd)

        return entropy_for_some_term


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class DomainConsensusTest(unittest.TestCase):
    """A class for DomainConsensus units testing."""

    def test_term_distr(self):
        """Test that actual result corresponds the expected one."""
        # Frequency per document
        candidates_total = {
            ('machine', 'learning'): 2, ('learning', 'data'): 1,
            ('data', 'outcome'): 1}

        # Candidates from the whole corpus
        candidates = [
            ('machine', 'learning'), ('learning', 'data'),
            ('data', 'outcome'), ('machine', 'learning')
            ]

        # Frequency in the whole corpus
        candidates_per_doc = [
            {('machine', 'learning'): 1, ('learning', 'data'): 1,
             ('data', 'outcome'): 1}, {('machine', 'learning'): 1}]

        expected_result = {('machine', 'learning'): [0.5, 0.5],
                           ('learning', 'data'): [1.0],
                           ('data', 'outcome'): [1.0]}

        self.assertEqual(DomainConsensus().term_distr(candidates_total,
                                                      candidates_per_doc,
                                                      candidates),
                         expected_result, "incorrect result")

        print("Term distribution testing is successfully executed!")

    def test_domain_consensus(self):
        """Test that a result type is dictionary."""
        domain_consensus = {
            ('machine', 'learning'): 1.0, ('learning', 'data'): 0.0,
            ('data', 'outcome'): 0.0}
        self.assertIsInstance(domain_consensus, dict,
                              "output value should be of dict type.")
        print("Domain consensus method testing is done!")

    def test_consensus_for_term(self):
        """Test that result is a float number."""
        ptd_for_a_term = [0.01, 0.5]
        self.assertIsNotNone(DomainConsensus().consensus_for_term(
                                                        ptd_for_a_term),
                             "a resulting value should be float, not None")
        print("Consensus for a term testing is successfully executed!")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def domain_consensus_demo():
    """Demonstrate how DomainConsensus class can be used."""
    from DomainConsensus import DomainConsensus

    print("\n")
    print("--------------------------------------")
    print("DomainConsensus Class Demonstration")
    print("--------------------------------------")
    print("\n")

    # Candidates from the whole corpus
    candidates = [('machine', 'learning'), ('learning', 'data'),
                  ('data', 'outcome'), ('machine', 'learning'),
                  ('learning', 'analyses'), ('analyses', 'data'),
                  ('data', 'predicts'), ('predicts', 'outcome')]

    # Frequency in the whole corpus
    candidates_per_doc = [
        {('machine', 'learning'): 1, ('learning', 'data'): 1,
         ('data', 'outcome'): 1},
        {('machine', 'learning'): 1, ('learning', 'analyses'): 1,
         ('analyses', 'data'): 1, ('data', 'predicts'): 1,
         ('predicts', 'outcome'): 1}]

    # Frequency per document
    candidates_total = {('machine', 'learning'): 2, ('learning', 'data'): 1,
                        ('data', 'outcome'): 1, ('learning', 'analyses'): 1,
                        ('analyses', 'data'): 1, ('data', 'predicts'): 1,
                        ('predicts', 'outcome'): 1}

    print('\t', 'The whole corpus of candidates: ')
    print('\t', "___   ___   ___   ___   ___   ___")
    print("\n")
    print(candidates)

    print("\n")
    print("\n")
    print("\n")
    print('\t', 'Distibution of a candidate t across all the texts in the',
          'domain corpus : ')
    print('\t', "___   ___   ___   ___   ___   ___   ___")
    print("\n")
    print("\t", "\t", "\t", "\t", "term frequency t in a text d")
    print("P_t (D) = ", "------------------------------------------")
    print("\t", "\t", "\t", "Σ ", "term frequency t' in a text d' ")
    print("\t", "\t", "   " "d'∈D")
    print("\n")
    print('\t', "D consists of all the domain corpus texts")
    print("\n")
    print("\n")
    print("\n")

    term_distribution = DomainConsensus().term_distr(candidates_total,
                                                     candidates_per_doc,
                                                     candidates)

    print('\t', "Term distribution for the whole domain corpus: ")
    print('\t', "___   ___   ___   ___   ___   ___   ___   ___")
    print("\n")
    print(term_distribution)

    print("\n")
    print("=======================================")
    print("\n")
    print('\t', 'Domain Consensus :')
    print('\t', "___   ___   ___   ___")
    print("\n")

    print("\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t", "\t",
          "   1")
    print("DC_t,Ddom = H(P_t (d)) = Σ", "( P_t (d') log -------- )")
    print("\t", "\t", "\t", "\t", "\t", "   d'∈D_dom", "\t", "\t",
          "P_t (d')")
    print("\n")
    print("\n")

    # compute domain consensus
    compute_consensus = \
        DomainConsensus().domain_consensus(term_distribution, candidates)
    print("Domain Consensus for a given corpus(DR_t,Ddom) :")
    print("\n")
    print(compute_consensus)

    print("\n")
    print("==================================================================")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    domain_consensus_demo()
    unittest.main()
    print("\n")
    print("DomainConsensus Class testing is done!")
