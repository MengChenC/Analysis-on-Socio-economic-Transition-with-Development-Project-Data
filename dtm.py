import numpy as np
import pandas as pd
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
from gensim.utils import effective_n_jobs
import nltk
from nltk.stem.snowball import SnowballStemmer

regex = r"[^a-z\s]"

def tokenize(text_series):
    '''
    Cleans, tokenizes + stems Pandas series of strings from
    the idb project dataset.
    
    Returns pandas series of lists of tokens
    '''
    # Clean text with regex
    clean = text_series.str.lower() \
                       .str.replace(regex,
                                    "",
                                    regex=True)

    # Anonymous tokenizer + stemmer functions
    stop1 = nltk.corpus.stopwords.words('english')
    stop2 = nltk.corpus.stopwords.words('spanish')
    stop3 = ['objective','main','general','project','sector','program','tc','support','supporting','energy','develop','developing',
             'development','efficient','country','countries','implement','implementing','implementation','technical','nation','improve',
             'improving','improvement','finance','financing','financial','technology','technological','system','institution','science',
             'government','strengthen','social','specific','region','area','transport','road','urban','electricity','service','increase',
             'increasing','increasement','invest','investment','generate','generating','generation','area','i','ii','iii','iv','v','vi']
    tokenize = lambda text: [i for i in nltk.word_tokenize(text) if ((i not in stop1) and (i not in stop2) and (i not in stop3))]
    stemmer = lambda tokens: [SnowballStemmer('english').stem(token) for token in tokens]

    # Tokenize and stem clean text
    tokens = clean.apply(tokenize)
    stemmed_tokens = tokens.apply(stemmer)
    
    return stemmed_tokens

def prepare_data(tokens):
    '''
    Prepares Pandas series of lists of tokens for use within a Gensim topic model
    
    Returns an id2word dictionary + bag of words corpus
    '''
    # Initialize Series of tokens as Gensim Dictionary for further processing
    dictionary = corpora.Dictionary([i for i in tokens])

    # Convert dictionary into bag of words format: list of (token_id, token_count) tuples
    bow_corpus = [dictionary.doc2bow(text) for text in tokens]
    
    return dictionary, bow_corpus

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=2):
    '''
    Computes Coherence values for LDA models with differing numbers of topics.
    
    Returns list of models along with their respective coherence values (pick
    models with the highest coherence)
    '''
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = models.ldamulticore.LdaMulticore(corpus=corpus,
                                                 id2word=dictionary,
                                                 num_topics=num_topics,
                                                 workers=effective_n_jobs(-1),
                                                 passes=20,
                                                 iterations=400)
        model_list.append(model)
        coherence_model = models.coherencemodel.CoherenceModel(model=model, 
                                                               corpus=corpus,
                                                               dictionary=dictionary,
                                                               coherence='u_mass')
        coherence_values.append(coherence_model.get_coherence())

    return model_list, coherence_values

def print_dtm(dtm, n_topics, n_time_slices):
    '''
    Prints out top words in each topic across time slices for visual comparison
    
    Input: Gensim LdaSeqModel, n_topics (int), n_time_slices (int)
    '''
    for topic in range(n_topics):
        for time in range(n_time_slices): 
            print("##### Topic {}, Time Slice {} #####".format(topic, time))    
            print(dtm.dtm_coherence(time)[topic][:10])    
        print("\n")

def dtm_coherence(list_dtms, bow_corpus, dictionary, n_time_slices):
    '''
    Computes UMass Coherence for each time slice in a list of DTMs
    
    Input: List of Gensim LdaSeqModels, number of time slices modeled (int)
    Returns: Dict of lists of coherence scores for each DTM
    '''
    coherence = {}
    for i, ldaseq in enumerate(list_dtms):
        coherence[i] = []
        for t in range(n_time_slices):
            topics_dtm = ldaseq.dtm_coherence(t)
            cm_DTM = CoherenceModel(topics=topics_dtm,
                                    corpus=bow_corpus,
                                    dictionary=dictionary,
                                    coherence='u_mass')

            coherence[i].append(cm_DTM.get_coherence())
            
        return coherence