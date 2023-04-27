import time
import pyspark
from graphframes import *
from pyspark.sql.functions import *
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import hash
from pyspark.sql.functions import lit
import os
import networkx as nx
# %pyspark --packages graphframes:graphframes:0.8.2-spark2.4-s_2.11 pyspark-shell
os.environ['JAVA_HOME'] = '/shared/centos7/oracle_java/jdk1.8.0_181'


N = 64 # Change this to change the number of partitions

def read_csv(spark, N):
    """Reads the Reddit Hyperlinks Body dataset and filters out only relationships with positive sentiment
    Input: spark, N: number of partitions
    Output: df: Spark DataFrame"""
    df = spark.read.csv("soc-redditHyperlinks-body.tsv", sep="\t", header=True, inferSchema=True).repartition(N, "SOURCE_SUBREDDIT")
    df = df.filter("LINK_SENTIMENT == 1")
    df = df.withColumn("weightage", lit(1.0))
    return df

def get_vertices(df):
    """Gets all the node ids and names and returns it as a Spark DataFrame"""
    vertices = df.selectExpr("SOURCE_SUBREDDIT as id", "SOURCE_SUBREDDIT as name").union(df.selectExpr("TARGET_SUBREDDIT as id", "TARGET_SUBREDDIT as name")).distinct()
    return vertices

# function to get edges from dataframe
def get_edges(df):
    """ function to get edges with weights > 1 from spark dataframe returns nodes"""
    edges = df.selectExpr("SOURCE_SUBREDDIT as src", "TARGET_SUBREDDIT as dst", "weightage as weightage")#.distinct()
    edges = edges.groupBy("src", "dst").agg(sum("weightage").alias("weights")).sort("weights", ascending=False).filter("weights > 1")
    #edges.show(n=10)
    return edges

# create graph frame from nodes edges
def create_graph(nodes, edges, N):
    g = GraphFrame(nodes.repartition(N, hash(nodes["id"]) % N), edges)
    return g

# generate connected components from graph frame
def connected_components(sc, g, filename):
    """ takes in spark graph frame, generates connected components
        saves as pickle object"""
    start = time.time()
    sc.setCheckpointDir("./checkpoints")
    cc = g.connectedComponents()
    end = time.time()
    diff = end-start
    #print(diff)
    cc.rdd.saveAsPickleFile(filename)
    cc.show()
    return diff
    

def pickle_to_dataframe(sc, spark, filename):
    """ reads in pickle object and converts to spark dataframe"""
    pickleRdd = sc.pickleFile(filename).collect()
    return spark.createDataFrame(pickleRdd)

def __main__():
    spark = SparkSession.builder.config("spark.memory.offHeap.enabled","true")\
                            .config("spark.memory.offHeap.size","100g")\
                            .config("spark.executor.memory", "100g")\
                            .config("spark.driver.memory", "100g")\
                            .appName("Reddit Community Detection").getOrCreate()
    sc = SparkContext.getOrCreate()
    df = read_csv(spark, N)
    edges = get_edges(df)
    vertices = get_vertices(df)
    edges.rdd.saveAsPickleFile('all_edges.pkl')
    print("Edges count = ", edges.count())
    df_edges = edges.toPandas()
    G = nx.from_pandas_edgelist(df_edges, source='src', target='dst', edge_attr=None, create_using=nx.DiGraph(), edge_key=None)
    nx.write_gexf(G, "reddit_links.gexf")
    
    gf = create_graph(vertices, edges, N)
    time_for_cc = connected_components(sc, gf, 'connected_components.pkl')
    print("Connected Components took {} seconds to execute for N={}".format(time_for_cc, N))
    df = pickle_to_dataframe(sc, spark, 'connected_components.pkl')
    df.show()