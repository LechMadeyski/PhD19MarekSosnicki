#!/usr/bin/env python

"""
Creates html representation of findings
"""

import argparse
import sys
import configuration
import logging
import runpy
import os
import json

from utilities import load_function, load_variable, getDoiFilename, createDirectoryIfNotExists, createDirectoryIfNotExistsOrClean
from SearchResultHtmlDisplay.findingsToHtml import findingsToHtml


from distutils.dir_util import copy_tree


def run_results_html_generation(articles, outputFolder):
    createDirectoryIfNotExistsOrClean(outputFolder)

    staticIncludesPath = os.path.dirname(os.path.abspath(__file__)) + "/materialize"
    copy_tree(staticIncludesPath, outputFolder)

    logger = logging.getLogger("run_results_html_generation")
    for doi, articleData in articles.items():
        logger.info("Creating html for " + doi)
        with open(getDoiFilename(outputFolder, doi, "html"), 'w', encoding='utf-8') as f:
          f.write(findingsToHtml(articleData["article"], articleData["findings"]))


def prepareArticles(finderResultsFolder, articlesJsons):
    result = dict()

    for foundFilename in os.listdir(finderResultsFolder):
        articleFullPath = articlesJsons+"/"+foundFilename
        foundFullPath = finderResultsFolder + "/" + foundFilename
        with open(articleFullPath, 'r') as articleFile:
            with open(foundFullPath, 'r') as foundFile:
                foundData = json.load(foundFile)
                foundArticle = json.load(articleFile)
                result[foundArticle["doi"]] = {"article" : foundArticle, "findings" : foundData}
    return result

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--output_finder', default='outputFinder', type=str, help='Location for finder result .json files')
    parser.add_argument('--output_html', default='outputHtml', type=str, help='Location for result .html files')
    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_results_html_generation')

    p = getArgumentsParser();
    a = p.parse_args(args=args)

    logger.info("Starting run_results_html_generation with following arguments")
    logger.info("output_articles = " + a.output_articles)
    logger.info("output_finder = " + str(a.output_finder))
    logger.info("output_html = " + a.output_html)

    run_results_html_generation(prepareArticles(a.output_finder, a.output_articles), a.output_html)


if __name__ == '__main__': sys.exit(main())