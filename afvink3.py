from Bio import Entrez
import re


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


def read_files():
    disease_list = []
    compound_list = []
    food_list = []
    count = 0
    file_paths = ["data/diseases.txt", "data/compounds.txt", "data/food.txt"]
    for path in file_paths:
        count += 1
        for line in open(path):
            if line != "" and count == 1:
                disease_list.append(line.strip())
            elif line != "" and count == 2:
                compound_list.append(line.strip())
            elif line != "" and count == 3:
                food_list.append(line.strip())
    return disease_list, compound_list, food_list


def get_info():
    abstract_list = []
    number_list = []
    query_list = []
    search_count = 0
    for c in compound_list:
            compound = c
            for d in disease_list:
                disease = d
                for f in food_list:
                    food = f
                    try:
                        query = '\"' + compound + '\"' + " AND " + '\"' + disease + '\"' + " AND " + '\"' + food + '\"'
                        query_list.append(query)
                        results = search(query)
                        id_list = results['IdList']
                        papers = fetch_details(id_list)

                        counter = 0
                        abstracts = []
                        names = []

                        for i, paper in enumerate(papers['PubmedArticle']):
                            counter += 1
                            try:
                                abstracts.append(paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
                                names.append(paper['MedlineCitation']['Article']['AuthorList'])
                            except KeyError:
                                pass

                        abstract_list.append(abstracts)
                        number_list.append(len(abstracts))

                        search_count += 1

                    except RuntimeError:
                        pass

    maximum = max(number_list)
    place = number_list.index(maximum)
    abstract_highest_count = abstract_list[place]
    print("The abstracts of the most frequent combination: ")
    print(query_list[place+1], "\n")
    teller = 1

    i = 0
    y = 0
    z = 0
    line = str(names[i])
    first_name = re.findall("'Initials': '[a-zA-Z]+'", line)
    last_name = re.findall("LastName': '[a-zA-Z]+'", line)
    if first_name:
        result = str(first_name).split(',')
        while z < len(result):
            print("z", result[z])
            z += 1
    if last_name:
        result = str(last_name).split(',')
        while y < len(result):
            print("y", result[y])
            y += 1

    for abstract in abstract_highest_count:
        print(teller, ": ", abstract[0])
        # print(initials[teller])
        # print(last_names[teller])
        teller += 1


if __name__ == '__main__':
    disease_list, compound_list, food_list = read_files()
    get_info()
