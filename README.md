# knowledgesharing
this repository contains the replication package of the Knowledge sharing paper 

The RepPackages-pop7.sh script:
    * it uses the PoP7 CLI executable that should be downloaded from here:
    https://harzing.com/resources/publish-or-perish/command-line

    * it produces a list of page locations within a paper that might contain the link to the replication package
    
    * for each page location, the script extract the three lines "preceding" the <replication package> stopwords and the three lines "after" that
