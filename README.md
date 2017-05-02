# spacehack
dating app


### scenario:
1. upload link to image with girl/boy that you like
2. put link to your vk.com account 
3. put find victims 
4. see girls / boys who are ready for relationships,
   have similar interests with you 
   similar to the photos that you have already uploaded


#### tech scenario explanation

1. create embeddings from user profiles
2. create embedding of user interests based on user communities and base info from profile
3. create a model that can predict the status of relationships based on sociel profile
4. create / find / implement / integrate model for face recognition
5. create / find / implement / integrate an algorithm for face similarity 
6. merge models with relevant coefficients


#### tech stack of technologies

1. word2vec for text embedding creation 
2. tfidf + word2vec embedding for model like doc2vec creation
3. xgboost for model for status relationships prediction
4. openface (cnns) for deep learning face recognition - embeddings of photos
6. custom metric for similarity between pictures (ml model based on torch framework)
7. custom metric for similarity between users and their interests (like normalised euclidian distance )
