## travel-purchase-prediction-with-deployment

#### Problem Statement
    Tourism is one of the most rapidly growing global industries and tourism forecasting is becoming an increasingly 
    important activity in planning and managing the industry. 
    Because of high fluctuations of tourism demand, accurate predictions of purchase of travel packages are of high 
    importance for tourism operators/companies.

    The goal is to predict whether the customer will purchase the travel package or not.
    There are two classes: 0 and 1.

    0: Means that the customer would not purchase the travel package
    1: Means that the customer would purchase the travel package.


#### Data Description
    The client would send data in multiple sets of files in batches at a specific location.
    Dataset will contain travel enquiry data consisting of Passport, Citytier, Occupation etc. for multiple customers.
    The target column will have 0 or 1 value for each customer.

    Apart from training files, the client also needs to provide a "schema" file which contain all the relevant 
    information about the training files such as:
    Name of the files, Length of Date value in FileName, Length of Time value in FileName, NUmber of Columnns, 
    Name of Columns, and their datatypes.

#### Data Validation
    In Data Validation, we perform different sets of validation on the given set of training files.
    
    Name Validation: validate the name of the files based on the given sample file name in the schema file. We have 
    created a regex pattern as per the sample name given in the schema file to use for name validation. 
    
    Length: After validating the pattern in the name, check for the length of the date in the file name as well as 
    the length of time in the file name. If all the values are as per requirements, we move such files to 'Good_Data' 
    Folder else we move such files to 'Bad_Data' Folder.
    
    Number of Columns: We validate the number of columns present in the files, and if it doesn't match with the value 
    given in the schema file, then the file is moved to 'Bad_Data' Folder.
    
    Name of Columns: The name of the columns is validated and should be the same as given in the schema file. 
    If not, then the file is moved to 'Bad_Data' Folder.
    
    The datatype of columns: The datatype of columns is given in the schema file. This is validated when we insert
    the files into Database. If the datatype is wrong, then the file is moved to 'Bad_Data' Folder.
    
    Null values in columns: If any of the columns in a file have all the values as NULL or missing, we discard such
    a file and move it to 'Bad_Data' Folder.


#### Data Insertion in Database
     Database Creation and Connection: Create a database with the given name passed. If the database is already created,
     open the connection to the database.
     
     Table creation in the database: Table with name - 'Good_Data', is created in the database for inserting the files 
     in the 'Good_Data' Folder based on given column names and datatype in the schema file. If the table is already
     present, then the new table is not created and new files are inserted in the already present table as we want 
     training to be done on new as well as old training files.
     
     Insertion of file in the table: All the files in the 'Good_Data' Folder are inserted in the above-created table. 
     If any file has invalid data type in any of the columns, the file is not loaded in the table and is moved to 
     'Bad_Data' Folder.
     After the files from 'Good_Data' Folder are inserted into the database, the Good_Data Folder is deleted.
     Also, the files in the 'Bad_Data' folder are moved to the Archive folder.
     
#### Model Training
     Data Export from Database: The data that is stored in the database is exported as a CSV file which acts as an imput 
        file for model training.
     
     Data Preprocessing: 
        First we remove the columns which are not useful for the training for example 'CustomerId' has no role in 
        training.
        Next, need to work on Encoding the categorical values of relevant features as categorical values need to be 
        transformed to numerical values to make them work with machine learning models.
        
        Then check for null values in the columns. If present, impute the null values using the KNN imputer.
        
        Next, check if any column has zero standard deviation, need to remove such columns as they don't give any 
        information during model training.
        
        Also need to apply oversampling approach to handle imbalance in the classes of the dataset.
        
    Clustering: 
        KMeans algorithm has been used to create clusters for the preprocessed data. The optimum number of clusters is 
        then selected and the preprocessed data is divided in same number of clusters.

    Model Selection and Hyperparameter Tuning:
        After dividing the data into clusters, we divide it into train and test data for each cluster.
        Following that, find the best model for each cluster out of the list of appropriate models which can be tried 
        as per the business problem. Then we perform hyperparameter tuning with GridSearchCV for these models 
        individually to get the optimal parameters for the models and compare their performance to choose the model with
        best results.
        For the given business problem, Random Forest and XGBoost have been considered to find the best model. This can 
        be different and multiple models can be used depending on the business problem. 

    Model Saving:
        The best model for each cluster would then be saved as per the cluster number, appending the cluster number at 
        the end of every model file in the 'models' folder. As a result when we have to do prediction, we will get 
        correct model for the given cluster.

#### Prediction
     For prediction, it follows the same steps given above ranging from reading the data to Data Validation then to 
     Data Transformation and then the DB operations- Data Insertion and Exporting the data to a csv file which act as 
     the input file for the prediction.
     Then this is followed by Data Preprocessing steps similar to what has been covered while training the data.
     Then Clustering is performed over individual clusters and model for each cluster is loaded. And then prediction 
     is done with the help of loaded model and the predictions are combined into a dataframe and saved in a csv file.
     Prediction can be performed from GUI or from postman tool.

#### Docker
    Docker provides the runtime envrionment to run the application independent of the system. As a result of 
    dockerizing the application, it would work successfully on ony Operating system.
    
    Whenever one needs to dockerize their solution, docker image would be created and Dockerfile would store the steps 
    that are needed to create the docker image.
    When working on large scale, Kubernates can be used to deploy the docker image and to manage the container.

#### CI/CD with CircleCI
    For maintaining Continuous Integration and Delivery pipeline, CircleCI tool has been used.
    The main purpose of establishing a CI/CD pipeline is to automate the process of building, testing and deploying 
    the code.

    The actions for building stages and deployment have been written in config.yml file present in '.circleci' directory.
    These steps/instructions get executed on the machine that CicleCI provides.

    It then uses the existing dockerfile to create the docker image which is then pushed to docker hub.
    The same docker image then gets deployed to heroku. This can also be deployed to Azure/other Cloud if one has the
    cloud provider account to deploy the application.

![Build_Pipeline_image](https://github.com/Karan-Pruthi/travel-purchase-prediction-deployment/blob/main/images/CircleCI_Actions.PNG)

