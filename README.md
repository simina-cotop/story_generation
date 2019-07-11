# story_generation

All data should be under the folder "data6u"

---------------------------------------------------------

To run the model, go to model8 folder and run the model_8.py script
```
python model_8.py
```

---------------------------------------------------------

## Things to keep in mind before running the model:
* You need to download google word2vector embeddings and change the path of the variable **Word2Vec_Google_Path** inside *Configurations.py* script to the path where you have the embeddings.

---------------------------------------------------------

## Things to keep in mind when running the model
* Whenever you want to debug the model and check the values of the many many variables to get an overview, remember ```print``` is your friend.
* If you get an error like ```AttributeError: 'ProgbarLogger' object has no attribute 'log_values'```, don't panic. Just check if your dataset has been loaded by checking ```x_train``` within *dataLoaders.py*. Print this variable and make sure that the data is being loaded. If it's empty, you need to check further to see where is the problem.

## TODO : Description of event_desc.cvs
