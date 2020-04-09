import attr
import json

@attr.s
class ArticleData:
    doi = attr.ib(default=str())
    title = attr.ib(default=str())
    text = attr.ib(default=str())
    journal_name = attr.ib(default=str())
    journal_info = attr.ib(default=str())
    authors = attr.ib(default=list())
    publisher = attr.ib(default=str())
    issn = attr.ib(default=str())
    scopus_link = attr.ib(default=str())
    publisher_link = attr.ib(default=str())
    read_status = attr.ib(default=str())
    publish_year = attr.ib(default=str())

    def to_dict(self):
        return attr.asdict(self)

    def merge(self, other):
        if not self.doi:
            self.doi = other.doi
        if not self.title:
            self.title = other.title
        if not self.journal_name:
            self.journal_name = other.journal_name
        if not self.journal_info:
            self.journal_info = other.journal_info
        if not self.authors:
            self.authors = other.authors
        if not self.publisher:
            self.publisher = other.publisher
        if not self.issn:
            self.issn = other.issn
        if not self.scopus_link:
            self.scopus_link = other.scopus_link
        if not self.publish_year:
            self.publish_year = other.publish_year

        if not self.publisher_link:
            self.publisher_link = other.publisher_link

        if not self.read_status:
            self.read_status = other.read_status

        if not self.text:
            self.text = other.text
        elif other.text:
            for section in other.text:
                if not [x for x in self.text if x['title'] == section['title']]:
                    self.text.append(section)


