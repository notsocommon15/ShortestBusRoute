"""Simple travelling salesman problem between cities."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import tkinter

bldgnames=[]

def create_data_model():
    """Stores the data for the problem."""
    #n=int(input("Enter number of buildings: "))
    global bldgnames
    global n
    global e1
    global master
    global master1
    global master2
    global master3
    global a
    global i
    global j
    global bn
    a=[]

    master=tkinter.Tk()
    tkinter.Label(master, text='Number of Bldgs:').grid(row=0) 
    #tkinter.Label(master, text='Last Name').grid(row=1) 
    e1 = tkinter.Entry(master) 
    #e2 = tkinter.Entry(master) 
    e1.grid(row=0, column=1) 
    #e2.grid(row=1, column=1)
    #tkinter.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tkinter.W, pady=4)
    tkinter.Button(master, text='Next', command=show_entry_fields).grid(row=3, column=1, sticky=tkinter.W, pady=4)
    master.mainloop()

    for i in range(n):
        c=[]
        for j in range(n):
            c.append(9999)
        a.append(c)
            

    for i in range(n):
        master1=tkinter.Tk()
        tkinter.Label(master1, text='Name of Bldg'+str(i+1)+':').grid(row=0)
        e1 = tkinter.Entry(master1)
        e1.grid(row=0, column=1)
        tkinter.Button(master1, text='Next', command=names).grid(row=3, column=1, sticky=tkinter.W, pady=4)
        #bldgnames.append(input("Enter name of bldg "+str(i+1)+":"))
        master1.mainloop()
        #master1.destroy()

    #print(bldgnames)

    for i in range(n):
        for j in range(i,n):
            if (i==j):
                a[i][j]=0;
            else:
                master2=tkinter.Tk()
                tkinter.Label(master2, text="Enter distance between building "+bldgnames[i]+ " & building "+bldgnames[j]+" : ").grid(row=0)
                e1 = tkinter.Entry(master2)
                e1.grid(row=0, column=1)
                tkinter.Button(master2, text='Next', command=dist).grid(row=3, column=1, sticky=tkinter.W, pady=4)
                master2.mainloop()
                #master1.destroy()
                
                #int(input())
                #a[j][i]=a[i][j]
    
            
            
    data = {}
    data['distance_matrix'] = a# yapf: disable
    #data['distance_matrix'].append()
    data['num_vehicles'] = int(1)



    master3=tkinter.Tk()
    tkinter.Label(master3, text="Type the starting block: ").grid(row=0) 
    #tkinter.Label(master, text='Last Name').grid(row=1) 
    e1 = tkinter.Entry(master3) 
    #e2 = tkinter.Entry(master) 
    e1.grid(row=0, column=1) 
    #e2.grid(row=1, column=1)
    #tkinter.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tkinter.W, pady=4)
    tkinter.Button(master3, text='Next', command=start).grid(row=3, column=1, sticky=tkinter.W, pady=4)
    master3.mainloop()

    
    #bn=input()
    b=9999
    for i in range(n):
        if (bn==bldgnames[i]):
            b=i
            break
    if b==9999:
        print("Incorrect starting block. Please try again.")
    #print(b)
    
    data['depot'] = int(b)
    #print(data['distance_matrix'])
    return data


def print_solution(manager, routing, assignment):
    global bldgnames
    """Prints assignment on console."""
    #print('Objective: {} miles'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    s=plan_output.split()
    #print (s)
    f=0
    w=""
    for i in s:
        if i.isdigit():
            if f!=0:
                w=w+("->")
            w=w+(bldgnames[int(i)])
            f=1


    master5=tkinter.Tk()
    tkinter.Label(master5, text='Objective [Shortest path possible] : '+str(assignment.ObjectiveValue())+" Miles").grid(row=0)
    tkinter.Label(master5, text='Path to be followed: '+w).grid(row=2) 
            
    plan_output += 'Route distance: {}miles\n'.format(route_distance)


def show_entry_fields():
    global n
    global e1
    global master
    n=int(e1.get())
    master.destroy()

def start():
    global e1
    global master3
    global bn
    x=str(e1.get())
    bn=x
    master3.destroy()

def names():
    global e1
    global string
    global bldgnames
    global master1

    string=str(e1.get())
    bldgnames.append(string)
    #print ("names")
    #print(string)
    master1.destroy()
    #mlabel=tkinter.Label(master, text=" Entered Successfully!").pack()

def dist():
    global e1
    global a
    global master2
    global i
    global j

    string=int(e1.get())
    a[i][j]=string
    a[j][i]=a[i][j]
    master2.destroy()

def main():

    global e1
    global n  


    
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        print_solution(manager, routing, assignment)

    
if __name__ == '__main__':
    main()
