FOR DEMO

![alt text](https://github.com/omNovos/RuleEngine/blob/master/rule_engine_ver_0.4/scshot.png)

API Documentation: https://app.swaggerhub.com/apis/deepengine/RuleEngine/0.4

# Some notes on this Demo Rules Engine

1.	demoPersonalizationTrigger method requires 2 inputs: the trigger (now there is only one “trigger1”) and the shopperId. It will:

    a.	Find all personalization rules that associated with the trigger (assignments)

    b.	Run all queries in each rule to find the winner (personalizations)

    c.	Find the content that associated with that rule (assignments)
    
    d.	Assign content to the shopper (assigned_contents)

2.	demoSegmentation method requires 2 inputs: segmentationId, and contentId. Similarly, it will:

    a.	Run all queries in the segmentation rule to find the correct list of shopper (segmenations)

    b.	Assign content to the list of shoppers (assigned_contents)

3.	We have already created a dataset followed with the document Miller sent to test the engine. For Allan, we create all 
the POST you need to replicate this dataset on your instance.

# Test cases we did:

## Case 1: segmentation 
GET localhost:5000/method/demoSegmentation/seg1/content1

=======Result=========

[
    {
        "shopperId": "shopper1",
        "contentId": "content1",
        "segmentationId": "seg1"
    }
]

## Case 2: personalization 
GET localhost:5000/method/demoPersonalizationTrigger/shopper1/trigger1

=======Result=========

{
    "shopperId": "shopper1",
    "contentId": "content3",
    "personalizationId": "per1"
}

# POST commands

POST /shoppers/shopper/shopper1
{
  "shopperId":"shopper1",
  "firstName":"Richard"
}

POST /contents/content/content1
{
  "contentName": "Communication 1 - Beyond meat general",
"title": "The Amazing Beyond Burger Has Arrived",
"description": "Announcing the arrival of the Beyond Burger – You won’t believe its not meat"
}

POST /contents/content/content2
{
  "contentName": "Communication 2 - Beyond meat targeted",
"title": "10% Off The Beyond Burger",
"description": "When you buy 2 or more"
}

POST /contents/content/content3
{
  "contentName": "Communication 3 - Recommended Recipe",
"title": "Beyond Sliders with Grape ColeSlaw",
"description": "Guilt free comfort food in less than 30 min",
"image":"https://www.metro.ca/en/recipes-occasions/recipes/smoked-meat-sandwich-and-cabbage-salad-with-grapes"
}

POST /contents/content/content4
{
  "contentName": "Communication 4 -  Hot Bar Special",
"title": "Fresh from our hot bar",
"description": "Your choice of chicken OR Eggplant parmesan topped with fresh basil and served over penne and marinara sauce. Only $9 per portion",
"image":"https://www.google.com/search?rlz=1C1GGRV_enCA752CA752&biw=1163&bih=554&tbm=isch&sa=1&ei=rkjLXOyaEIWO5wLW57TgCg&q=chicken+parm&oq=chicken+parm&gs_l=img.3..0i67l3j0j0i67l6.6555.7884..8065...0.0..1.554.2432.3-4j1j1......1....1..gws-wiz-img.......35i39.kzmWzu20SDw#imgrc=BoE7dJAHdVXZpM:"
}

POST /preferred_stores/preferred_store/pre1
{
  "shopperId": "shopper1",
  "preferredStoreName": "store1"
}

POST /questions/question/1
{
  "Are you a vegetarian?": "yes",
  "shopperId": "shopper1"
}

POST /questions/question/2
{
  "Are you looking to add more plant based proteins to your diet?": "yes",
  "shopperId": "shopper1"
}

POST /questions/question/3
{
  "Do you prefer home cooking or eating out?": "Home Cooking",
  "shopperId": "shopper1"
}

POST /questions/question/4
{
  "Are you interested in meat alternatives and substitutes?": "yes",
  "shopperId": "shopper1"
}

POST /questions/question/5
{
  "Do you enjoy trying new recipes and ingredients?": "no",
  "shopperId": "shopper1"
}

POST /queries/query/query1
{
  "queryName": "Richard Store",
  "indexName": "preferred_stores",
  "queryBody": {"condition":"AND","rules":[{"id":"preferredStoreName","field":"preferredStoreName","type":"string","input":"text","operator":"equal","value":"store1"}]}
}

POST /queries/query/query2
{
  "queryName": "Richard Question",
  "indexName": "questions",
  "queryBody": {"condition":"OR","rules":[{"id":"Are you a vegetarian?","field":"Are you a vegetarian?","type":"string","input":"text","operator":"equal","value":"yes"},{"id":"Are you looking to add more plant based proteins to your diet?","field":"Are you looking to add more plant based proteins to your diet?", "type":"string","input":"text","operator":"equal","value":"yes"}]}
}

POST /queries/query/query3
{
  "queryName": "Question 1",
  "indexName": "questions",
  "queryBody": {"condition":"AND","rules":[{"id":"Do you prefer home cooking or eating out?","field":"Do you prefer home cooking or eating out?","type":"string","input":"text","operator":"equal","value":"Home Cooking"}]}
}

POST /queries/query/query4
{
  "queryName": "Question 2",
  "indexName": "questions",
  "queryBody": {"condition":"AND","rules":[{"id":"Are you interested in meat alternatives and substitutes?","field":"Are you interested in meat alternatives and substitutes?","type":"string","input":"text","operator":"equal","value":"yes"}]}
}

POST /queries/query/query5
{
  "queryName": "Question 3",
  "indexName": "questions",
  "queryBody": {"condition":"AND","rules":[{"id":"Do you enjoy trying new recipes and ingredients?","field":"Do you enjoy trying new recipes and ingredients?","type":"string","input":"text","operator":"equal","value":"no"}]}
}

POST /segmentations/segmentation/seg1
{
  "segmentationName": "Richard Store Segment",
"queryIds": ["query1"]
}

POST /segmentations/segmentation/seg2
{
  "segmentationName": "Richard Question Segment",
"queryIds": ["query1", "query2"]
}

POST /personalizations/personalization/per1
{
  "personalizationName": "Question 1",
"scoredQuerieIds":
[
    {
      "queryIds" : ["query3"],
      "point" : 100
    },
    {
      "queryIds" : ["query5"],
      "point" : 50
    }
]
}

POST /personalizations/personalization/per2
{
  "personalizationName": "Question 2",
"scoredQuerieIds":
[
    {
      "queryIds" : ["query4"],
      "point" : 100
    }
]
}

POST /triggers/trigger/trigger1
{
  "triggerName": "demo"
}

POST /competition_pools/competition_pool/comp1
{
  "competitionPoolName": "demo"
}

POST /assignments/assignment/assign1
{
  "assigmentName": "Assignment 1",
"triggerId": "trigger1",
"competitionPoolId": "comp1",
"personalizationId": "per1",
"contentId": "content3"
}

POST /assignments/assignment/assign2
{
  "assigmentName": "Assignment 2",
"triggerId": "trigger1",
"competitionPoolId": "comp1",
"personalizationId": "per2",
"contentId": "content4"
}

POST /assigned_contents/assigned_content/ac1
{
"shopperId": "shopper1",
"contentId": "content1",
"segmentationId": "seg1"
}

POST /assigned_contents/assigned_content/ac2
{
"shopperId": "shopper1",
"contentId": "content2",
"segmentationId": "seg2"
}

POST /assigned_contents/assigned_content/ac3
{
"shopperId": "shopper1",
"contentId": "content3",
"segmentationId": "per1"
}
