#  License:		                BSD License 
#  PythonTOP default license:   license.txt

import numpy as np
import matplotlib.pyplot as plt
import json


#   14-----------------l13----13---l12--12--------l11--------------11
#   | -                       |          |                   -     |
#   |   -            e2       l17  e3    l18    e5         l16     |
#   |     l15                 |          |               -         |
#   |        -   3-----l3-----4----l19-----7-----l7---8            |
#   l14          |            |           |           |           l10
#   |            |            |           |           |            |
#   |    e1      l2          l4    e4    l6          l8     e6     |
#   |            |            |           |           |            |
#   |            |            |           |           |            |    ^
#   1-----l1-----2           5-----l5-----6           9-----l9-----10   |y
#--> x



class counter_class:
    current_node = 0
    current_element = 0
def _find_node_in_list(list_i,nr_node_i):
    temp_entry = []
    for i in range(len(list_i)):
        if (list_i[i][0] == nr_node_i):
            temp_entry = list_i[i]
    return temp_entry
        

def _plot_all_nodes(line_nodes_array):
    x_plot,y_plot = [],[]
    for i in range(len(line_nodes_array)):
        x_plot_i,y_plot_i = line_nodes_array[i][1],line_nodes_array[i][2]
        x_plot.append(x_plot_i),y_plot.append(y_plot_i)   
    plt.plot(x_plot,y_plot,'X')
def _plot_all_elements(element_list,node_list):
    color_dict = {1:'black',2:'blue',3:'green',4:'red'}
    nr_elements = len(element_list)
    for i in range(nr_elements):
        x_i,y_i = [],[]
        current_element = element_list[i]
        current_mat = current_element[5]
        for k in range(4):
            x_i.append(_find_node_in_list(node_list,current_element[k+1])[1])
            y_i.append(_find_node_in_list(node_list,current_element[k+1])[2])
        x_i.append(_find_node_in_list(node_list,current_element[1])[1])
        y_i.append(_find_node_in_list(node_list,current_element[1])[2])
        plt.plot(x_i,y_i,c=color_dict[current_mat])

def _create_e1(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[0],line_nodes_array[1],line_nodes_array[14],line_nodes_array[13]
    element_edge_nodes = [1,2,3,14]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[len(l4)-1-j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[i-1][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes
def _create_e2(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[2],line_nodes_array[16],line_nodes_array[12],line_nodes_array[14]
    element_edge_nodes = [3,4,13,14]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[len(l3)-1-i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[len(l4)-1-j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[len(l3)-i][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes

def _create_e3(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[18],line_nodes_array[17],line_nodes_array[11],line_nodes_array[16]
    element_edge_nodes = [4,7,12,13]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[len(l3)-1-i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[len(l3)-i][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes
def _create_e4(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[4],line_nodes_array[5],line_nodes_array[18],line_nodes_array[3]
    element_edge_nodes = [5,6,7,4]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[len(l4)-1-j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[i-1][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes
def _create_e5(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[6],line_nodes_array[15],line_nodes_array[10],line_nodes_array[17]
    element_edge_nodes = [7,8,11,12]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[len(l3)-1-i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[len(l3)-i][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes
def _create_e6(line_nodes_array,div_i,counter,mat):
    #####################################
    # -----> e1 (write this in a function later), with mat entry for each part, orientation of edge lines?
    #####################################
    l1,l2,l3,l4 = line_nodes_array[8],line_nodes_array[9],line_nodes_array[15],line_nodes_array[7]
    element_edge_nodes = [9,10,11,8]
    n_elements_x = len(l1)+1
    n_elements_y = len(l2)+1
    n_elements_total = n_elements_x*n_elements_y

    ##mid lines
    mid_line_nodes = []
    for i in range(n_elements_x-1):
        mid_line_nodes.append(_create_Line_Nodes(l1[i],l3[i],div_i,counter))

    len_temp_lines = len(mid_line_nodes)+2
    temp_lines = []

    #create vertical temp lines to create elements easier
    for i in range(len_temp_lines):
        temp_temp_lines = []
        #start and end node
        if (i==0): 
            start_node,end_node = element_edge_nodes[0],element_edge_nodes[3]
            temp_temp_lines.append(start_node)
            for j in range(len(l4)):
                temp_temp_lines.append(l4[len(l4)-1-j][0])
            temp_temp_lines.append(end_node)

        elif (i==len_temp_lines-1):
            start_node,end_node = element_edge_nodes[1],element_edge_nodes[2]
            temp_temp_lines.append(start_node)
            for j in range(len(l2)):
                    temp_temp_lines.append(l2[j][0])
            temp_temp_lines.append(end_node)

        else:
            start_node,end_node = l1[i-1][0],l3[i-1][0]
            temp_temp_lines.append(start_node)
            for j in range(len(mid_line_nodes[i-1])):
                    temp_temp_lines.append(mid_line_nodes[i-1][j][0])
            temp_temp_lines.append(end_node)       
        temp_lines.append(temp_temp_lines)

    elements_i = []
    #create elements
    for i in range(n_elements_x):
        for j in range(n_elements_y):
            counter.current_element = counter.current_element +1
            node_1,node_2 = temp_lines[i][j],temp_lines[i+1][j]
            node_3,node_4 = temp_lines[i+1][j+1],temp_lines[i][j+1]
            elements_i.append([counter.current_element,node_1,node_2,node_3,node_4,mat])

    return elements_i,mid_line_nodes
def _create_Line_Nodes(node1,node2,div,counter):
    dx = node2[1]-node1[1]
    dy = node2[2]-node1[2]
    ddx,ddy = dx/div,dy/div
    line_nodes = []
    for i in range(div):
        if(i!=0):
            counter.current_node = counter.current_node+1
            line_nodes.append([counter.current_node,node1[1]+i*ddx,node1[2]+i*ddy]) 
    return line_nodes
def _assemble_nodes(lines_array):
    total_node_array = []
    for i in range(len(lines_array)):
        current_nr_lines = len(lines_array[i])
        for j in range(current_nr_lines):
            current_nr_nodes = len(lines_array[i][j])
            for k in range(current_nr_nodes):
                total_node_array.append(lines_array[i][j][k])
    return total_node_array
def _assemble_elements(element_array):
    total_element_array = []
    for i in range(len(element_array)):
        current_nr_elements = len(element_array[i])
        for j in range(current_nr_elements):
            total_element_array.append(element_array[i][j])
    return total_element_array
def _export_json_file(element_array,node_array):
    data = {
        'TOP-Version':"WS17/18_v01",
        'Elements' : element_array,
        'Nodes': node_array
    }

    with open('membrane_wall.json', 'w') as f:
        json.dump(data,f)

#start main
counter = counter_class()
div_i = 3    ###<------------------------------------------------------user
#create edge nodes ###<------------------------------------------------user
edge_nodes = [[[1,-3,0],[2,-2,0],[3,2,3],[4,3,3],[5,3,1],[6,4,1],
    [7,4,3],[8,5,3],[9,5,0],[10,7,0],[11,7,5],[12,4,5],[13,3,5],[14,0,5]]]
counter.current_node = len(edge_nodes[0])
#create contour nodes
line_nodes_array = []
for i in range(19):
    a = i
    b = i+1
    if (i==13): a,b = 13,0
    if (i==14): a,b = 13,2
    if (i==15): a,b = 7,10
    if (i==16): a,b = 3,12
    if (i==17): a,b = 6,11
    if (i==18): a,b = 3,6
    line_nodes_array.append(_create_Line_Nodes(edge_nodes[0][a],edge_nodes[0][b],div_i,counter))

#create elements for each part
elements_e1,mid_nodes_e1 = _create_e1(line_nodes_array,div_i,counter,1)
elements_e2,mid_nodes_e2 = _create_e2(line_nodes_array,div_i,counter,1)
elements_e3,mid_nodes_e3 = _create_e3(line_nodes_array,div_i,counter,1)
elements_e4,mid_nodes_e4 = _create_e4(line_nodes_array,div_i,counter,1)
elements_e5,mid_nodes_e5 = _create_e5(line_nodes_array,div_i,counter,1)
elements_e6,mid_nodes_e6 = _create_e6(line_nodes_array,div_i,counter,1)




#assemble total nodes
total_nodes = _assemble_nodes([edge_nodes,line_nodes_array,mid_nodes_e1,mid_nodes_e2,
    mid_nodes_e3,mid_nodes_e4,mid_nodes_e5,mid_nodes_e6])

#assemble total element
total_elements =_assemble_elements([elements_e1,elements_e2,elements_e3,elements_e4,elements_e5,elements_e6])
#export to json file
_export_json_file(total_elements,total_nodes)

#visualize newly created geometry
_plot_all_elements(total_elements,total_nodes)
plt.show()

