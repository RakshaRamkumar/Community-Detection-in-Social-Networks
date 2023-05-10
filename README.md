# Community-Detection-in-Social-Networks

This project was a course capstone project for EECE 5645: Parallel Processing for Data Analytics. The team that worked on this project is Kedar Ghule, Raksha Ramkumar, Jason Serpe and Dana Diaconu.

## Problem Statement

Community detection plays an important role in network analysis as it allows researchers and data scientists to get a better understanding of the structure of the network. It can also reveal valuable details about the features of the strongly connected nodes in communities and their similarity. Social networks such as Facebook, Twitter, and Reddit have millions of users and billions of connections between them. Detecting communities within these networks, i.e., groups of similar nodes, can help understand the underlying structure of the network and identify patterns in user behavior. It is also an interesting task as we do not know any ground truths since this is an unsupervised learning problem. There are several approaches to detect communities within social networks to gain insights into the network's structure and user behavior. One of the biggest challenges of community detection algorithms is parsing huge graph data which leads to long run times and requires a significant number of computational resources.

Given the challenges for this task, we aim to show the benefits of using big data processing tools like Apache Spark to perform community detection, specifically community detection in social networks.

## Dataset

We use the Reddit Hyperlink dataset from the Stanford Network Analysis Project (SNAP) which can be found [here]{https://snap.stanford.edu/data/soc-RedditHyperlinks.html}. This dataset consists of Jan 2014 to April 2017. We used the Reddit Hyperlinks body.tsv file from this dataset that has 35,776 vertices (subreddits) and 286,561 edges (number of hyperlinks).

## Data Preprocessing
