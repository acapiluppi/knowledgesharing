# knowledgesharing
this repository contains the replication package of the Knowledge sharing paper 

====== UNSUPERVISED ML script
The python_TOPICS_2.py script works in an unsupervised fashion: given a text file, it extracts the concepts and topics using a LDA approach

usage: ./python3 ./python_TOPICS_2.py <name of text file containing a research paper>

====== SUPERVISED ML script
The python_sLDA script uses one of the training datasets (e.g., with full labels, short labels or only top-labels) produced in the first pipeline.
It takes an <unseen> text to predict its label(s), using the training from the larger datasets. Based on Bag-of-words, LDA and lemmatisation

usage: ./python3 ./python_sLDA <name of unseen text file containing a research paper>
