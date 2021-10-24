#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 10.03.2021
# Mac OS
"""
Zweck: die Programmausführung.

Autorin: Daryna Ivanova
"""

from datetime import datetime
from src.CandidateSelection import CandidateSelection
from src.DomainRelevance import DomainRelevance
from src.DomainConsensus import DomainConsensus
from src.TermDecision import TermDecision
from src.ConsoleParser import ConsoleParser
from src.TermsEvaluation import TermsEvaluation


def main():
    """Program execution."""
    now = datetime.now()
    print("\n", "Starting at " + str(now))

    # Parse command-line arguments
    parser = ConsoleParser()
    texts, alphas, thetas, goldstandard_file = parser.parse()

    # Domain corpus candidates, frequency distribution
    candidates_total, candidates_per_doc, candidates = CandidateSelection().\
        text_files_getter(texts, 3)
    print("Number of candidates: ", len(candidates))
    print("\n")

    # Reference corpus candidates, frequency distribution
    reuters_freq, reuters_bigrams = CandidateSelection().reuters_corpus()

    # Domain Relevance
    cond_prob_domain = DomainRelevance().\
        cond_probability(candidates, candidates_total)

    cond_prob_reference = DomainRelevance().\
        cond_probability(reuters_bigrams, reuters_freq)

    domain_relevance = DomainRelevance().relevance(cond_prob_domain,
                                                   cond_prob_reference,
                                                   candidates)

    # Compute Domain Consensus
    domain_term_distr = DomainConsensus().term_distr(
              candidates_total, candidates_per_doc, candidates)

    domain_consensus = DomainConsensus().domain_consensus(domain_term_distr,
                                                          candidates)

    gold_terminology = TermsEvaluation().gold_terminology(goldstandard_file)

    # Final terms and precision/recall for each alpha-theta combination
    for alpha in alphas:
        for theta in thetas:
            final_terms = TermDecision().decision_function(candidates,
                                                           domain_relevance,
                                                           domain_consensus,
                                                           alpha, theta)
            # Create files with alpha/theta results
            TermDecision().outputter(alpha, theta, final_terms)

            precision_recall = \
                TermsEvaluation().precision_and_recall(final_terms,
                                                       gold_terminology)
            # Number of final terminology
            l_final = len(final_terms)
            print("\n")
            print("For alpha = " + str(alpha) + ", theta = " + str(theta) +
                  ": precision = " + str(precision_recall[0]) + " recall = " +
                  str(precision_recall[1]))

            print("For alpha = " + str(alpha) + ", theta = " + str(theta) +
                  " number of candidates: " + str(l_final))
            print("\n")

    now = datetime.now()
    print("\n")
    print("Finishing at " + str(now))


if __name__ == "__main__":
    main()
