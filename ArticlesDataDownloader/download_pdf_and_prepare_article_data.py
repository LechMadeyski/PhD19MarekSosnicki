import os

from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_utilities import download_file_from_link_to_path, clear_download_directory
from ArticlesDataDownloader.extract_text_from_pdf import read_pdf_as_json


def download_pdf_and_prepare_article_data(
        driver,
        pdf_link,
        output_filename='temporary.pdf',
        should_clear_file=True):
    try:
        if os.path.isfile(output_filename):
            os.remove(output_filename)
        download_file_from_link_to_path(driver, pdf_link, output_filename)
        result_reading = ArticleData(text=read_pdf_as_json(output_filename))
    except Exception as error:
        if should_clear_file and os.path.isfile(output_filename):
            os.remove(output_filename)
        return None

    if should_clear_file:
        os.remove(output_filename)
    return result_reading


def download_pdf(
        driver,
        pdf_link,
        output_filename='temporary.pdf'):
    try:
        clear_download_directory()
        return download_file_from_link_to_path(driver, pdf_link, output_filename)
    except Exception as error:
        return None
