# importing Flask and other modules
from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
from joblib import load

# Flask constructor
app = Flask(__name__) 
# Load the machine learning model and encoder
Random_model = load('model.pkl')
label_en = load('encode.pkl')

# Load crop details
details_data = pd.read_json('crop_details.json')

# Define columns for input data
columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

@app.route('/', methods =["GET", "POST"])
def crop_data():
    a = None
    spacing = None
    timeofsowing = None
    methodofsowing = None
    timeofwater = None
    nutrientrecommendation = None
    weedmanagement = None
    insectmanagement = None
    diseasemanagement = None
    strawyield = None
    
    if request.method == "POST":

        N = request.form.get("nitrogen")
        P = request.form.get("phosphorus")
        K = request.form.get("potassium")
        temperature = request.form.get("temperature")
        humidity = request.form.get("humidity")
        ph = request.form.get("ph")
        rainfall = request.form.get("rainfall")
        columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        data = pd.DataFrame(columns=columns)
        data["N"] = [N]
        data["P"] = [P]
        data["K"] = [K]
        data["temperature"] = [temperature]
        data["humidity"] = [humidity]
        data["ph"] = [ph]
        data["rainfall"] = [rainfall]
        pred = Random_model.predict(data)
        a = label_en.inverse_transform(pred)
        
        print(a)
        a=str(a)
        a=a[2:-2]

        details_data=pd.read_json('crop_details.json')
        crop_names=details_data.name
        print(a)
        for crop_name in crop_names:
            word=crop_name
            if (fuzz.ratio(word, a) >= 70):
                print("Word matched :", fuzz.ratio(word, a) )
                print('selected crop is : ',crop_name)
                spacing = np.array_str(details_data[details_data.name==crop_name].spacing.values)
                timeofsowing = np.array_str(details_data[details_data.name==crop_name].timeOfSowing.values)
                methodofsowing = np.array_str(details_data[details_data.name==crop_name].methodOfSowing.values)
                timeofwater = np.array_str(details_data[details_data.name==crop_name].timeOfWater.values)
                nutrientrecommendation = np.array_str(details_data[details_data.name==crop_name].nutrientRecommendation.values)
                weedmanagement = np.array_str(details_data[details_data.name==crop_name].weedManagement.values)
                insectmanagement = np.array_str(details_data[details_data.name==crop_name].insectManagement.values)
                diseasemanagement = np.array_str(details_data[details_data.name==crop_name].diseaseManagement.values)
                strawyield = np.array_str(details_data[details_data.name==crop_name].strawYield.values)
                spacing = spacing[2:-2]
                timeofsowing = timeofsowing[2:-2]
                methodofsowing = methodofsowing[2:-2]
                timeofwater = timeofwater[2:-2]
                nutrientrecommendation = nutrientrecommendation[2:-2]
                weedmanagement = weedmanagement[2:-2]
                insectmanagement = insectmanagement[2:-2]
                diseasemanagement = diseasemanagement[2:-2]
                strawyield = strawyield[2:-2]
                break

            else:
                a=str(a)
                text_file = open("output.txt", "w")
                text_file.write("PREDICTED CROP NAME: "+a)
                text_file.close()


                # print(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
            
        text_file_read = open("output.txt", "r")
        # return text_file_read.read()+ "\n\n" + "SPACING : " + spacing+ "\n\n" + "TIME OF SOWING : " + timeofsowing+ "\n\n" + "METHOD OF SOWING : " + methodofsowing+ "\n\n" + "TIME OF WATER : " + timeofwater+ "\n\n" + "NUTRIENTS RECOMMENDATION : " + nutrientrecommendation+ "\n\n" + "WEED MANAGEMENT : " + weedmanagement+ "\n\n" + "INSECT MANAGEMENT : " + insectmanagement+ "\n\n" + "DISEASE MANAGEMENT : " + diseasemanagement+ "\n\n" + "STRAW YIELD : " + strawyield
        return render_template("index.html",a=a,spacing=spacing, timeofsowing=timeofsowing, methodofsowing=methodofsowing, timeofwater=timeofwater, nutrientrecommendation=nutrientrecommendation, weedmanagement=weedmanagement, insectmanagement=insectmanagement, diseasemanagement=diseasemanagement, strawyield=strawyield)

    
    return render_template("index.html")

if __name__=='__main__':
    app.run()
