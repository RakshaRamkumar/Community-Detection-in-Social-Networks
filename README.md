# Parallelized Community Detection in Social Networks

This project was a course capstone project for EECE 5645: Parallel Processing for Data Analytics. The team that worked on this project is Kedar Ghule, Raksha Ramkumar, Jason Serpe and Dana Diaconu.

## Problem Statement

Community detection plays an important role in network analysis as it allows researchers and data scientists to get a better understanding of the structure of the network. It can also reveal valuable details about the features of the strongly connected nodes in communities and their similarity. Social networks such as Facebook, Twitter, and Reddit have millions of users and billions of connections between them. Detecting communities within these networks, i.e., groups of similar nodes, can help understand the underlying structure of the network and identify patterns in user behavior. It is also an interesting task as we do not know any ground truths since this is an unsupervised learning problem. There are several approaches to detect communities within social networks to gain insights into the network's structure and user behavior. One of the biggest challenges of community detection algorithms is parsing huge graph data which leads to long run times and requires a significant number of computational resources.

Given the challenges for this task, we aim to show the benefits of using big data processing tools like Apache Spark to perform community detection, specifically community detection in social networks.

## Tools
Python, Apache Spark through PySpark, GraphFrames, Gephi.

## Dataset

We use the Reddit Hyperlink dataset from the Stanford Network Analysis Project (SNAP) which can be found [here](https://snap.stanford.edu/data/soc-RedditHyperlinks.html). This dataset consists of Jan 2014 to April 2017. We used the Reddit Hyperlinks body.tsv file from this dataset that has 35,776 vertices (subreddits) and 286,561 edges (number of hyperlinks).

## Data Preprocessing
The Reddit Hyperlink dataset was converted into a directed graph structure. Spark Dataframes were utilized for the data preprocessing steps. The following preprocessing steps were performed:
1. **Filtering out edges with negative sentiments:** All negative edges with negative sentiment (-1) value were filtered out, as negative sentiment is not indicative of a ‘community’ in the sense that the nodes are similar.
2. **Filter out weak edges:** Next, we aggregated all posts that contained the same source and destination subreddits, such that our data was of the form (Source, Destination, Number of Posts). We then found the set of distinct subreddits, either source or destination, which became our list of nodes/vertices. Each data point became an edge between these nodes, with the number of posts equivalent to the weight of the edge. We then filtered out any edges that were of weight 1. Essentially, this removed weak links between subreddits, and would also help to filter out subreddits that were very small and had generally few associated posts. The preprocessed graph dataset visualized using Gephi below: 

![1](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/93416e23-bfbf-4efd-8b23-d5adaacefc6c)

3. **Connected Components:** A graph dataset need not always be connected. That is, there may not exist a path from every node to every other node in the graph dataset (subgraphs in it may not connected to each other at all). Hence, we need to find the total number of nodes in each subgraph to see if it is big enough for further graph analysis. Smaller subgraphs or lone nodes will not contribute to the community detection task and should be eliminated. Connected Components is often used as one of the early steps of graph preprocessing. The GraphFrames library provides a parallelized implementation to find connected components on a GraphFrames object using the connectedComponents() function. It computes the connected component membership of each vertex and returns a graph with each vertex assigned a component ID. For this task, we take the largest connected component (connected component with most vertices) for further analysis. Below figure shows a visualization using Gephi of the largest connected component that we investigate for community detection. It contains roughly 11,000 nodes and 31,000 edges.

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/c6a08118-0a0e-4a7d-903e-f74037fcf276)

## Community Detection

Using the graph of the largest component, we performed community detection on it. We used three algorithms – Label Propagation, Power Iteration Clustering (a version of Graph Spectral Clustering), and the Girvan-Newman Algorithm.

#### Label Propagation
Label propagation is a graph algorithm used for community detection. It works by propagating labels like a “message” randomly throughout the network. It is a non-deterministic algorithm that starts with a subset of the data having labels depicting the clusters and eventually assigns labels to each node of the graph. The main intuition is that a label can quickly become dominant in a densely connected group of nodes but will have trouble crossing a sparsely connected region. Label Propagation can be parallelized in Spark using the GraphFrames library. GraphFrames offers an in-built implementation of the Label Propagation algorithm through the labelPropagation() function. The only hyperparameter it takes is the number of iterations. It should also be noted that for label propagation, the number of communities to be found is not specified beforehand.

#### Power Iteration Clustering
Power Iteration Clustering is a correlation/distance-based clustering algorithm which is built on spectral clustering. It finds the low-dimensional embedding of a dataset using the truncated power iteration method. Using this embedding, the clusters in the dataset are found. The correlation between the nodes/vertices of the graph is defined by the affinity matrix. In our project, we are defining the affinity matrix using the weights of the edges. In general, an affinity matrix is a symmetric matrix that defines if there is a connection between two given nodes. Power Iteration Clustering is parallelized using Spark’s MLib library. For Power Iteration Clustering, we need to specify the value K which is the number of communities. For this, we performed hyperparameter tuning.

#### Girvan-Newman Algorithm
The Girvan-Newman method is an iterative method which computes the betweenness centrality for all edges in the graph, removes the edges with the highest betweenness centrality and then does the same computations all over again. The algorithm stops when there are no more edges or the edges inside communities have the same betweenness. The betweenness centrality of an edge is given by the number of shortest paths between vertices which pass through that edge. There are no parallel implementations for Girvan-Newman in libraries such as PySpark or GraphFrames. We  tried to build upon an open source code howver were not able to scale it due to the worst case time complexity of the algorithm.

## Validation Analysis
Community detection is an unsupervised learning task. For a problem like this, there are no ground truths available in the dataset. The validation analysis was performed on the training dataset since we cannot validate on a ‘test dataset’ for such unsupervised learning tasks. To evaluate our solution approaches, we make use of the modularity metric. Modularity is a popular metric used to evaluate community detection algorithms. A high modularity score means that there are dense connections between the nodes within the communities. Conversely, a low modularity score implies that there are sparse connections between nodes within the communities. The value of modularity ranges from -1 to +1.

Below is a table that summarizes the results we got for Label Propagation and the Power Iteration Clustering algorithm.
![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/c3907651-0246-496d-b8b0-7e56feda7fe1)

Below is a graph showing our communities for the label propagation algorithm:
![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/e027d820-5cf1-4d81-8df5-a1dc6501e2f7)

Below is a graph showing our communities for the power iteration clustering algorithm:
![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/0b573177-9c96-42cd-afc3-a16973c38a28)

In both graphs, nodes are colored according to their community. The circles and labels show some specific communities that were detected. Both algorithms were able to detect many distinct communities, however, there are some noticeable issues. For instance, neither algorithm was able to detect communities within the center of mass of the graph. This represents very large subreddits (r/pics, r/AMA, r/askreddit, etc) which generally have links to many other subreddits and each other, and thus essentially become one very large community. To verify that these communities are correct, here are two zoomed in images of specific communities, with the nodes labeled with the name of the subreddit:
![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/c0cdfdae-7a13-4904-a5a6-12e67acebff3)

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/e3b78e2f-d458-49f1-8526-2bb0ddad7b40)

## Performance Analysis
Finally, to complete our objective of the project, we did a performance analysis to observe the speed-up with parallelism. This was only performed on Label Propagation and Power Iteration Clustering only as Girvan-Newman was slow because of high time complexity. We also did a performance analysis on the Connected Components method. Below are charts showing our results for our performance analysis on the connected components and label propagation algorithm:
![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/3449913e-7ad9-4be8-a61f-a87a4a19290a)  

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/a7544bbc-3b67-4cc3-a2b7-3d8b29deb299)

For power iteration clustering, we saw that it was the fastest. On a single core, the PIC takes around 62 seconds to give out the resulting clusters. As seen from the graph below, with increasing number of cores, the execution time of the algorithm decreases:

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/f6b26ee9-2a99-4db2-b0c7-6455cd1ebd21)

It is important to note that the core-partition ratio is also important and must be chosen wisely to get the highest speed-up.
Keeping constant partitioning (N=2), the following graph shows the trend of execution time with varying number of cores:

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/b85717e0-bd51-4b6b-8134-518510bcd498)

In this case, there is generally a speedup with a constant number of partitions and an increasing number of cores, as the algorithm was able to take advantage of the hardware level parallelism and assign multiple workers to the same partition.
With 64 cores, increasing the number of partitions decreases the speed, only up to a certain point after which increasing the partitioning further leads to an increase in the speed. As the number of partitions increases, the associated costs (generating partitions, communication) also increase, and outweigh the benefit of increased data parallelism.

![image](https://github.com/kedarghule/Community-Detection-in-Social-Networks/assets/41315903/2f1748c6-40bb-4be6-84ec-3d5b6a2ce865)





