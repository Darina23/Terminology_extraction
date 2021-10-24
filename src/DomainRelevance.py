#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 05.03.2021
# Mac OS
"""
Zweck: die Häufigkeit von Kandidaten in Domäne- vs. Referenzkorpus zu erfassen.

Autorin: Daryna Ivanova
"""

import unittest


class DomainRelevance():
    """
    Get the frequency of a candidate term across different corpora.

    Methods
    -------
    cond_probability_and_abs_frequency(corpus: list)
        Compute conditional probability P(t|D) of a term in a  whole corpus and
        an absolute frequency of a bigram.

    relevance(domain_terms_probability: dict, reference_corpus_tprob: dict)
        Computes Domain Relevance DR regarding to P(t|D) for domain and
        reference corpus.
    """

    def cond_probability(self, candidates: list,
                         candidates_total: dict) -> dict:
        """
        Estimate a conditional probability P(t|D) of a candidate term.

        Parameters
        ----------
        candidates : list
            Bigrams from the whole corpus.
        candidates_total : dict
            Bigrams and their absolute frequencies across all texts.

        Returns
        -------
        candidates_probability : dict
            Candidate and conditional probability.

        """
        candidates_probability = {}

        # number of occurences for each term across all texts
        occurence_total = sum(candidates_total.values())

        for candidate in candidates:
            frequency = candidates_total[candidate]

            # conditional probability of a candidate term
            probability = frequency / occurence_total

            candidates_probability[candidate] = probability

        return candidates_probability

    def relevance(self, domain_tprob: dict,
                  reference_tprob: dict, candidates: list) -> dict:
        """
        Compare the frequency of a candidate term across different corpora.

        Parameters
        ----------
        domain_tprob : dict
            Takes a dictionary with candidate terms and their conditional
            probabilities from the domain corpus.
        reference_tprob : dict
            Takes a dictionary with candidate terms and their conditional
            probabilities from the reference corpus.
        candidates : list
            Candidates from the whole corpus.

        Returns
        -------
        domain_relevance : dict
            Dictionary with the candidate terms for keys and their Domain
            Relevance scores for values.

        """
        domain_relevance = {}

        for candidate in candidates:
            if candidate in reference_tprob.keys():
                d = domain_tprob[candidate]

                # Domain Relevance
                dr = d / \
                    (d +
                     reference_tprob[candidate])

                domain_relevance[candidate] = dr
            else:
                # If a candidate is not in a reference corpus
                domain_relevance[candidate] = 1

        return domain_relevance


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class DomainRelevanceTest(unittest.TestCase):
    """A class for DomainRelevance units testing."""

    def test_cond_probability(self):
        """Test that an actual result corresponds the expected one."""
        candidates_total = {('language', 'processing'): 2,
                            ('linguistics', 'provides'): 1,
                            ('automatic', 'language'): 1}
        candidates = [('language', 'processing'), ('linguistics', 'provides'),
                      ('automatic', 'language'), ('language', 'processing')]

        res = DomainRelevance().cond_probability(candidates, candidates_total)

        expected_res = {('language', 'processing'): 0.5,
                        ('linguistics', 'provides'): 0.25,
                        ('automatic', 'language'): 0.25}
        self.assertEqual(res, expected_res,
                         "doesn't correspond the expected result.")
        print("Conditional probability testing is successfully executed!")

    def test_relevance(self):
        """Test that DR scores are not greater than 1."""
        reference_tprob = {('machine', 'learning'): 0.5,
                           ('automatic', 'langugage'): 0.25,
                           ('data', 'output'): 0.75,
                           ('outcome', 'analyses'): 0.14,
                           ('climate', 'catastrophy'): 0.29,
                           ('big', 'question'): 0.345,
                           ('predicts', 'outcome'): 0.14}

        candidates = [('language', 'processing'), ('linguistics', 'provides'),
                      ('automatic', 'language'), ('language', 'processing')]

        domain_tprob = {('language', 'processing'): 0.5,
                        ('linguistics', 'provides'): 0.25,
                        ('automatic', 'language'): 0.25}

        res = DomainRelevance().relevance(domain_tprob, reference_tprob,
                                          candidates)
        for score in res.values():
            self.assertLessEqual(score, 1, "DR scores must be <= 1")
        print("Domain Relevance testing is successfully executed!")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def domain_relevance_demo():
    """Demonstrate how DomainRelevance class can be used."""
    print("\n")
    print("-----------------------------------")
    print("DomainRelevance Class Demonstration")
    print("-----------------------------------")
    print("\n")

    # Conditional probability for reference corpus
    cond_prob_reference = {('machine', 'learning'): 0.14,
                           ('learnig', 'methods'): 0.25,
                           ('data', 'output'): 0.668,
                           ('outcome', 'analyses'): 0.14,
                           ('climate', 'catastrophy'): 0.29,
                           ('big', 'question'): 0.345,
                           ('predicts', 'outcome'): 0.14}

    # Candidates from the whole corpus
    candidates = [('machine', 'learning'), ('learning', 'data'),
                  ('data', 'outcome'), ('machine', 'learning'),
                  ('learning', 'analyses'), ('analyses', 'data'),
                  ('data', 'predicts'), ('predicts', 'outcome')]

    # Frequency per document
    candidates_total = {('machine', 'learning'): 2, ('learning', 'data'): 1,
                        ('data', 'outcome'): 1, ('learning', 'analyses'): 1,
                        ('analyses', 'data'): 1, ('data', 'predicts'): 1,
                        ('predicts', 'outcome'): 1}

    cond_prob_domain = DomainRelevance().\
        cond_probability(candidates, candidates_total)

    print("\n")
    print("\n")
    print("\n")
    print('\t', 'Conditional distibution of a candidate: ')
    print('\t', "___   ___   ___   ___   ___   ___   ___")
    print("\n")
    print("\t", "\t", "\t", "\t", "term frequency t in a corpus D")
    print("P(t|D) = ", "------------------------------------------")
    print("\t", "\t", "\t", "Σ ", "term frequency t' in a corpus D")
    print("\t", "\t", "   " "t'∈T")
    print("\n")
    print('\t', "T consists of all the candidates from the corpus")
    print("\n")
    print("\n")
    print("\n")

    print('Conditional probability for reference candidate terms: ')
    print("\n")
    print(cond_prob_reference)
    print("\n")
    print("\n")
    print('Conditional probability for domain candidate terms: ')
    print("\n")
    print(cond_prob_domain)

    print("\n")
    print("=======================================")
    print("\n")
    print('\t', 'Domain Relevance :')
    print('\t', "___   ___   ___   ___")
    print("\n")

    print("\t", "\t", "\t", "\t", "P(t|D_dom)")
    print("DR_t,Ddom = ", "----------------------------")
    print("\t", "\t", "\t", "P(t|D_dom) + P(t|D_ref)")
    print("\n")
    print("\n")
    print("=======================================")
    print("\n")

    print('Domain Relevance for a given data:')
    print("\n")
    print(DomainRelevance().relevance(cond_prob_domain, cond_prob_reference,
                                      candidates))
    print("\n")
    print("==================================================================")
    print("\n")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    domain_relevance_demo()
    unittest.main()
    print("\n")
    print("DomainRelevance Class testing is done!")
