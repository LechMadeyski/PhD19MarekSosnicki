import pytest
import os
import shutil

from ArticlesDataDownloader.ArticleData import ArticleData
from .ArticlesDataDownloader import ArticlesDataDownloader

TEST_DIRECTORY = ".test_directory"
SHOULD_CLEAR = False


@pytest.fixture
def setup_downloader(should_clear = SHOULD_CLEAR):
    if should_clear:
        if os.path.exists(TEST_DIRECTORY):
            shutil.rmtree(TEST_DIRECTORY)
        os.makedirs(TEST_DIRECTORY)
    elif not os.path.exists(TEST_DIRECTORY):
        os.makedirs(TEST_DIRECTORY)

    proxy_file = 'proxy_auth_plugin.zip'
    if not os.path.exists(proxy_file):
        proxy_file = None
    downloader = ArticlesDataDownloader(TEST_DIRECTORY, proxy_file)
    yield downloader
    if should_clear:
        shutil.rmtree(TEST_DIRECTORY)


def test_science_direct_html_by_doi(setup_downloader):
    DOI = "10.1016/j.ins.2019.08.077"
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))
    # TODO: add other bibliographic data - failing for now basing on ris

    assert filename == TEST_DIRECTORY + '/10.1016_j.ins.2019.08.077.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1016_j.ins.2019.08.077.pdf')

    assert result_data.publisher_link == 'https://linkinghub.elsevier.com/retrieve/pii/S0020025519308242'
    assert result_data.publish_year == '2020'

    assert result_data.read_status == 'OK'
    assert result_data.title == 'ABFL: An autoencoder based practical approach for software fault localization'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 6
    assert len(result_data.text) == 31
    assert 'Abstract' in result_data.text[0]['title']
    assert len(result_data.text[0]['paragraphs']) == 1
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 7
    assert 'Introduction' in result_data.text[1]['title']
    assert 'Background' in result_data.text[2]['title']
    assert 'Spectrum Based Fault Localization' in result_data.text[3]['title']
    assert len(result_data.text[3]['paragraphs'][0]['sentences']) == 3
    assert 'Conclusion and future work' in result_data.text[-3]['title']
    assert 'Declaration of Competing Interest' in result_data.text[-2]['title']
    assert 'Acknowledgments' in result_data.text[-1]['title']


# No access to article
# def test_springer_html_by_doi_chapter(setup_downloader):
#     DOI = '10.1007/978-3-030-38364-0_32'
#     filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))
#
#     assert filename == TEST_DIRECTORY + '/10.1007_978-3-030-38364-0_32.json'
#     assert os.path.isfile(TEST_DIRECTORY + '/10.1007_978-3-030-38364-0_32.pdf')
#
#     assert result_data.publisher_link == 'http://link.springer.com/10.1007/978-3-030-38364-0_32'
#     assert result_data.publish_year == '2020'
#
#     assert result_data.read_status == 'OK'
#     assert result_data.start_page == '361'
#     assert result_data.end_page == '369'
#     assert result_data.title == 'An Improvement of Applying Multi-objective Optimization Algorithm into Higher Order Mutation Testing'
#     assert result_data.doi == DOI
#     assert len(result_data.authors) == 2
#     assert len(result_data.text) == 9
#     assert result_data.text[0]['title'] == 'Abstract'
#     assert len(result_data.text[0]['paragraphs']) == 1
#     assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 3
#     assert 'Introduction' in result_data.text[1]['title']
#     assert len(result_data.text[1]['paragraphs']) == 5
#     assert len(result_data.text[1]['paragraphs'][3]['sentences']) == 3
#     assert 'Proposed Approach and Related Works' in result_data.text[2]['title']
#     assert 'Supporting Tool and PUTs' in result_data.text[3]['title']
#     assert 'Results Analysis' in result_data.text[4]['title']
#     assert 'Conclusions' in result_data.text[5]['title']
#     assert 'Notes' in result_data.text[6]['title']


def test_springer_pdf_by_doi_articles(setup_downloader):
    DOI = '10.1007/BF03192394'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1007_BF03192394.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1007_BF03192394.pdf')

    assert result_data.publisher_link == 'https://journal-bcs.springeropen.com/articles/10.1007/BF03192394'
    assert result_data.publish_year == '2006'

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == 'Muta-Pro: Towards the definition of a mutation testing process'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 4
    assert len(result_data.text) == 14
    assert result_data.text[0]['title'] == 'Abstract'


def test_willey_html_by_doi(setup_downloader):
    DOI = '10.1002/stvr.1728'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1002_stvr.1728.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1002_stvr.1728.pdf')

    assert result_data.publisher_link == 'https://onlinelibrary.wiley.com/doi/abs/10.1002/stvr.1728'

    assert result_data.read_status == 'OK'
    assert result_data.title == 'Performance mutation testing'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 4
    assert len(result_data.text) == 36
    assert result_data.text[0]['title'] == 'Abstract'
    assert len(result_data.text[0]['paragraphs']) == 1
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 11
    assert 'Introduction' in result_data.text[1]['title']
    assert len(result_data.text[1]['paragraphs']) == 7
    assert len(result_data.text[1]['paragraphs'][4]['sentences']) == 7
    assert 'Background' in result_data.text[2]['title']
    assert '2.1 Performance bugs' in result_data.text[3]['title']
    assert '2.2 Mutation testing' in result_data.text[4]['title']
    assert 'Problem Statement' in result_data.text[5]['title']
    assert len(result_data.text[5]['paragraphs']) == 9
    assert len(result_data.text[5]['paragraphs'][6]['sentences']) == 5
    assert 'Research Questions' in result_data.text[6]['title']

    assert 'Unnecessary Recalculation of Values (URV)' in result_data.text[10]['title']
    assert len(result_data.text[10]['paragraphs']) == 5

    assert '6.1 Subjects under test' in result_data.text[17]['title']
    assert len(result_data.text[17]['paragraphs']) == 15

    assert 'Conclusion and Future Work' in result_data.text[-2]['title']
    assert 'Acknowledgements' in result_data.text[-1]['title']


def test_ieee_html_by_doi(setup_downloader):
    DOI = '10.1109/APSEC48747.2019.00022'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1109_APSEC48747.2019.00022.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1109_APSEC48747.2019.00022.pdf')

    assert result_data.publisher_link == 'https://ieeexplore.ieee.org/document/8946088/'

    assert result_data.publish_year == '2019'

    assert result_data.read_status == 'OK'
    assert result_data.title == 'A Mutation-Based Approach for Assessing Weight Coverage of a Path Planner'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 4
    assert len(result_data.text) == 9
    assert result_data.text[0]['title'] == 'Abstract'
    assert len(result_data.text[0]['paragraphs']) == 1
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 7
    assert 'Introduction' in result_data.text[1]['title']
    assert len(result_data.text[1]['paragraphs']) == 12
    assert len(result_data.text[1]['paragraphs'][6]['sentences']) == 5
    assert 'Definitions' in result_data.text[2]['title']
    assert 'Proposed Approach' in result_data.text[3]['title']
    assert 'Experiments' in result_data.text[4]['title']
    assert 'Discussion' in result_data.text[5]['title']
    assert 'Threats To Validity' in result_data.text[6]['title']
    assert 'Related Work' in result_data.text[7]['title']
    assert 'Conclusions' in result_data.text[8]['title']


def test_acm_pdf_by_doi(setup_downloader):
    DOI = '10.1145/3293882.3330574'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1145_3293882.3330574.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1145_3293882.3330574.pdf')

    assert result_data.publisher_link == 'http://dl.acm.org/citation.cfm?doid=3293882.3330574'
    assert result_data.publish_year == '2019'

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == "DeepFL: Integrating Multiple Fault Diagnosis Dimensions for Deep Fault Localization"
    assert result_data.doi == DOI
    assert len(result_data.authors) == 4
    assert len(result_data.text) == 11
    assert result_data.text[0]['title'] == 'Abstract'
    assert len(result_data.text[0]['paragraphs']) == 1
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 9
    assert result_data.text[1]['title'] == 'Begining data'
    assert 'INTRODUCTION' in result_data.text[2]['title']
    assert len(result_data.text[2]['paragraphs']) == 1
    assert len(result_data.text[2]['paragraphs'][0]['sentences']) == 33
    assert 'BACKGROUND AND RELATED WORK' in result_data.text[3]['title']
    assert 'APPROACH' in result_data.text[4]['title']
    assert 'EXPERIMENTAL SETUP' in result_data.text[6]['title']
    assert 'RESULT ANALYSIS' in result_data.text[7]['title']
    assert 'CONCLUSION' in result_data.text[8]['title']
    assert 'ACKNOWLEDGMENTS' in result_data.text[9]['title']
    assert 'REFERENCES' in result_data.text[10]['title']


def test_article_with_scopus_link_only(setup_downloader):
    SCOPUS_LINK = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85074719668&origin=inward&txGid=743ab63d74ada4f8f3059ad6e752522e'
    filename, result_data = setup_downloader.read_article(ArticleData(filename_base='anyName', scopus_link=SCOPUS_LINK))

    assert filename == TEST_DIRECTORY + '/anyName.json'


# def test_article_with_scopus_link_that_has_publisher_link(setup_downloader):
#     SCOPUS_LINK = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-84919624650&origin=inward&txGid=0e4a6cf3a5910d1b48062317c69b926b'
#
#     filename, result_data = setup_downloader.readArticle('anyName2', SCOPUS_LINK)
#     assert filename == TEST_DIRECTORY + '/anyName2.json'
#
#     assert result_data.publish_year == '2014'


def test_acm_pdf_by_doi_2(setup_downloader):
    DOI = '10.1145/2661136.2661157'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1145_2661136.2661157.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1145_2661136.2661157.pdf')

    assert result_data.publisher_link == 'http://dl.acm.org/citation.cfm?doid=2661136.2661157'
   # assert result_data.publish_year == ''

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == 'Coverage and Its Discontents'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 3
    assert len(result_data.text) == 25
    assert result_data.text[0]['title'] == 'Abstract'
    assert len(result_data.text[0]['paragraphs']) == 1
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 6
    assert result_data.text[1]['title'] == 'Begining data'
    assert 'Introduction' in result_data.text[2]['title']
    assert len(result_data.text[2]['paragraphs']) == 1
    assert len(result_data.text[2]['paragraphs'][0]['sentences']) == 3

    # ITERATION IN PDF
    # assert 'Justifying the Use of Coverage' in result_data.text[3]['title']
    # assert 'Mutation is the Elephant in the Room' in result_data.text[4]['title']
    # assert 'How Can Users of Code Coverage Sleep\nWell at Night Again?' in result_data.text[5]['title']
    # assert 'A Sketch of a Data Set' in result_data.text[6]['title']
    # assert 'No Simple Answers' in result_data.text[7]['title']
    # assert 'The Plural of Anecdote is Not Conﬁdence' in result_data.text[8]['title']
    # assert 'Advice and Discomfort' in result_data.text[9]['title']
    # assert 'Advice for Researchers' in result_data.text[10]['title']
    # assert 'Advice for Practitioners' in result_data.text[11]['title']
    # assert 'Acknowledgments' in result_data.text[12]['title'] 
    # assert 'References' in result_data.text[13]['title']



# def test_acm_pdf_by_shall_detect_invalid_pdf_and_read_nothing(setup_downloader):
#     DOI = '10.1145/3084226.3084257'
#     filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))
#
#     assert filename == TEST_DIRECTORY + '/10.1145_3084226.3084257.json'
#     assert result_data.publisher_link == 'http://dl.acm.org/citation.cfm?doid=3084226.3084257'
#    # assert result_data.publish_year == ''
#
#     # SHOULD BE EMPTY - this one is kind of invalid
#
#     assert result_data.read_status == 'OK'
#     assert result_data.title == 'Effectiveness Assessment of an Early Testing Technique using Model-Level Mutants'
#     assert result_data.doi == DOI
#     assert len(result_data.authors) == 4
#     # assert len(result_data.text) == 1
#     # assert result_data.text[1]['title'] == 'Abstract'


def test_acm_pdf_by_doi_3(setup_downloader):
    DOI = '10.1145/3358501.3361234'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1145_3358501.3361234.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1145_3358501.3361234.pdf')

    assert result_data.publisher_link == 'http://dl.acm.org/citation.cfm?doid=3358501.3361234'
   # assert result_data.publish_year == ''

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == 'Mutation Testing for DSLs (Tool Demo)'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 4
    assert len(result_data.text) == 10
    assert result_data.text[0]['title'] == 'Abstract'
    assert len(result_data.text[0]['paragraphs']) == 2
    assert len(result_data.text[0]['paragraphs'][0]['sentences']) == 3
    assert result_data.text[1]['title'] == 'Begining data'
    assert 'Introduction' in result_data.text[2]['title']
    assert len(result_data.text[2]['paragraphs']) == 1
    assert len(result_data.text[2]['paragraphs'][0]['sentences']) == 16
    assert 'Defining MT Tools with Wodel-Test' in result_data.text[3]['title']
    assert 'Generated MT Tool' in result_data.text[6]['title']
    assert 'Conclusions and Future Work' in result_data.text[7]['title']
    assert 'Acknowledgments' in result_data.text[8]['title']
    assert 'References' in result_data.text[9]['title']


def test_ieee_pdf_by_doi(setup_downloader):
    DOI = '10.1109/ASE.2000.873655'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1109_ASE.2000.873655.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1109_ASE.2000.873655.pdf')

    assert result_data.publisher_link == 'https://ieeexplore.ieee.org/document/873655/'
    assert result_data.publish_year == '2000'

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == 'A DSL approach to improve productivity and safety in device drivers development'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 5


def test_science_direct_pdf_by_doi(setup_downloader):
    DOI = '10.1016/j.procs.2016.05.298'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1016_j.procs.2016.05.298.json'
    assert os.path.isfile(TEST_DIRECTORY + '/10.1016_j.procs.2016.05.298.pdf')

    assert result_data.publisher_link == 'https://linkinghub.elsevier.com/retrieve/pii/S1877050916306494'
    assert result_data.publish_year == '2016'

    assert result_data.read_status == 'OK - PDF READ'
    assert result_data.title == 'EMINENT: Embarrassingly Parallel Mutation Testing'
    assert result_data.doi == DOI
    assert len(result_data.authors) == 3
    assert len(result_data.text) == 7
    assert result_data.text[0]['title'] == 'Abstract'
    assert result_data.text[1]['title'] == 'Begining data'
    assert len(result_data.text[1]['paragraphs']) == 1
    assert len(result_data.text[1]['paragraphs'][0]['sentences']) == 5
    assert 'Introduction' in result_data.text[2]['title']
    assert len(result_data.text[2]['paragraphs']) == 1
    assert len(result_data.text[2]['paragraphs'][0]['sentences']) == 35
    assert 'State of the art' in result_data.text[3]['title']
    assert 'Experiments' in result_data.text[-3]['title']
    assert 'Conclusions and future work' in result_data.text[-2]['title']
    assert 'References' in result_data.text[-1]['title']

def test_willey_no_access_to_article(setup_downloader):
    DOI = '10.1002/0471028959.sof217'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1002_0471028959.sof217.json'
    assert not os.path.isfile(TEST_DIRECTORY + '/10.1002_0471028959.sof217.pdf')

    assert result_data.read_status == 'No access or PDF not available'

    assert result_data.journal_name == 'Encyclopedia of Software Engineering'
    assert result_data.publisher_link == 'http://doi.wiley.com/10.1002/0471028959.sof217'
    assert result_data.publish_year == '2002'
    assert result_data.authors == ["Mathur, Aditya P."]

    assert len(result_data.text) == 1
    assert result_data.text[0]["title"] == 'Abstract'
    assert len(result_data.text[0]["paragraphs"]) == 1
    assert len(result_data.text[0]["paragraphs"][0]["sentences"]) == 13


def test_willey_no_access_to_article_and_failed_to_read_ris(setup_downloader):
    DOI = '10.1002/stvr.4370010305'
    filename, result_data = setup_downloader.read_article(ArticleData(doi=DOI))

    assert filename == TEST_DIRECTORY + '/10.1002_stvr.4370010305.json'
    assert not os.path.isfile(TEST_DIRECTORY + '/10.1002_stvr.4370010305.pdf')

    assert result_data.read_status == 'No access or PDF not available'

    assert result_data.publisher_link == 'http://doi.wiley.com/10.1002/stvr.4370010305'
    assert result_data.publish_year == '1991'
    assert result_data.authors == ["Woodward, M R"]
    assert result_data.publication_date == '1991/10/01'
    assert result_data.journal_name == 'Software Testing, Verification and Reliability'

    assert len(result_data.text) == 1
    assert result_data.text[0]["title"] == 'Abstract'
    assert len(result_data.text[0]["paragraphs"]) == 1
    assert len(result_data.text[0]["paragraphs"][0]["sentences"]) == 3

