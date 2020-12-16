# knowledgesharing
this repository contains the replication package of the Knowledge sharing paper 

The python_sLDA script uses one of the training datasets (e.g., with full labels, short labels or only top-labels) produced in the first pipeline.
It takes an <unseen> text to predict its label(s), using the training from the larger datasets

usage: ./python3 ./python_sLDA <name of unseen text containing a research paper>
