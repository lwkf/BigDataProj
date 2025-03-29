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
- Extract the files into ./data folder:
```bash
data/
├── business.json
├── review.json
├── user.json
├── checkin.json
└── tip.json
```

### 3. Start Containers
```bash
docker-compose up -d
```

## Data Processing Pipeline
Load Data to HDFS
```bash
docker exec -it namenode bash

# Inside container:
hdfs dfs -mkdir -p /yelp/input
hdfs dfs -put /data/*.json /yelp/input/
```

## Install Mappers/Reducers
For each file (business_mapper.py, business_reducer.py, etc.):
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

# Verify files exist
```bash
docker exec -it namenode ls /
```

## Run Cleaning Jobs
Execute these in separate terminal tabs:
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
