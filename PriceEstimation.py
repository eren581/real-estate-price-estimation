import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from statsmodels.tools.eval_measures import rmse
from sklearn.metrics import explained_variance_score

model = pickle.load(open("model.sav", 'rb'))

def readFromFile():
    read = np.load("test.npy")
    df = pd.DataFrame(read)
    Y = df[0]
    X = df.drop(0, axis=1)
    scaler = StandardScaler().fit(X)
    rscl_X = scaler.transform(X)
    predict(rscl_X,Y)
def byHand():
    X = [0] * 59
    district = [0]*16
    dist = input("Please Choose District:\n1-Akyurt2-Altındağ3-Beypazarı4-Elmadağ5-Etimesgut6-Gölbaşı7-Kahramankazan8-Keçiören9-Kızılcahamam10-Mamak11-Polatlı12-Pursaklar13-Sincan14-Yenimahalle15-Çankaya16-Çubuk\n")
    district[int(dist)-1]=1
    X[43:]=district
    X[0]=int(input("Square Meters: "))
    X[1]=int(input("Room Number: "))
    X[2]=int(input("Building Age: "))
    floor=[0]*10
    house=input("To Enter Floor press(1) Or other floor types press (2): 1-Basement2-Ground Floor3-Garden Floor4-Entrance Floor5-High Entrance6-Private7-Villa8-Loft9-Floor Over 30")
    if (house is '1'):
        h1=int(input("Floor number: "))
        floor[9]=h1
    elif (house is '2'):
        h2=int(input(" "))
        floor[h2-1]=1
    X[3:13]=floor
    X[13]=int(input("Building Floor: "))
    heating=[0]*5
    ht=int(input("Choose Heating Type: 1-Stove 2-Boiler 3-Central heating 4-Natural gas 5-Floor Heating"))
    heating[ht-1]=1
    X[14:19]=heating
    X[19] = int(input("Bathroom Number: "))
    X[20]=int(input("Please Press 0(No) or 1(Yes)\nHas Balcony:"))
    X[21]=int(input("Has Furniture:"))
    X[22]=int(input("Has Woodwork: "))
    X[23]=int(input("Alarm(Thief): "))
    X[24]=int(input("Elevator: "))
    X[25]=int(input("Fiber: "))
    X[26]=int(input("Laminate: "))
    X[27]=int(input("Parquet"))
    X[28]=int(input("Has Security: "))
    X[29]=int(input("Thermal insulation: "))
    X[30]=int(input("Parking Lot: "))
    X[31]=int(input("Sports Area: "))
    X[32]=int(input("Shopping Mall: "))
    X[33]=int(input("Hospital: "))
    X[34]=int(input("Market: "))
    X[35]=int(input("University: "))
    X[36]=int(input("Primary School: "))
    X[37]=int(input("Town Center: "))
    X[38]=int(input("Main Road: "))
    X[39]=int(input("Subway: "))
    X[40]=int(input("Bus Stop: "))
    X[41]=int(input("Minibus:"))
    X[42]=int(input("Has Landscape: "))
    X=np.array(X).reshape(1,-1)
    print("Price: ",int(np.exp(model.predict(X))))

def predict(X,Y):
    pre = model.predict(X)
    actual_y_test = np.exp(Y)
    actual_predicted = np.exp(pre)
    diff = abs(Y - actual_predicted)
    compare_actual = pd.DataFrame({'Test Data': actual_y_test, 'Predicted Price': actual_predicted, 'Difference': diff})
    compare_actual = compare_actual.astype(int)
    print("Root Mean Squared Error: ",rmse(actual_predicted, actual_y_test))

    print("Variance Score: ",explained_variance_score(actual_y_test,actual_predicted))
    compare_actual.to_csv('results.csv')
while(1):
        inpt = input("1-Test file\n2-By Hand\n3-Exit\nPlease press (1/2/3): ")
        if inpt == '1':
                readFromFile()
        if inpt == '2':
                byHand()
        if inpt == '3':
                exit(0)