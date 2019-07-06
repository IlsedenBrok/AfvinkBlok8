from Bio import Entrez
import matplotlib.pyplot as plt


def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax=100,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def visualise(first_yearlist, second_yearlist):
    allyears = first_yearlist + second_yearlist
    unique_years = list(set(allyears))
    unique_years = sorted(unique_years)

    first_counter = []
    second_counter = []

    for year in unique_years:
        first_counter.append(first_yearlist.count(year))

    for year in unique_years:
        second_counter.append(second_yearlist.count(year))

    x_axis = unique_years
    y_axis_1 = first_counter
    y_axis_2 = second_counter

    plt.bar(x_axis, y_axis_1, color='b', width=0.5)
    plt.bar(x_axis, y_axis_2, color='g', width=0.5)
    plt.show(block=True)


if __name__ == '__main__':
    results = search('bitter gourd')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    first_yearlist = []

    for i, paper in enumerate(papers['PubmedArticle']):
        try:
            first_yearlist.append(paper['MedlineCitation']['DateCompleted']['Year'])
        except KeyError:
            pass

    results = search('kinase')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    second_yearlist = []

    for i, paper in enumerate(papers['PubmedArticle']):
        try:
            second_yearlist.append(paper['MedlineCitation']['DateCompleted']['Year'])
        except KeyError:
            pass

    visualise(first_yearlist, second_yearlist)