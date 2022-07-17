from os import listdir
import pandas
from application_logging.logger import App_Logger


class dataTransformPredict:
    """
                  This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.

                  """

    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validated/Good_Raw"
        self.logger = App_Logger()

    def replaceMissingWithNull(self):

        """
                                  Method Name: replaceMissingWithNull
                                  Description: This method replaces the missing values in columns with "NULL" to
                                               store in the table.
                                                      Also, adding quotes to the columns with string data type to store
                                                      in the table.

                                          """

        try:
            log_file = open("Prediction_Logs/dataTransformLog.txt", 'a+')
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pandas.read_csv(self.goodDataPath + "/" + file)
                csv.fillna('NULL', inplace=True)
                # list of columns with string datatype variables
                columns = ['TypeofContact', 'Occupation', 'Gender', 'ProductPitched', 'MaritalStatus',
                           'Designation']

                for col in columns:
                    csv[col] = csv[col].apply(lambda x: "'" + str(x) + "'")

                csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, " %s: File Transformed successfully!!" % file)

        except Exception as e:
            self.logger.log(log_file, "Data Transformation failed because:: %s" % e)

            log_file.close()
            raise e
        log_file.close()