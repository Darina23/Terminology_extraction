#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Datum: 25.03.2021
# Mac OS
"""
Zweck: Programmauführung in der Kommandozeile. Hilfsklasse.

Autorin: Daryna Ivanova
"""

import unittest
import argparse
import mock


class ConsoleParser():
    """
    Parser class for command line arguments.

    Methods
    -------
    parse()
        Defines required arguments and parses them.
    """

    def parse(self) -> tuple:
        """
        Parse a command line input.

        Returns
        -------
        output: tuple
            Parsed arguments.

        """
        parser = argparse.ArgumentParser(description='Terminology extraction.\
                                         Program execution.')
        parser.add_argument('corpus', type=str, help='Directory name.')

        parser.add_argument('alpha',  type=str, help='A factor, which \
                            controls the cotribution of domain relevance and \
                                domain consensus scores.')
        parser.add_argument('theta', type=str, help='A threshold needed to \
                            be reached for a candidate to refer to the final \
                                terminology.')
        parser.add_argument('goldstandard_file', type=str, help='A txt file \
                            with the gold terminology')

        args = parser.parse_args()

        # split alpha values
        alphas_list_str = args.alpha.split(', ')
        thetas_list_str = args.theta.split(', ')

        alphas_list = []
        thetas_list = []

        # convert alpha and theta values into float numbers
        for alpha in alphas_list_str:
            alphas_list.append(float(alpha))

        for theta in thetas_list_str:
            thetas_list.append(float(theta))

        output = args.corpus, alphas_list, thetas_list, args.goldstandard_file

        return output


##############################################################################
#                    A CLASS TESTING AND DEMONSTRATION                       #
##############################################################################


                 ###################
                 ###   TESTING   ###
                 ###################


class ConsoleParserTest(unittest.TestCase):
    """Test ConsoleParser class units."""

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(corpus="clt", alpha="0.2",
                                                theta="0.4",
                                                goldstandard_file="gold.txt"))
    def test_parse(self, mock_args):
        """Test that the command-line arguments are parsed."""
        res = ConsoleParser().parse()
        self.assertEqual(res, ("clt", [0.2], [0.4], "gold.txt"),
                         "arguments are not parsed.")
        print("Arguments were successfully parsed.")


                 ##########################
                 ###   DEMONSTRATION   ####
                 ##########################


def console_parser_demo():
    """Demonstrate how ConsoleParser class can be used."""
    print("\n")
    print("--------------------------------------")
    print("ConsoleParser Class Demonstration")
    print("--------------------------------------")
    print("\n")
    print('\t', "Command-line input: ")
    print("\n")
    print("================================================================" +
          "=========================")
    print("python3 main.py acl_texts '0.3, 0.7, 0.9' '0.2, 0.5, 0.95'",
          "gold_terminology.txt")
    print("================================================================" +
          "=========================")
    print("\n")
    print("\t", "Parsed arguments:", "\t", "acl_texts/ ", " [0.3, 0.7, 0.9]",
          " [0.2, 0.5, 0.95]", " gold_terminology.txt")
    print("\n")
    print("==================================================================")
    print("\n")
    print("\n")
    print("TESTING BEGINS...")
    print("\n")


if __name__ == "__main__":
    console_parser_demo()
    unittest.main()
    print("\n")
    print("ConsoleParser Class testing is done!")
