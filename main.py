import sys
import random
from string import Template
from xml.dom import minidom
from xml.etree import ElementTree
from easy_entrez import EntrezAPI


def select_sample(uids, size):
    return random.sample(uids, size)


def xml_to_string(element):
    return (
        minidom.parseString(ElementTree.tostring(element))
        .toprettyxml(indent=' ' * 4)
    )


if __name__ == '__main__':

    toolname = 'py-search-sampler'
    email = sys.argv[1]

    entrez_api = EntrezAPI(
        toolname,
        email,
        return_type='json'
    )

    query_template = Template(
        '(english[la] NOT review[pt])'
        ' AND '
        '("Computer Simulation"[MH] OR "Computer Simulation"[TIAB] OR "Mathematical Computing "[MH] OR "Mathematical Computing "[TIAB] OR "Systems Biology"[MH] OR "Systems Biology"[TIAB] OR "Models, Theoretical"[MH] OR "Theoretical Model"[TIAB] OR "Models, Biological"[MH] OR "Biological Model"[TIAB] OR "Computational Model"[TIAB])'
        ' AND '
        'Cells[MH] AND (("${year}"[Date - Publication] : "${year}"[Date - Publication]))'
    )

    years = [2010, 2021]
    uids = []
    for year in years:
        print(f'Searching for publications in year: {year}')
        term = query_template.substitute(year=year)
        results = entrez_api.search(database='pubmed', term=term, max_results=100000)
        r = results.data['esearchresult']
        all_uids = r['idlist']
        print(f'Found {len(all_uids)} articles')
        uids.extend(select_sample(all_uids, 5))

    fetch_data = entrez_api.fetch(uids, max_results=10000)
    articles = fetch_data.data
    print(xml_to_string(articles))