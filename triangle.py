import os
import googlemaps
from itertools import combinations

all_waypoints = [
	["42.777500, -72.423222","Ashuelot Bridge, Winchester"],
	["42.838028, -72.360639","Coombs Bridge, Winchester,"],
	["42.847306, -72.340361","Slate Bridge, Swanzey"],
	["42.871556, -72.327500","West Swanzey Bridge, Swanzey"],
	["42.886889, -72.287389","Sawyer's Crossing, Swanzey"],
	["42.854583, -72.273972","Carleton Bridge, Swanzey"],
	["42.955639, -71.935667","County Bridge, Hancock"],
	["43.192167, -71.748306","Rowell's Bridge, Hopkinton"],
	["43.222778, -71.712667","Railroad Bridge, Hopkinton"],
	["43.276889, -71.811306","Dalton Bridge, Warner"],
	["43.288333, -71.856000","Waterloo Bridge, Warner"],
	["43.264361, -71.952972","Bement Bridge, Bradford"],
	["43.434861, -71.836306","Keniston Bridge, Andover"],
	["43.430417, -71.869389","Cilleyville Bridge, Andover"],
	["43.390972, -72.194611","Corbin Bridge, Newport"],
	["43.170028, -72.345833","Mcdermott Bridge, Langdon"],
	["43.153083, -72.393667","Prentiss Bridge, Langdon"],
	["43.472972, -72.383333","Cornish-Windsor Bridge, Cornish"],
	["43.462750, -72.354222","Blacksmith Shop Bridge, Cornish"],
	["43.464556, -72.369250","Dingleton Hill Bridge, Cornish"],
	["43.517389, -72.374306","Blow-Me-Down Bridge, Cornish"],
	["43.553361, -72.265444","Meriden Bridge, Plainfield"],
	["43.867556, -72.165111","Edgell Bridge, Lyme"],
	["44.154000, -72.035611","Bath-Haverhill Bridge, Bath"],
	["44.166889, -71.965833","Bath Bridge, Bath"],
	["44.134333, -71.950583","Swiftwater Bridge, Bath"],
	["44.460556, -71.653472","Mt.Orne Bridge, Lancaster"],
	["44.460297, -71.653725","Mechanic Street Bridge, Lancaster"],
	["44.595823, -71.511325","Groveton Bridge, Northumberland"],
	["44.852917, -71.551278","Columbia Bridge, Columbia"],
	["45.054750, -71.406833","Pittsburg-Clarksville Bridge, Pittsburg"],
	["45.084278, -71.313389","Happy Corner Bridge, Pittsburg"],
	["45.072222, -71.305972","River Road Bridge, Pittsburg"],
	["44.600722, -71.407917","Stark Bridge, Stark"],
	["44.097278, -71.681139","Sentinel Pine Bridge, Lincoln"],
	["43.810278, -71.666639","Blair Bridge, Campton"],
	["43.853333, -71.657917","Turkey Jim's Bridge, Campton"],
	["43.814722, -71.621361","Bump Bridge, Campton"],
	["43.775667, -71.739694","Smith Bridge, Plymouth"],
	["43.856139, -71.364222","Durgin Bridge, Sandwich"],
	["43.821556, -71.212306","Whittier Bridge, Ossipee"],
	["43.984389, -71.119472", "Swift River Bridge"],
	["43.983250, -71.116417", "Saco River Bridge"],
	["44.005722, -71.241444","Albany Bridge, Albany"],
	["44.094472, -71.203444","Bartlett Bridge, Bartlett"],
	["44.142000, -71.185472","Honeymoon Bridge, Jackson"],
	["43.360167, -72.245722","Pier Bridge, Newport"],
	["43.358528, -72.253778","Wright's Bridge, Newport"],
	["43.445333, -71.643444","Sulphite Bridge, Franklin"],
	["43.177583, -71.822056","Heniker Bridge, Heniker"],
	["44.049528, -71.687472","Clark's Bridge, North Woodstock"],
	["43.718333, -71.618250","Squam Bridge, Ashland"],
	["43.639056, -72.222167","Packard Hill Bridge, Lebanon"]
]

num_waypoints = len (all_waypoints)

googlemaps_api_key = os.environ['GOOGLE_MAPS_API']

gmaps = googlemaps.Client(key=googlemaps_api_key)

waypoint_distances = {}
waypoint_durations = {}

for num, waypointPair1 in enumerate(all_waypoints, start=1):
    for num2, waypointPair2 in enumerate(all_waypoints, start=1):
        if ((num != num2) & ( num2 > num )) :

            waypoint1 = waypointPair1[0]
            waypoint2 = waypointPair2[0]

            try:
                route = gmaps.distance_matrix(origins=[waypoint1],
                                            destinations=[waypoint2],
                                            mode="driving",  # Change this to \"Walking" for walking directions,
                                                            # "bicycling" for biking directions, etc.
                                            language="English",
                                            units="metric")

                # "distance" is in meters
                distance = route["rows"][0]["elements"][0]["distance"]["value"]

                # "duration" is in seconds
                duration = route["rows"][0]["elements"][0]["duration"]["value"]

                waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
                waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

            except Exception as e:
                print("Error with finding the route between %s and %s. %s" % (waypoint1, waypoint2, e))


# write out the triangle matrix
with open("my-triangle-dist-dur.py", "w") as out_file:
    out_file.write("dists = [\n")

    for num3, waypointPair1 in enumerate(all_waypoints, start=1):
        if (num3 != (num_waypoints - 0)):
            out_file.write("\t[")

        for num4, waypointPair2 in enumerate(all_waypoints, start=1):

            waypoint1 = waypointPair1[0]
            waypoint2 = waypointPair2[0]

            if ( (num3 != num4) & ( num4 > num3 ) ) :
                out_file.write(str(waypoint_distances[frozenset([waypoint1, waypoint2])]))
                if num4 < num_waypoints:
                    out_file.write(", ")

        if (num3 != (num_waypoints - 0)):
            out_file.write("]")
        if num3 < (num_waypoints - 1):
            out_file.write(",")
            out_file.write("\n")
    out_file.write("\n]\n")

    # write out the places array
    out_file.write("\n\nplaces = [\n")
    for num5, waypointPair in enumerate(all_waypoints, start=1):
        out_file.write("\"" + waypointPair[1] + "\", ",)
    out_file.write("\n]\n")

# write out Dr. Olsens format
with open("my-waypoints-dist-dur.tsv", "w") as out_file:
    out_file.write("\t".join(["waypoint1",
                              "waypoint2",
                              "distance_m",
                              "duration_s"]))
    
    for (waypoint1, waypoint2) in waypoint_distances.keys():
        out_file.write("\n" +
                       "\t".join([waypoint1,
                                  waypoint2,
                                  str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                  str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))
                                  
                          