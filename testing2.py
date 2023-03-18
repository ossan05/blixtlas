            
def resize()
    blue_stations.clear()
    station_group.empty()
    for i in range(blue_station_amount):
        new_station = Station(xy_blue, "graphics/station1.png")
        station_group.add(new_station)  
        blue_stations.append(xy_blue)      
    for i in range(grey_station_amount):
        new_station = Station(xy_grey, "graphics/station0.png")
        station_group.add(new_station)

def resize():
    for bus in bus_group:
        bus.xy = 