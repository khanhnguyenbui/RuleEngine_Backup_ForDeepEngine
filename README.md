# Rule Engine



## Easy usage
The Rule Engine server run on a Flask API framework, which is currently available online at: http://35.237.224.155/

Endpoints description could be seen on a Swagger site at: https://app.swaggerhub.com/apis/deepengine/Shopper/


## Deployment
The Rule Engine API server and the Swagger server are in their correspondent folders. 

For the Rule Engine server, it is currently deployed on Google Cloud Compute VM

1. Firstly by installing required packages:

```
pip3 install -r requirements.txt
```
or (depends on which python is running)
```
python -m pip install -r requirements.txt
```

2. Make sure you don't have any other querybuilder package by pip freeze. Otherwise, clean it.

3. Cd to querybuilder, then run:
```
python setup.py
```

4. Then simply run the server by:
```
python flaskWebServerAPIPortal
```

The Swagger server has its own README for deployment.


## Other Usages
The Google Cloud VM has been paid for several months and will be open for free usage (for now), we are currently running an ElasticSearch instance, with Kibana, which could be accessed at: http://35.237.224.155:5601

## Note
- Please note that the current "Try it out" function on the Swagger site won't work, however, the Rule Engine server works with other methods such as curl or Postman.
- You might need to see the current Elasticsearch server at http://35.237.224.155:5601 to know what are the indexes and their mappings.
- For Windows user:
  - edit 0.0.0.0 to localhost in flaskWebServerAPIPortal
  - remove uwsgi in requirements.txt





