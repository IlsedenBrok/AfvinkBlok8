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
    try:
        for c in compound_list:
            compound = c
            for d in disease_list:
                disease = d
                for f in food_list:
                    food = f
                    query = '\"' + compound + '\"' + " AND " + '\"' + disease + '\"' + " AND " + '\"' + food + '\"'
                    print("Searching for ", query)
                    results = search(query)
                    id_list = results['IdList']
                    papers = fetch_details(id_list)
                    
                    return papers
    except RuntimeError:
        print(query, " heeft 0 resultaten")



def save_details():
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
    return abstracts, names


def get_names():
    i = 0
    print("lengte names   ", len(names))
    print("names   ", names)
    y = 0
    z = 0
    line = str(names[i])
    first_name = re.findall("'Initials': '[a-zA-Z]+'", line)
    last_name = re.findall("LastName': '[a-zA-Z]+'", line)
    if first_name:
        result = str(first_name).split(',')
        while z < len(result):
            print(result[z])
            z += 1
    if last_name:
        result = str(last_name).split(',')
        while y < len(result):
            print(result[y])
            y += 1
        return first_name, last_name


if __name__ == '__main__':
    disease_list, compound_list, food_list = read_files()
    papers = get_info()
    abstracts, names = save_details()
    first, last = get_names()
