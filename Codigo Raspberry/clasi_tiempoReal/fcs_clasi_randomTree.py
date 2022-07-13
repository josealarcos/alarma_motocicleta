import pandas as pd
import alarma


alarma.activar(1)
#preparamos datos para el entrenamiento
ax = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/ax.csv',sep=",",header=None)
ax = ax.interpolate(method="ffill")
ay = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/ay.csv',sep=",",header=None)
ay = ay.interpolate(method="ffill")
az = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/az.csv',sep=",",header=None)
az = az.interpolate(method="ffill")
gx = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/gx.csv',sep=",",header=None)
gx = gx.interpolate(method="ffill")
gy = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/gy.csv',sep=",",header=None)
gy = gy.interpolate(method="ffill")
gz = pd.read_csv('/home/pi/clasi_tiempoReal/csv_data/gz.csv',sep=",",header=None)
gz = gz.interpolate(method="ffill")
#definimos la que será la matriz de entrenamiento
df = pd.concat([ax,ay.iloc[:,1:],az.iloc[:,1:],gx.iloc[:,1:],gy.iloc[:,1:],gz.iloc[:,1:]],axis=1)
df = pd.concat([df,df,df,df,df],axis=0)
df = pd.concat([df,df,df,df,df],axis=0) 
#definimos nuestras variables X e Y
X = df.iloc[:,1:]
Y = df.iloc[:,0]
#COMENZAMOS EL ENTRENAMIENTO
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.3,random_state=1)
#entrenamos nuestro modelo con el algoritmo de random forest 
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=500,n_jobs=-1,random_state=1)
rf.fit(x_train,y_train)
#entrenamos por decission tree
'''from sklearn.tree import DecisionTreeClassifier
rf = DecisionTreeClassifier(random_state=1)
rf.fit(x_train,y_train)'''
print('entreamiento realizado')


