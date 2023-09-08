# Key Learnings

- ## Importance of Data Exploration
  Exploring the Subreddit dataset was crucial as it helped us understand the different features captured in the dataset. The three main feature points from this dataset that we used were 'Source subreddit', 'Destination subreddit' and 'Sentiment'. With this knowledge we were able to decide the data preparation and data pre-processing steps required for our project. We translated this data into a graph format, where each node was a sub-reddit and the edges were the hyperlinks between these sub-reddits weighted with the number of posts.

  With this definition, we filtered out the negative sentiment and weak links and applied Connected Components as our next pre-processing step. This helped in getting a clearer definition of the existence of a 'community'. We applied the community-detection algorithms on the largest connected component in our graph.

- ## Tools Used
  With the data ready to be processed and the objective clear and set, the next step is to figure out which amoing the various available tools would be best-suited for our task and data. After performing initial experimentation and literature survey, we decided to represent our graph using the Spark Dataframe. With this representation, we were able to perform Graph parallelism when we partition over the vertices and can communicate over the edges.

  We also used Gephi, a visualization tool that helped a lot in making sense of the communities being detected and the links between each node in a very efficient manner. The entire programming was done in Python because of its ease-to-use property and our proficiency in the language. We also used PySpark for data parallelism and utilized our universitie's cluster of CPUs to perform parallelism.
  
- ## Community Detection Algorithms
  Three community detection algorithms namely Label Propagation, Power Iteration Clustering and Girvan-Newman were implemented and compared. These 3 algorithms were chosen because they are different in their underlying implementation of grouping nodes into communities and we wanted to see how each of them perform in terms of accuracy and parallelism usage.

  We understood the working of these algorithms and the parameters that control them. By implementing them, we realized the use-case for each of these methods and the challenges involved. 
- ## Evaluation Metrics
One of the most important aspects of implementing a Machine Learning algorithm is its evaluation on unseen test dataset. Since community detection is an unsupervised clustering technique, there are no 'ground truths' to measure the prediction against. We employed a metric called 'modularity' to measure how densely the formed communities are.

- ## Parallelism in Action
By partitioning the RDDs efficiently and using multiple CPU cores for the implementation of all the three algorithms, we were able to observe the speed-up in execution. It is important to note that the core-partition ratio is also important and must be chosen wisely to get the highest speed-up. We understood that just increasing the number of cores/partitions blindly does not always guarantee a decrease in the execution time: the inherent behavior of how the algorithm is implemented in the library used also factors in.
