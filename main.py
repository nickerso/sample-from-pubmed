import sys

import entrezpy.esearch.esearcher
import entrezpy.log.logger
import random


# entrezpy.log.logger.set_level('DEBUG')


def select_sample(uids, size):
    return random.sample(uids, size)


def execute_search(toolname, email, query_string):
    es = entrezpy.esearch.esearcher.Esearcher(toolname, email)
    analyzer = es.inquire({
        'db': 'pubmed',
        'term': query_string,
        'rettype': 'uilist'
    })
    count = analyzer.result.count
    print(f'Number of results: {count}')
    uids = analyzer.result.uids
    if count != len(uids):
        print(f'Should have {count} UIDs but there are {len(uids)}.')
        exit(-1)
    return uids


if __name__ == '__main__':

    toolname = 'esearcher-sampler'
    email = sys.argv[1]

    query = '("last 10 years"[dp] AND english[la] NOT review[pt])' \
            ' AND ' \
            '("Computer Simulation"[MH] OR "Computer Simulation"[TIAB] OR "Mathematical Computing "[MH] OR "Mathematical Computing "[TIAB] OR "Systems Biology"[MH] OR "Systems Biology"[TIAB] OR "Models, Theoretical"[MH] OR "Theoretical Model"[TIAB] OR "Models, Biological"[MH] OR "Biological Model"[TIAB] OR "Computational Model"[TIAB])' \
            ' AND ' \
            'Cells[MH]'

    # query = '("Computer Simulation"[MH] OR "Computer Simulation"[TIAB] OR "Mathematical Computing"[MH] OR "Mathematical Computing"[TIAB] OR "Systems Biology"[MH] OR "Systems Biology"[TIAB] OR "Models, Theoretical"[MH] OR "Theoretical Model"[TIAB] OR "Models, Biological"[MH] OR "Biological Model"[TIAB] OR "Computational Model"[TIAB])'

    # query = '"Computer Simulation"[MH]'
    # query = '"Computer Simulation"[MH] OR "Computer Simulation"[TIAB]'

    # query = 'nickerson dp[Author - First]'

    print(query)
    uids = execute_search(toolname, email, query)
    sample_uids = select_sample(uids, 10)
    print(f'Selected random sample of Pubmed IDs to check: {sample_uids}')
    # fetch_pubmed(sample_uids)