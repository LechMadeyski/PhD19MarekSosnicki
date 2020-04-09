
from .ArticleData import ArticleData
from .format_text_and_split_into_sentences import format_text_and_split_into_sentences

import os
from pprint import pprint
import rispy


def __entry_to_article_data(entry):
    res = ArticleData()
    res.title = entry.get('title', str())
    res.authors = entry.get('authors', list())
    res.issn = entry.get('issn', str())
    res.publisher = entry.get('publisher', str())
    res.doi = entry.get('doi', str())
    res.journal_name = entry.get('journal_name', str())
    res.publish_year = entry.get('year', str())

    if entry.get('abstract', None):
        res.text = [dict(
            title='Abstract',
            paragraphs=[dict(sentences=format_text_and_split_into_sentences(entry.get('abstract')))])]
    return res


def ris_to_article_data(filepath):
    with open(filepath, 'r', buffering=-1, encoding=None) as bibliography_file:
        file_as_string = bibliography_file.read()
        entries = rispy.loads(file_as_string)
        for entry in entries:
            print('Analyzing entry ' + str(entry))
            return __entry_to_article_data(entry)
    raise AssertionError('Could not find proper ris entry')

