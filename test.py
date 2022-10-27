
ly={"abc": 3, "defg": 4, "hijkl": 5}
print([(i,j) for i,j in zip(ly.keys(), [ly[i] for i in ly])])
print(ly["abc"])