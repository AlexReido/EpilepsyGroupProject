# Group Epilepsy sugery progect

This project aims to aid in epilepsy surgery planning specifically in locating potential resection which cause the maximum reduction in network ictogenicity.

The backend of this project is broken down into three microservices:
* Create model
* Perform search
* Show results

This allows modularity and enables us to develop the project in parallel. The modularity makes it easy to adapt and more maintainable. The services will be completely decoupled so if an improved search service is developed it can immediately replace the current search without changing the other services.

I will now cover the API structure implemented by the backend
### Create model /model/
This service has two distinct methods to generate a network model; Generating a model from an artificial network and generating a model from ieeg data. 

Get /model/artificial/?constructionTechnique=Random&n=20

Potentialy another service here: 
Get /model/ieeg/?parameters

### Perform search /search/
This service performs the search on the network model and returns the results in the form 
of a list of different sets of nodes with the ictogenicity reduction value.

Pass the network model
Get /search/?NodestobeExcluded=ACG&MaximumNumberOfNodes=20&AlgorithmUsed=NSGA

### Show results /results/
This service returns the results in the format preferred

Get /results/table/?numberofresults=10

Get /results/report/

Get /results/diagram/