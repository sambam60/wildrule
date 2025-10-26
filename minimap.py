from map import rooms
Direction_Movements = {
    "north":(0,1),
    "south":(0,-1),
    "east":(1,0),
    "west":(-1,0)
}

def generate_layout(start="Starter"):
    layout = {start:(0,0)} #start the map at 0,0

    Unvisited = [start] # creates a list of any unvisited rooms

    while len(Unvisited) >0: #while there are unchecked rooms
        room_name = Unvisited.pop(0) #takes first room from list and removes it

        x,y = layout[room_name] # gets the coordinates of current room

        room = rooms[room_name] #gets the data about the room from the rooms dictionary

        exits = room["exits"]

        for direction in exits:
            next_room = exits[direction]
            direction = direction.lower() #normalises the direction name

            if direction not in Direction_Movements: # only allows north east south and west
                continue
            dx,dy = Direction_Movements[direction] #gets the change in coordinates

            New_Coordinates = (x + dx, y + dy) # calculates the coordinates of the next room

            if next_room not in layout: #if the next room isnt mapped
                layout[next_room] = New_Coordinates # saves its position in the layout

                Unvisited.append(next_room) # then adds to list of unvisited rooms
    return layout #once all rooms have been visited returns full dictionary of rooms
def draw_minimap(current_room):
    layout = generate_layout() # gets the layoutof the map you want to draw
    xs = []  # all x coordinates
    ys = []  # all y coordinates
    for coords in layout.values(): # for every coordinate in the map layout
        x = coords[0]   #x coordinate is first number
        y = coords[1]   #y coordinate is the second number
        xs.append(x)    #add teh x to list of all x values
        ys.append(y)    #add the y to list of all y values
    min_x,max_x = min(xs),max(xs) # gets the minimum and maximum x and y values and stores the as variables
    min_y,max_y = min(ys),max(ys)
    for y in range(max_y,min_y-1,-1): # for each value of y going bacwards otherwise the map would be upside down
        line = ""
        for x in range(min_x,max_x+1):# goes left  to write through x values
            room = None
            for name in layout: #for each room name in the map layout
                coords = layout[name]   # get the rooms coordinates
                rx, ry = coords # then splits them into rx and ry
                if (rx,ry)==(x,y):# if the rooms coordinates match the current position
                    room = name
                    break   # stops looking for rooms
            if room: # if there is a room (not none)
                room_reference = rooms.get(room) # gets the reference of the room's properties
                if room_reference == current_room: #if the room is the same as current room
                    line += "[X] " # sets x in box for current room
                elif room_reference["explored"] == True: # checks if room has already been visited by the player before
                    match room_reference["area"]: # sets letter in box based on room area type
                        case "Forest":
                            line += "[F] "
                        case "Tundra":
                            line += "[T] "
                        case "Plains":
                            line += "[P] "
                        case "Village":
                            line += "[V] "
                else:# if not
                    line +="[?] " # sets ? in box for unexplored rooms
            else: # if no room
                line += "    "# sets as blank space
        print(line)

# When calling these functions, the map prints "None" on the last line. I don't know why this is happening. -Muhammad
# If Ed can review this function and figure out what's going on, that would be nice :)
