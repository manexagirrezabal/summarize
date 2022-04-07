from itertools import combinations
from operator import itemgetter

from distance import jaccard
from networkx import Graph, pagerank

from .language import LanguageProcessor

from scipy.spatial.distance import cosine

from sentence_transformers import SentenceTransformer
#sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v2')
#embeddings = model.encode(sentences)
#print(embeddings)

__all__ = ['summarize']


def summarize(text, sentence_count=5, language='english'):
    processor = LanguageProcessor(language)

    sentence_list = processor.split_sentences(text)
#    wordset_list = map(processor.extract_significant_words, sentence_list)
#    stemsets = [
#        {processor.stem(word) for word in wordset}
#        for wordset in wordset_list
#    ]

    graph = Graph()
    pairs = combinations(enumerate(sentence_list), 2)
    for (index_a, sentence_a), (index_b, sentence_b) in pairs:
        #print (index_a,index_b)
        #print (stems_a, stems_b)
        #print()
        if sentence_a and sentence_b:
            representations = model.encode([sentence_a,sentence_b])
            similarity = cosine(representations[0],representations[1])
#            similarity = 1 - jaccard(sentence_a, sentence_b)
            
            if similarity > 0:
                #print ("Save this!",similarity)
                graph.add_edge(index_a, index_b, weight=similarity)

    print (pagerank(graph))
    ranked_sentence_indexes = list(pagerank(graph).items())
    if ranked_sentence_indexes:
        sentences_by_rank = sorted(
            ranked_sentence_indexes, key=itemgetter(1), reverse=True)
        best_sentences = map(itemgetter(0), sentences_by_rank[:sentence_count])
        best_sentences_in_order = sorted(best_sentences)
    else:
        best_sentences_in_order = range(min(sentence_count, len(sentence_list)))

    return ' '.join(sentence_list[index] for index in best_sentences_in_order)
    