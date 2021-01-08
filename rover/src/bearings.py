from math import radians, cos, sin, asin, sqrt

# A, B are two GPS locations
A = (23.296875399014667, 79.99461999999994)
B = (67.46860181215418, 24.44774499999994)
theta1, lon1 = A
theta2, lon2 = B
# convert degrees into radians
theta1, lon1, theta2, lon2 = map(radians, [theta1, lon1, theta2, lon2])

def bearings(theta1, lon1, theta2, lon2):
	# β = atan2(X,Y)
	# X = cos θb * sin ∆L
	# Y = cos θa * sin θb – sin θa * cos θb * cos ∆L
	diflong = lon2 - lon1
	X = cos(theta2) * sin(diflong)
	Y = cos(theta1) * sin(theta2) - sin(theta1) * cos(theta2) * cos(diflong)
	beta = atan2(X,Y)
	return beta

def haversine(theta1, lon1, theta2, lon2):
    dlon = lon2 - lon1
    dlat = theta2 - theta1
    a = sin(dlat/2)**2 + cos(theta1) * cos(theta2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth
    return c * r

print(bearings(theta1, lon1, theta2, lon2))
print(haversine(theta1, lon1, theta2, lon2))
