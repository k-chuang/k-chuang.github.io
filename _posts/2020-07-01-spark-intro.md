---
title: Spark Introduction
# date: 2020-06-02 15:44:18.000000000 -07:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- General
- Distributed Computing
- Apache Spark
- Kubernetes
- Google Dataproc
- Hadoop
tags:
- Apache Spark
- PySpark
- YARN
- HDFS
- Google Dataproc
- Hadoop
# meta:
  # _wpcom_is_markdown: '1'
  # _publicize_job_id: '30813365882'
  # timeline_notification: '1557873861'
permalink: "/2020/07/01/spark-introduction/"
---

# Apache Spark Introduction
Apache Spark is a fast and general-purpose cluster computing system. It provides high-level APIs in Java, Scala, Python and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including **Spark SQL** for SQL and structured data processing, **MLlib** for machine learning, **GraphX** for graph processing, and **Spark Streaming**.

Spark is a great tool to have as a data engineer/ data scientist / machine learning engineer, because it can handle large amounts of data (yuck Big Data) and is very fast at processing data due distributed computing (where tasks are separated out to multiple computers) and in-memory data structures.

## Distributed Computing Terms
- **Partitioned Data**
  - Because the processing tasks will be divided across multiple nodes, the data also has to be able to be divided across multiple nodes. Partitioned data refers to data that has been optimized to be able to be processed on multiple nodes. Spark's RDDs are partitioned.
    - Dataframes can be partitioned on `user_id`, which is similar to indexing in relational databases. Example is listed below. N = Node and U = user.
      - N1: U1, U4, U6
      - N2: U2, U3, U7
- **Fault Tolerance**
  - Refers to the ability of a system to continue working properly in the event of a failure (e.g. node failure or communication break between nodes). Spark has RDDs (i.e. Resilient Distributed Datasets), which are fault-tolerant, because they are essentially DAGs (i.e. Directed Acyclic Graphs) of computation that can be recomputed when there's a failure.
- **Lazy Evaluation**
  - Lazy evaluation has to do with how code is compiled and executed. Lazy evaluation is the opposite of strict / eager / greedy evaluation, which continually & eagerly processes code line by line (how typical code runs). An example of lazy evaluation is how Python generators work (lazy evaluation until .next is called). Spark programs are lazily evaluated via transformations, and only when an action is called (e.g. display result or save output), will the program actually run.
    - Lazily evaluated transformation: `df.select("user_id").join(df_2, on="user_id")`
    - Action will trigger compilation and execution of code.
      - `df.collect()`

## Apache Spark Terms
- **Resilient Distributed Datasets (RDDs)**
  - a fundamental data structure of Spark and an immutable distributed collection of objects. 
  - Each dataset in RDD is divided into logical partitions, which may be computed on different nodes in the cluster
  - Resilient = they are resilient due to their immutability and lineage graphs (which will be discussed shortly)
  - Distributed = partitions in multiple nodes
  - RDD is a read-only, partitioned collection of records. RDDs can be created through deterministic operations on either data on stable storage or other RDDs. RDD is a fault-tolerant collection of elements that can be operated on in parallel.
  - RDDs support in-memory processing computation. This means, it stores the state of memory as an object across the jobs and the object is sharable between those jobs. Data sharing in memory is 10 to 100 times faster than network and Disk.
- **Spark DataFrame**
  - Abstraction on top of RDDs
  - Have all features of RDDs, but also a schema
  - **Typically use DataFrames instead of RDDs directly.**
  - DataFrames are just organized into a columnar structure.
  - Similar to a table in a relational database
  - More optimized than RDDs
    - Optimization takes place using catalyst optimizer. Dataframes use catalyst tree transformation framework in four phases: a) Analyzing a logical plan to resolve references. b) Logical plan optimization. c) Physical planning. d) Code generation to compile parts of the query to Java bytecode.
- **Transformations**
  - They are lazy operations that can be applied to RDDs to create one or more new RDDs. It’s important to note that Transformations create new RDDs because, remember, RDDs are immutable so they can’t be altered in any way once they’ve been created.
  - Transformations take an RDD as an input and perform some function on them based on what Transformation is being called, and outputs one or more RDDs.
  - As a compiler comes across each Transformation, it doesn’t actually build any new RDDs, but rather constructs a chain of hypothetical RDDs that would result from those Transformations which will only be evaluated once an Action is called.
  - This chain of hypothetical, or “child”, RDDs, all connected logically back to the original “parent” RDD, is what a lineage graph is.
  - Examples: `map`, `filter`, `flatMap`, `union`, `intersection`, `groupByKey`, `reduceByKey`, `join`, `pipe`, `repartition`, `coalesece`
- **Actions**
  - An Action is any RDD operation that does not produce an RDD as an output. Some examples of common Actions are doing a count of the data, or finding the max or min, or returning the first element of an RDD, etc. As was mentioned before, an Action is the cue to the compiler to evaluate the lineage graph and return the value specified by the Action.
  - Examples: `reduce`, `collect`, `count`, `first`, `take`, `countByKey`
- **Lineage Graph**
  - a lineage graph outlines what is called a “logical execution plan”
  -  What that means is that the compiler begins with the earliest RDDs that aren’t dependent on any other RDDs, and follows a logical chain of Transformations until it ends with the RDD that an Action is called on.

## How I've used Spark
At CBS Interactive, we used Spark on Google Cloud Dataproc to generate daily user movie / show recommendations for CBS All Access (similar to the Recommended For You carousel you see on Netflix). Google Cloud Dataproc is a managed Spark & Hadoop service on Google Cloud Platform that makes open source data and analytics processing fast, easy, and more secure in the cloud.

We chose Spark for a few reasons. First, Spark is able to handle large amounts of user interaction data in an efficient manner (e.g. millions of records and TBs of data processed within an hour). In order to generate relevant and personalized movie / show recommendations, we used a collaborative filtering recommendation model, which essentially predicts what a given user might like based on the preferences of users with similar interests. Conveniently, Spark provides a really nice API for the [collaborative filtering model](https://spark.apache.org/docs/latest/ml-collaborative-filtering.html), which we've used for training, testing, and tuning of hyperparameters of the collaborative filtering recommendation model on our internal user interaction data as well as predicting new movie / show recommendations for users.

As a Machine Learning Engineer at CBS Interactive, I was tasked with creating a new collaborative filtering model and workflow to incorporate a new implicit feedback column (e.g. duration watched) as well as add business rules to postprocess the recommendations (e.g. filter out non-kid movies / shows from kids profiles). Implicit feedback (e.g. views, clicks, purchases, likes, shares etc.) represents the strength in observations of user actions towards a given product like movie or show. The collaborative model training, testing, tuning, predicting, and postprocessing were all done using Spark.

## Spark Tips
Here are my messy set of notes which include some useful tips when using Spark:

- Avoid shuffling the data
  - Shuffle is an expensive operation since it involves disk I/O, data serialization, and network I/O.
  - Transformations that cause shuffle include:
    - cogroup, groupWith, join, groupByKey, reduceByKey, combineByKey, sortByKey, distinct, intersection, repartition, coalesce, aggregation with window functions using Window.partitionBy()
- Avoid groupByKey and use reduceByKey or combineByKey instead.
  - groupByKey shuffles all the data, which is slow.
  - reduceByKey shuffles only the results of sub-aggregations in each partition of the data.
- Partitioning
  - Partitioning by a column is similar to indexing a column in a relational database.
  - The partition columns should be used frequently in queries for filtering and should have a small range of values with enough corresponding data to distribute the files in the directories.
  - Ideal place to partition is at the data source, while fetching the data.
  - `repartition(N)` to reorder and either increase or decrease the number of partitions with shuffling data across the network to achieve even load balancing.
  - Repartition before writing to storage
- Coalesce
  - can use `coalesce(N)` to reduce the number of partitions in a DataFrame without shuffling
- Broadcast
  - Broadcast variables are read-only shared variables that are cached and available on all nodes in a cluster in-order to access or use by the tasks.
  - Useful to apply broadcast joins espeically joining large DF with a smaller DF
- Cache
  - Cache RDDs when using iterative algorithms or fast interactive RDD use
  - keep in memory for much faster access next time you query it
  - When to cache:
    - RDD re-use in iterative machine learning applications
    - RDD re-use in standalone Spark applications
    - When RDD computation is expensive, caching can help in reducing the cost of recovery in the case one executor fails
- Some useful SQL Spark API commands
  - coalesce(num_partitions)
    - Combine data down to num_partitions
  - broadcast
    - shared variable that caches data to all nodes
    - can be used to apply broadcast joins
    - Marks a DataFrame as small enough for use in broadcast joins.
  - repartition(num_partitions, *cols)
    - cols specifies partitioning column
    - Return a new RDD that has exactly numPartitions partitions
    - increase/decrease level of parallelism in this RDD.
    - Uses a shuffle to redistribute data.
  - cache()
    - Persist this RDD with the default storage level (MEMORY_ONLY).
  - union
    - combine rows from two different data frames
  - left_anti join
    - join all rows from df1 that are not present in df2
  - explode
    - Returns a new row for each element in the given array or map.

## Conclusion
I've enjoyed using Spark for many reasons. It's extremely powerful when dealing with big data, the API is really easy to use and well documented, and it has many useful ML algorithms ready to use.

# References
- https://www.tutorialspoint.com/apache_spark/apache_spark_rdd.htm
- https://towardsdatascience.com/a-neanderthals-guide-to-apache-spark-in-python-9ef1f156d427
- https://luminousmen.com/post/spark-tips-partition-tuning