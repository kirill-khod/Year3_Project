
# pip install bertopic

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import nltk
import gensim
import gensim.corpora as corpora
import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from gensim.models.coherencemodel import CoherenceModel

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')


colnames=['name', 'description', 'price', 'link'] 
docs1 = pd.read_csv('appliance.csv',names=colnames, header=None)
docs2 = pd.read_csv('laptops.csv',names=colnames, header=None)
docs3 = pd.read_csv('phones.csv',names=colnames, header=None)
docs4 = pd.read_csv('sneakers.csv',names=colnames, header=None, sep=';')
docs5 = pd.read_csv('toys.csv',names=colnames, header=None, sep=';')
docs6 = pd.read_csv('makiyazh.csv',names=colnames, header=None, sep=';')
docs7 = pd.read_csv('reduced_data.csv',names=colnames, header=None)



docs = docs1.append(docs2, ignore_index=True)
docs = docs.append(docs3, ignore_index=True)
docs = docs.append(docs3, ignore_index=True)
docs = docs.append(docs4, ignore_index=True)
docs = docs.append(docs5, ignore_index=True)
docs = docs.append(docs6, ignore_index=True)
docs = docs.append(docs7, ignore_index=True)



# docs['comb'] = docs['name'] + " " + docs['description']
docs['comb'] = docs['name']

docs.head()

filtered_text = []
lemmatizer = WordNetLemmatizer()

for w in docs['comb']:
  filtered_text.append(lemmatizer.lemmatize(w))
print(filtered_text[:1])
docs['filtered'] = filtered_text



embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
umap_model = UMAP(n_neighbors=20, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = HDBSCAN(min_cluster_size=40,metric='euclidean', cluster_selection_method='eom', prediction_data=True)
vectorizer_model = CountVectorizer()
ctfidf_model = ClassTfidfTransformer()

docs.head()

topic_model= BERTopic(language = "multilingual", top_n_words = 10, n_gram_range = (1,2), calculate_probabilities=True, verbose=True, 
  embedding_model=embedding_model,    
  umap_model=umap_model,              
  hdbscan_model=hdbscan_model,        
  vectorizer_model=vectorizer_model,  
  ctfidf_model=ctfidf_model,          
  nr_topics = "auto"
          )
topics, probs = topic_model.fit_transform(docs['filtered'])

# topic_model.update_topics(list(docs['filtered']), n_gram_range=(1, 2), top_n_words = 10)

hierarchical_topics = topic_model.hierarchical_topics(docs['filtered'])

hierarchical_topics

topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)


tree = topic_model.get_topic_tree(hierarchical_topics)
print(tree)

representative_docs = topic_model.get_representative_docs()
representative_docs

docs['Topic'] = topics

docs.head()

freq = topic_model.get_topic_info()
freq

topic_model.get_topic(0)

topic_model.visualize_hierarchy(top_n_topics=50)

topic_model.visualize_heatmap(n_clusters=20, width=1000, height=1000)

# from sklearn.metrics.pairwise import cosine_similarity
# sim_matrix = cosine_similarity(topic_model.c_tf_idf_)
# df = pd.DataFrame(sim_matrix, columns=topic_model.topic_labels_.values(), index=topic_model.topic_labels_.values())
# df
# # distance_matrix = cosine_similarity(np.array(topic_model.topic_embeddings)[1:, :])

topic_model.visualize_barchart(top_n_topics=len(freq))

topic_model.visualize_topics()

topic_model.save("my_model")

test_docs = "adidas кроссовки"
predicted_topics, predicted_probs = topic_model.transform(test_docs)
print(f'Predicted topic is {predicted_topics}, and the probability is {np.round(predicted_probs,2)}')

new_review ="adidas кроссовки"
similar_topics, similarity = topic_model.find_topics(new_review, top_n=5)
print(f'The most similar child topic is {similar_topics}, and the similarities is {np.round(similarity,2)}')