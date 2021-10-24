#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 12.03.2021
# Mac OS
"""
Zweck: die Berechnung der Entscheidungspunktzahl für jeden Termkandidat.

Autorin: Daryna Ivanova
"""

import unittest
import os


class TermDecision():
    """
    Choose final terms and calculate decision scores.

    Methods
    -------
    decision_function(candidates: list, relevance: dict, consensus: dict,
                      alpha: float, theta: float)
        Determine if a candidate is a term according to it's score.
    """

    def decision_function(self, candidates: list, relevance: dict,
                          consensus: dict, alpha: float, theta: float) -> dict:
        """
        Decide if a candidate belongs to final terminology.

        Parameters
        ----------
        candidates : list
            Bigrams of the whole corpus.
        relevance : dict
            Domain relevance for each term.
        consensus : dict
            Domain consensus for each term.
        alpha : float
            A factor, which controls the cotribution of domain relevance and
            domain consensus scores.
        theta : float
            A threshold needed to be reached for a candidate to refer to the
            final terminology.

        Returns
        -------
        result : dict
            Terms with their decision scores.
        """
        decision_scores = {}

        final_terms = {}

        for candidate in candidates:

            # decision scores
            f_t = alpha * relevance[candidate] \
                + (1 - alpha) * consensus[candidate]

            decision_scores[candidate] = f_t

        # automated decision if a candidate belongs to terms
        for term, value in decision_scores.items():

            if value > theta:
                final_terms[term] = value

        return final_terms

    def outputter(self, alpha: float, theta: float, final_terms: dict):
        """
        Create an output txt files for each alpha/theta combination.

        Write down an alpha/theta combination at the beginning of a file and
        final terms with theit desocion scores.

        Parameters
        ----------
        alpha : float
            A factor, which controls the cotribution of domain relevance and
            domain consensus scores.
        theta : float
            A threshold needed to be reached for a candidate to refer to the
            final terminology.
        final_terms : dict
            Final terms and their desicion scores.

        Returns
        -------
        None.
        """
        # create txt file with result according to alpha and theta values
        with open(os.getcwd() + "/Output/" + "result_" + str(alpha) + "_" +
                  str(theta) + ".txt", 'w') as f:

            f.write("\u03b1 = " + str(alpha) + ', ' + "\u03b8 = " +
                    str(theta) + '\n')

            for key, value in final_terms.items():
                f.write(key[0] + ' ' + key[1] + '\t' + str(value) + '\n')


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class TermDecisionTest(unittest.TestCase):
    """A class for TermDecision units testing."""

    def test_decision_function(self):
        """Test that the method returnes correct result."""
        candidates = [('a', 'b'), ('a', 'c'), ('a', 'a'), ('a', 'b')]
        relevance = {('a', 'b'): 1.0, ('a', 'c'): 0.25, ('a', 'a'): 0.5}
        consensus = {('a', 'b'): 0.5, ('a', 'c'): 0.01, ('a', 'a'): 0.1}
        alpha = 0.6
        theta = 0.3
        result = {('a', 'b'): 0.8, ('a', 'a'): 0.33999999999999997}

        self.assertEqual(TermDecision().decision_function(candidates,
                                                          relevance, consensus,
                                                          alpha, theta),
                         result, "result is not correct.")
        print("Decision function testing is successfully executed!")

    def test_outputter(self):
        """Test  that outputter() method creates a file."""
        alpha = 0.6
        theta = 0.3
        final_terms = {('a', 'b'): 0.8, ('a', 'a'): 0.33999999999999997}
        TermDecision().outputter(alpha, theta, final_terms)

        outputter_result = os.getcwd() + "/Output/result_0.6_0.3.txt"
        self.assertTrue(os.path.isfile(outputter_result),
                        "no such file was found.")
        print("Output functionn testing is successfully executed!")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def term_decision_demo():
    """Demonstrate how TermDecision class can be used."""
    print("\n")
    print("--------------------------------------")
    print("TermDecision Class Demonstration")
    print("--------------------------------------")
    print("\n")

    # Candidates from the whole corpus
    candidates = [('machine', 'learning'), ('learning', 'data'),
                  ('data', 'outcome'), ('machine', 'learning'),
                  ('learning', 'analyses'), ('analyses', 'data'),
                  ('data', 'predicts'), ('predicts', 'outcome')]

    consensus = {('machine', 'learning'): 1.0, ('learning', 'data'): 0.0,
                 ('data', 'outcome'): 0.0, ('learning', 'analyses'): 0.0,
                 ('analyses', 'data'): 0.0, ('data', 'predicts'): 0.0,
                 ('predicts', 'outcome'): 0.0}

    relevance = {('machine', 'learning'): 0.641025641025641,
                 ('learning', 'data'): 1, ('data', 'outcome'): 1,
                 ('learning', 'analyses'): 1, ('analyses', 'data'): 1,
                 ('data', 'predicts'): 1,
                 ('predicts', 'outcome'): 0.4716981132075471}

    # Candidates, Domain Consensus and DomainTelevace demonstration
    print('\t', "Candidates:")
    print('\t', "___   ___")
    print("\n")
    print(candidates)
    print("\n")
    print('\t', "Domain Consensus: ")
    print('\t', "___   ___   ___")
    print("\n")
    print(consensus)
    print("\n")
    print('\t', "Domain Relevance:")
    print('\t', "___   ___   ___")
    print("\n")
    print(relevance)

    # Compute Decision Function
    print("\n")
    print("=======================================")
    print("\n")
    print('\t', '\t', '\t', 'Decision Function:')
    print("\n")
    print("=======================================")
    print("\n")
    print('\t', '\t', "f(t) = αDR_t,Ddom + (1 - α) DC_t,Ddom")
    print("\n")
    print('\t', '\t', '\t', '\t', '\t', '\t', "||")
    print('\t', '\t', '\t', '\t', '\t', '\t', "\/")
    print("\n")
    print('\t', '\t', "f(t) > θ => Final Terminology")

    print("\n")
    print("=======================================")
    print("\n")
    print('\t', 'Compute decision function for the given data :')
    print('\t', "___   ___   ___   ___   ___   ___   ___   ___")
    print("\n")
    print('Alpha: 0.5')
    print('Theta: 0.8')
    print("\n")
    final_terms = TermDecision().decision_function(candidates, relevance,
                                                   consensus, 0.5, 0.8)
    print("f(t) = ", final_terms)
    print("Output/ :", "result_0.5_0.8.txt")
    print("\n")
    print("==================================================================")
    print("\n")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    term_decision_demo()
    unittest.main()
    print("\n")
    print("TermDecision Class testing is done!")
