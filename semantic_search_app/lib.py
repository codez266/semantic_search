from sentence_transformers import SentenceTransformer, util
import torch
import re

def get_corpus():
    corpus = None
    with open("semantic_search_app/data/las_23.bib") as fin:
        corpus = fin.read()

    # Define a regular expression pattern to extract inproceeding blocks
    inproceeding_pattern = re.compile(r'@inproceedings{(.*?)\}\n\}', re.DOTALL|re.MULTILINE)

    # Find all inproceeding blocks in the references text
    inproceeding_blocks = inproceeding_pattern.findall(corpus)

    # Define a regular expression pattern to extract title and abstract from each inproceeding block
    title_abstract_pattern = re.compile(r'title = {(.*?)},\n.*?url = {(.*?)},\n.*?abstract = {(.*?)}', re.DOTALL)

    # Extracted titles and abstracts from each inproceeding block
    paper_data = []
    for block in inproceeding_blocks:
        match = title_abstract_pattern.search(block)
        if match:
            title, url, abstract = match.groups()
            paper_data.append((title, url, abstract))
            # print("Title:", title)
            # print("Abstract:", abstract)
            # print("\n" + "="*50 + "\n")
    return paper_data

def get_search_results(model, data, corpus, query, logger):
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    top_k = min(5, len(data))
    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    results = []
    logger.info("Query: {}".format(query))
    for score, idx in zip(top_results[0], top_results[1]):
        results.append((data[idx]))
    return results
