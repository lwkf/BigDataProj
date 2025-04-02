# BigDataProj

- Hadoop NameNode UI: http://localhost:9870
- Spark Master UI: http://localhost:8080
- Spark Worker UI: http://localhost:8081

# Yelp Dataset Analysis with Hadoop/Spark

![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Hadoop](https://img.shields.io/badge/Apache_Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black)
![Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)

This project processes raw Yelp dataset JSON files into cleaned, analysis-ready formats using Hadoop MapReduce. The cleaned datasets are then available for further analysis with Spark.

## Prerequisites

- Docker Desktop ([Windows](https://docs.docker.com/desktop/install/windows-install/)/[Mac](https://docs.docker.com/desktop/install/mac-install/))
- 8GB+ RAM recommended
- Git

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/lwkf/BigDataProj.git
```

### 2. Download Dataset
- Get the Yelp dataset from official source: https://business.yelp.com/data/resources/open-dataset/
- Get the AFINN-111 text for sentiment analysis from offical source: https://github.com/fnielsen/afinn/blob/master/afinn/data/AFINN-111.txt 
- Extract the files into ./data folder:
```bash
data/
├── business.json
├── review.json
├── user.json
├── checkin.json
├── tip.json
└── AFINN-111.txt
```

### 3. Start Containers
```bash
docker-compose up -d
```

## Data Processing Pipeline
1. Enter namenode terminal
```bash
docker exec -it namenode bash
```
2. Create a directory in the node and copy data files over.
- NOTE: When `-put` command is executed, `INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false` will be printed periodically until the command finishes execution. This process may take a while as all datasets are being copied from local to the namenode.
```bash
# Inside container:
hdfs dfs -mkdir -p /yelp/input
hdfs dfs -put /data/*.json /yelp/input/
hdfs dfs -put data/AFINN-111.txt /yelp/input/
```
3. Install Python onto the node.
```bash
# Install Python
# Backup current sources list
cp /etc/apt/sources.list /etc/apt/sources.list.bak

# Update to use the archived repositories for Debian Stretch
echo "deb http://archive.debian.org/debian stretch main contrib non-free" > /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main contrib non-free" >> /etc/apt/sources.list

# Add [check-valid-until=no] to prevent expiration errors
echo "Acquire::Check-Valid-Until \"false\";" > /etc/apt/apt.conf.d/10-nocheckvalid
echo "APT::Get::Assume-Yes \"true\";" >> /etc/apt/apt.conf.d/10-nocheckvalid
echo "APT::Get::AllowUnauthenticated \"true\";" >> /etc/apt/apt.conf.d/10-nocheckvalid

apt-get update
apt-get install -y python3

# Verify Python Installation
python3 --version
```
4. Create a shortcut (symlink) to point towards the Python executable.
```bash
# Create a Python Symlink
ln -s /usr/bin/python3 /usr/bin/python
```

## Install Mappers/Reducers
- Open a new terminal tab to run these commands locally
- For each file (business_mapper.py, business_reducer.py, etc.):
```bash
# Copy from local to namenode
docker cp scripts/mappers/business_mapper.py namenode:/business_mapper.py
docker cp scripts/reducers/business_reducer.py namenode:/business_reducer.py
docker cp scripts/mappers/review_mapper.py namenode:/review_mapper.py
docker cp scripts/reducers/review_reducer.py namenode:/review_reducer.py
docker cp scripts/mappers/user_mapper.py namenode:/user_mapper.py
docker cp scripts/reducers/user_reducer.py namenode:/user_reducer.py
docker cp scripts/mappers/checkin_mapper.py namenode:/checkin_mapper.py
docker cp scripts/reducers/checkin_reducer.py namenode:/checkin_reducer.py
docker cp scripts/mappers/tip_mapper.py namenode:/tip_mapper.py
docker cp scripts/reducers/tip_reducer.py namenode:/tip_reducer.py
```

## Run Cleaning Jobs
Execute these in the namenode terminal tab:
### Business Data
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files business_mapper.py,business_reducer.py \
    -mapper "python business_mapper.py" \
    -reducer "python business_reducer.py" \
    -input /yelp/input/business.json \
    -output /yelp/output/cleaned_business
```
### Review Data
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files review_mapper.py,review_reducer.py \
    -mapper "python review_mapper.py" \
    -reducer "python review_reducer.py" \
    -input /yelp/input/review.json \
    -output /yelp/output/cleaned_reviews
```
### User Data
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files user_mapper.py,user_reducer.py \
    -mapper "python user_mapper.py" \
    -reducer "python user_reducer.py" \
    -input /yelp/input/user.json \
    -output /yelp/output/cleaned_users
```
### Checkin Data
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files checkin_mapper.py,checkin_reducer.py \
    -mapper "python checkin_mapper.py" \
    -reducer "python checkin_reducer.py" \
    -input /yelp/input/checkin.json \
    -output /yelp/output/cleaned_checkins
```
### Tip Data
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files tip_mapper.py,tip_reducer.py \
    -mapper "python tip_mapper.py" \
    -reducer "python tip_reducer.py" \
    -input /yelp/input/tip.json \
    -output /yelp/output/cleaned_tips
```
### Check files were created with no issues
```bash
#There should be 5 items
hdfs dfs -ls /yelp/output
```
## To access spark
Open a new terminal tab to run these commands:
```bash
#Access the Spark master container
docker exec -it spark-master bash

#Run PySpark
/spark/bin/spark-shell --master spark://spark-master:7077
```

### Load Cleaned Datasets to Spark
```bash
val businessDF = spark.read.json("hdfs://namenode:9000/yelp/output/cleaned_business")
val reviewDF = spark.read.json("hdfs://namenode:9000/yelp/output/cleaned_reviews")
val userDF = spark.read.json("hdfs://namenode:9000/yelp/output/cleaned_users")
val checkinDF = spark.read.json("hdfs://namenode:9000/yelp/output/cleaned_checkins")
val tipDF = spark.read.json("hdfs://namenode:9000/yelp/output/cleaned_tips")
val afinnRDD = spark.sparkContext.textFile("hdfs://namenode:9000/yelp/input/AFINN-111.txt")
```

### Sample Spark Analysis
```bash
# Top 10 cities with most businesses
businessDF.groupBy("city", "state")
  .count()
  .orderBy($"count".desc)
  .show(10, false)
```

## Final Setup
- 3 Terminal Tabs, one for local, one for namenode, one for spark-master
- Cleaned Datasets obervable within the namenode terminal using
```bash
#There should be 5 items
hdfs dfs -ls /yelp/output
```
- 5 datasets loaded into spark (businessDF, reviewDF, userDF, checkinDF, tipDF)

## Next Steps

- Perform Analysis within Spark
- Save outputs to a csv to use for visualisation
1.  In the Spark Shell, Save the output to HDFS
```bash
# Ensure your Spark DataFrame is saved as a CSV in HDFS
analysisResult 
  .coalesce(1) 
  .write 
  .option("header", "true") 
  .mode("overwrite") 
  .csv("hdfs://namenode:9000/yelp/output/analysis_result")
```
2.  In the namenode terminal tab, Retrieve the output from HDFS
```bash
# Copy the output file from HDFS to the local machine
hdfs dfs -get /yelp/output/analysis_result ./output
```
3. Locate the CSV File
```bash
# Locate the correct file
find ./output -name "part-*.csv"
```
4. Open a new terminal tab and Copy the file from Docker
```bash
# Copy the output file to the host machine
docker cp namenode:/output/part-00000-*.csv ./analysis_output/analysis_result.csv
```
Now the retrieved csv file is ready for visualisation.
- To close docker container run:
```bash
docker-compose down  
```
- To open docker container again, run:
```bash
docker-compose up -d
```

