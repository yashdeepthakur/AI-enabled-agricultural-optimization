from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
from joblib import load
Random_model = load('model.pkl')
label_en = load('encode.pkl')

# Define columns and create an empty DataFrame
columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
data = pd.DataFrame(columns=columns)

# Function to read input data
def read(data):
    for col in columns:
        value = input(f"Enter {col}: ")
        data[col] = [value]

# Read input data
read(data)
print(data)

# Predict using the model
pred = Random_model.predict(data)

# Inverse transform the predictions
a = label_en.inverse_transform(pred)
print(a)
a=str(a)
a=a[2:-2]

details_data=pd.read_json('crop_details.json')
crop_names=details_data.name
for crop_name in crop_names:
    word=crop_name
    if (fuzz.ratio(word, a) >= 70):
        print("Word matched :", fuzz.ratio(word, a) )
        print('selected crop is : ',crop_name)
        # print(medical_data[medical_data.name==disease_name])
        
        #open text file
        text_file = open("output.txt", "w")
        text_file.write("PREDICTED CROP NAME : "+crop_name)
        text_file.write("\n\n")
        text_file.write("SPACING :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].spacing.values))
        text_file.write("\n\nTIME OF SOWING : \n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].timeOfSowing.values))
        text_file.write("\n\nMETHOD OF SOWING : \n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].methodOfSowing.values))
        text_file.write("\n\nTIME OF WATER : \n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].timeOfWater.values))
        text_file.write("\n\nNUTRIENTS RECOMMENDATION :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].nutrientRecommendation.values))
        text_file.write("\n\nWEED MANAGMENT :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].weedManagement.values))
        text_file.write("\n\nINSECT MANAGEMENT :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].insectManagement.values))
        text_file.write("\n\nDISEASE MANAGEMENT :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].diseaseManagement.values))
        text_file.write("\n\nSTRAW YIELD :\n")
        text_file.write(np.array_str(details_data[details_data.name==crop_name].strawYield.values))
        text_file.close()
        break
        
    else:
        a=str(a)
        text_file = open("output.txt", "w") 
        text_file.write("PREDICTED DISEAS56E NAME : "+a)
        text_file.close()
        
        


