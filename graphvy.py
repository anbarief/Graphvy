import random
import math
import copy
import numpy

from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.properties import ListProperty
from kivy.clock import Clock

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

wsize = Window.size
Window.clearcolor = (180/255, 180/255, 180/255, 0.9)
node_info = "Name: {}, Value: {}, Degree: {}, ID: {}"
font_file = 'Sofia-Regular.otf'


def animation_path():
    dx = 2
    bound = 5
    n = int(bound/dx)
    path = [(0,0)]
    
    for i in range(n):
        x_new, y_new = dx, 0
        path.append((x_new, y_new))

    for i in range(n):
        x_new, y_new = - dx, 0
        path.append((x_new, y_new))

    for i in range(n):
        x_new, y_new = - dx, 0
        path.append((x_new, y_new))

    for i in range(n):
        x_new, y_new = dx, 0
        path.append((x_new, y_new))

    return path

def valid_coordinate(text):
    numbers_condition = "0123456789.-"
    confirm = 1
    for i in range(len(text)):
        if not (text[i] in numbers_condition):
            confirm = 0
            break

    if ('-' in text[1:]):
        confirm = 0

    if text.count('.') > 1:
        confirm = 0

    if text == "" or text == "." or text == "-" or text == "-.":
        confirm = 0

    if confirm == 1:
        return True
    else:
        return False


class MainScreen(FloatLayout):

    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.axis = Axis()
        self.add_widget(self.axis)
        self.axis.size_hint = (1, 1)

        self.coordinates = Coordinates(self)

        self.buttons = []
             
        self.reset_button = Button(text = "Reset", font_size = 10, font_name = font_file)
        self.add_widget(self.reset_button)
        self.reset_button.size_hint = (0.1, 0.1)
        self.reset_button.halign = "center"
        self.reset_button.bind(on_release = self.reset)
        self.buttons.append(self.reset_button)

        self.node_button = Button(text = "Add Node", font_size = 10, font_name = font_file)
        self.add_widget(self.node_button)
        self.node_button.size_hint = (0.1, 0.1)
        self.node_button.pos_hint = {'x':0.1, 'y':0}
        self.node_button.halign = "center"
        self.node_button.bind(on_release = self.axis.add_node)
        self.buttons.append(self.node_button)

        self.connect_button = Button(text = "Connect Nodes", font_size = 10, font_name = font_file)
        self.add_widget(self.connect_button)
        self.connect_button.size_hint = (0.1, 0.1)
        self.connect_button.pos_hint = {'x':0.2, 'y':0}
        self.connect_button.halign = "center"
        self.connect_button.bind(on_release = self.axis.connect_nodes)
        self.buttons.append(self.connect_button)

        self.map_button = Button(text = "Show\nNodes Map", font_size = 10, font_name = font_file)
        self.add_widget(self.map_button)
        self.map_button.size_hint = (0.1, 0.1)
        self.map_button.pos_hint = {'x':0, 'y': 0.1}
        self.map_button.halign = "center"
        self.map_button.bind(on_release = self.axis.show_map)
        self.buttons.append(self.map_button)

        self.map = Map()
        self.add_widget(self.map)
        self.map.pos_hint = {'x':0, 'y':0.1}

        self.edit_button = Button(text = "Edit Node", font_size = 10, font_name = font_file)
        self.add_widget(self.edit_button)
        self.edit_button.size_hint = (0.1, 0.1)
        self.edit_button.pos_hint = {'x':0.3, 'y':0}
        self.edit_button.halign = "center"
        self.edit_button.bind(on_release = self.axis.edit_node)
        self.buttons.append(self.edit_button)

        self.edit_text = TextInput(font_size = 10)
        self.add_widget(self.edit_text)
        self.edit_text.size_hint = (0.2, 0.05)
        self.edit_text.pos_hint = {'x':0.3, 'y':0.1}
        self.edit_text.halign = "center"
        self.edit_text.bind(text = self.axis.on_edit_text)
        self.edit_text.background_color = [0, 0, 0, 0]
        self.edit_text.disabled = True

        self.info_label = TextInput(text = "Info: ", font_size = 10)
        self.add_widget(self.info_label)
        self.info_label.size_hint = (0.5, 0.1)
        self.info_label.pos_hint = {'x': 0.5, 'y': 0}
        self.info_label.halign = "left"
        self.info_label.valign = "top"
        self.info_label.text_size = [0.5*wsize[0], 0.1*wsize[1]] 
        self.info_label.disabled = True

        self.connected_subgraph_button = Button(text = "Connected\nSubgraph", font_size = 10, halign = 'center', valign = 'center', font_name = font_file)
        self.add_widget(self.connected_subgraph_button)
        self.connected_subgraph_button.size_hint = (0.1, 0.1)
        self.connected_subgraph_button.pos_hint = {'x':0.9, 'y': 0.1}
        self.connected_subgraph_button.halign = "center"
        self.connected_subgraph_button.bind(on_release = self.axis.connected_subgraph)
        self.buttons.append(self.connected_subgraph_button)

        self.import_data_button = Button(text = "Import Data", font_size = 10, font_name = font_file)
        self.add_widget(self.import_data_button)
        self.import_data_button.size_hint = (0.1, 0.1)
        self.import_data_button.pos_hint = {'x':0.9, 'y': 0.2}
        self.import_data_button.halign = "center"
        self.import_data_button.bind(on_release = self.axis.import_data)
        self.buttons.append(self.import_data_button)

        self.generate_plot_button = Button(text = "Generate Plot", font_size = 10, font_name = font_file)
        self.add_widget(self.generate_plot_button)
        self.generate_plot_button.size_hint = (0.1, 0.1)
        self.generate_plot_button.pos_hint = {'x':0.9, 'y': 0.3}
        self.generate_plot_button.halign = "center"
        self.generate_plot_button.bind(on_release = self.axis.gen_plot)
        self.buttons.append(self.generate_plot_button)

        self.goto_button = Button(text = "Go To Point", font_size = 10, font_name = font_file)
        self.add_widget(self.goto_button)
        self.goto_button.size_hint = (0.1, 0.1)
        self.goto_button.pos_hint = {'x':0, 'y': 0.2}
        self.goto_button.halign = "center"
        self.goto_button.bind(on_release = self.axis.goto)

        self.goto_box = TextInput(text = "x, y", font_size = 10)
        self.add_widget(self.goto_box)
        self.goto_box.size_hint = (0.1, 0.075)
        self.goto_box.pos_hint = {'x':0, 'y':0.3}
        self.goto_box.halign = "center"

    def reset(self, obj):
        self.clear_widgets(self.children)
        self.canvas.clear()
        self.start()

        
class Coordinates:

    def __init__(self, parent):
        self.parent = parent
        self.x = [0, 800]
        self.y = [0, 600]
        self.create_ticks()

    def create_ticks(self):
        self.top_left_tick = Label(text = "({}, {})".format(self.x[0], self.y[1]), font_size = 12, halign = "left", color = (0, 0, 0, 1))
        self.parent.add_widget(self.top_left_tick)
        self.top_left_tick.size_hint = (0.05, 0.05)
        self.top_left_tick.pos_hint = {'x': 0.05, 'y': 0.95}
        self.top_right_tick = Label(text = "({}, {})".format(self.x[1], self.y[1]), font_size = 12, halign = "right", color = (0, 0, 0, 1))
        self.parent.add_widget(self.top_right_tick)
        self.top_right_tick.size_hint = (0.05, 0.05)
        self.top_right_tick.pos_hint = {'x': 1-0.1, 'y': 0.95}
        
    def update_ticks(self):
        self.top_left_tick.text = "({}, {})".format(round(self.x[0], 2), round(self.y[1],2))
        self.top_right_tick.text = "({}, {})".format(round(self.x[1], 2), round(self.y[1],2))


class Map(Widget):

    def __init__(self):
        super().__init__()
        self.pos = [0.1*wsize[0], 0.1*wsize[1]]
        self.size = [240, 240]
        self.map_x = [0.1*wsize[0], 0.1*wsize[0] + 240]
        self.map_y = [0.1*wsize[1], 0.1*wsize[1] + 240]

    def apply_visual(self):
        self.graph = root.axis.graph
        self.rectangle = Rectangle(pos = [0.1*wsize[0], 0.1*wsize[1]], size = [240, 240])
        self.bg_color = Color(0,0,0,0.7)
        self.canvas.add(self.bg_color)
        self.canvas.add(self.rectangle)
        if len(self.graph.nodes) > 0:      
            self.nodes_x_min, self.nodes_x_max = self.graph.nodes_xmin, self.graph.nodes_xmax 
            self.nodes_y_min, self.nodes_y_max = self.graph.nodes_ymin, self.graph.nodes_ymax

            self.dx = self.nodes_x_max-self.nodes_x_min
            self.dy = self.nodes_y_max-self.nodes_y_min

            self.norm_dim = max([self.dx, self.dy])
            if abs(self.norm_dim) < 0.00001:
                self.norm_dim = 0.00001
            self.ratio = 238/self.norm_dim
            self.marker_size = 4
            
            color = Color(0,1,1,0.8)
            self.canvas.add(color)
            for i in self.graph.nodes:
                x = (i.coordinates[0] - self.nodes_x_min)*self.ratio
                y = (i.coordinates[1] - self.nodes_y_min)*self.ratio
                pos = [1 + self.map_x[0] + x - 0.5*self.marker_size, 1 + self.map_y[0] + y - 0.5*self.marker_size]
                marker = Ellipse(pos = pos, size = [self.marker_size, self.marker_size])
                self.canvas.add(marker)
                
            self.map_info = TextInput(font_size = 10)
            self.map_info.text = "nodes range: x=[{}, {}], y=[{}, {}]".format(round(self.nodes_x_min, 2), round(self.nodes_x_max, 2), round(self.nodes_y_min, 2), round(self.nodes_y_max, 2))
            self.map_info.disabled = True
            root.add_widget(self.map_info)
            self.map_info.size_hint = (240/wsize[0], 0.075)
            self.map_info.pos_hint = {'x': 0.1, 'y': 0.1 + 240/wsize[1]}        
            
    def clear_visual(self):
        self.canvas.clear()
        if 'map_info' in dir(self):
            root.remove_widget(self.map_info)
        
     
class Node(Button):
    
    widget_pos = ListProperty()
    widget_size = ListProperty()
    node_center = ListProperty()

    def __init__(self, value, text, center, color):
        super().__init__()
        xo, yo = root.coordinates.x[0], root.coordinates.y[0]
        self.value = value
        self.coordinates = center
        self.visual_text = text
        self.visual_color = color
        self.r = 12.5
        self.background_color = (0, 0, 0, 0)
        self.pos = [center[0]-self.r-xo, center[1]-self.r-yo]
        self.size = (2*self.r, 2*self.r)

        self.visual_widget = Widget()
        self.add_widget(self.visual_widget)
        self.visual_widget.pos = self.pos
        self.visual_widget.size = self.size

        self.apply_visual(source = "circle2_normal.png", color = self.visual_color)

        self.edges = []
        self.neighbor = []
        self.press_count = -1
        
        self.widget_pos = self.pos
        self.widget_size = self.size
        self.node_center = [center[0] - xo, center[1] - yo]

        self.anim_path = []
        
    def animate(self, dt):
        if len(self.anim_path) != 0:
            self.node_center = [self.node_center[0] + self.anim_path[0][0], \
                                self.node_center[1] + self.anim_path[0][1]]
            self.anim_path.pop(0)
            for i in self.edges:
                i.update_line()
        else:
            Clock.unschedule(self.anim_scheduled)
        
    def apply_visual(self, source = "circle2_normal.png", color = (202/255,204/255,206/255,1)):
        self.visual_color = color
        col = Color(*color)
        self.visual_widget.canvas.add(col)
        circle_pos = [0, 0]
        self.circle_graphics = Ellipse(pos = circle_pos, size = [2*0.95*self.r, 2*0.95*self.r])
        self.visual_widget.canvas.add(self.circle_graphics)
        self.node_img = Image(source = source)
        self.visual_widget.add_widget(self.node_img)
        self.node_img.pos = self.pos
        self.node_img.size = [2*self.r, 2*self.r]
        self.node_text = Label(text = self.visual_text, font_size = 15, font_name = 'DejaVuSans')
        self.node_text.color = (1, 1, 1, 0.2)
        self.visual_widget.add_widget(self.node_text)
        self.node_text.pos = self.pos
        self.node_text.size = self.size

    def update_visual(self, source, color):
        self.clear_visual()
        self.apply_visual(source, color)

    def clear_visual(self):
        self.visual_widget.canvas.clear()
        self.visual_widget.remove_widget(self.node_img)
        self.visual_widget.remove_widget(self.node_text)

    def on_node_center(self, obj, value):
        self.pos = [value[0]-self.r, value[1]-self.r]
        self.widget_pos = self.pos
        self.circle_graphics.pos = [self.pos[0] + 0.05*self.r, self.pos[1] + 0.05*self.r]

    def on_widget_pos(self, obj, value):
        self.pos = value
        self.node_img.pos = value
        self.node_text.pos = value

    def on_widget_size(self, obj, value):
        self.size = value
        self.r = 0.5*self.size[0]
        self.node_text.size = value

    @property
    def degree(self):
        return len(self.edges)

    def add_edge(self, edge):
        self.edges.append(edge)

    def connect_node(self, node):
        connected = root.axis.graph.connected_by_normal_edge([self, node])
        if not connected:
            nodes = [self, node]
            line = Line(points = [nodes[0].center[0], nodes[0].center[1], \
                                  nodes[1].center[0], nodes[1].center[1]], \
                        width = root.axis.graph.visual_size['lw'])
            color = Color(0/255,150/255, 255/255, 0.5)
            root.axis.edge_drawer.canvas.add(color)
            root.axis.edge_drawer.canvas.add(line)

            edge_obj = NormalEdge(nodes, line, (0/255,150/255, 255/255, 0.5))
            nodes[0].add_edge(edge_obj)
            nodes[0].neighbor.append(nodes[1])
            nodes[1].add_edge(edge_obj)
            nodes[1].neighbor.append(nodes[0])
        else:
            pass
         
    def on_press(self):
        super().on_press()

        self.press_count *= -1
        if self.press_count == 1:
            self.background_color = (0, 0.8, 0.9, 0.5)
            self.node_text.color = (1, 1, 1, 1)
            
            for i in root.axis.graph.nodes:
                if i != self:
                    i.press_count = -1
                    i.background_color = (0, 0, 0, 0)
                    i.node_text.color = (1, 1, 1, 0.2)

            root.info_label.text = "Info: " + node_info.format(self.node_text.text, self.value, self.degree, self)

            if len(self.anim_path) == 0:    
                self.anim_path = animation_path()
                self.anim_scheduled = Clock.schedule_interval(self.animate, 1/60)
            
            if root.axis.connect_nodes_option == 1:

                if len(self.parent.a_to_b) < 2:
                    self.parent.a_to_b.append(self)

                if len(self.parent.a_to_b) == 2:

                    make_edge = not root.axis.graph.connected_by_normal_edge(self.parent.a_to_b)
                    if not make_edge:
                        self.parent.a_to_b.pop()
                        root.info_label.text = "Info: " + "THESE NODES ARE ALREADY CONNECTED!"
                        self.press_count = -1
                        self.background_color = (0, 0, 0, 0)
                        self.node_text.color = (1, 1, 1, 0.2)

                    else:
                        nodes = self.parent.a_to_b
    
                        line = Line(points = [nodes[0].center[0], nodes[0].center[1], \
                                              nodes[1].center[0], nodes[1].center[1]], \
                                              width = root.axis.graph.visual_size['lw'])
                        color = Color(0/255,150/255, 255/255, 0.5)
                        root.axis.edge_drawer.canvas.add(color)
                        root.axis.edge_drawer.canvas.add(line)

                        edge_obj = NormalEdge(nodes, line, (0/255,150/255, 255/255, 0.5))
                        nodes[0].add_edge(edge_obj)
                        nodes[0].neighbor.append(nodes[1])
                        nodes[1].add_edge(edge_obj)
                        nodes[1].neighbor.append(nodes[0])

                        for i in nodes:
                            i.press_count = -1
                            i.background_color = (0, 0, 0, 0)
                            i.node_text.color = (1, 1, 1, 0.2)

                        self.parent.a_to_b = []

            elif self.parent.connected_subgraph_option == 1:

                if len(self.edges) > 0:
                    prev_subgraph = root.axis.graph.previous_selected_subgraph
                    self.press_count = -1
                    self.background_color = (0, 0, 0, 0)
                    self.node_text.color = (1, 1, 1, 0.2)

                    if prev_subgraph != None:
                        for i in prev_subgraph.nodes:
                            i.background_color = (0, 0, 0, 0)
                            i.node_text.color = (1, 1, 1, 0.2)
                        if (not self in prev_subgraph.nodes):
                            subgraph = root.axis.graph.find_subgraph(self.edges[0])
                            for i in subgraph.nodes:
                                i.background_color = (0, 0.8, 0.9, 0.5)
                                i.node_text.color = (1, 1, 1, 1)
                            root.axis.graph.previous_selected_subgraph = subgraph
                        else:
                            root.axis.graph.previous_selected_subgraph = None
                    else:
                        subgraph = root.axis.graph.find_subgraph(self.edges[0])
                        for i in subgraph.nodes:
                            i.background_color = (0, 0.8, 0.9, 0.5)
                            i.node_text.color = (1, 1, 1, 1)
                        root.axis.graph.previous_selected_subgraph = subgraph
                else:
                    self.press_count = -1
                    self.background_color = (0, 0, 0, 0)
                    self.node_text.color = (1, 1, 1, 0.2)

            elif self.parent.edit_node_option == 1:
                root.edit_text.text = self.visual_text

        else:
            self.background_color = (0, 0, 0, 0)
            self.node_text.color = (1, 1, 1, 0.2)
            if self.parent.connect_nodes_option == 1:
                if self.parent.a_to_b != []:
                    self.parent.a_to_b.pop()


class NormalEdge:

    def __init__(self, nodes, line, color):
        self.nodes = nodes
        self.line = line
        self.line_coordinates = [self.nodes[0].coordinates[0], self.nodes[0].coordinates[1], \
                                 self.nodes[1].coordinates[0], self.nodes[1].coordinates[1]]
        self.color = color

    def update_line(self):
        self.line.points = [self.nodes[0].center[0], self.nodes[0].center[1], \
                            self.nodes[1].center[0], self.nodes[1].center[1]]
        

class Graph(Widget):

    nodes = ListProperty()

    def __init__(self, nodes = None, name = "", container = None):
        super().__init__()
        if nodes == None:
            self.nodes = []
        else:
            self.nodes = [i for i in nodes]
        self.name = name
        self.connected_subgraphs = []
        self.previous_selected_subgraph = None
        self.visual_size = {'lw': 1.5}
        self.container = container

    def connected_by_normal_edge(self, nodes):
        combined = nodes[0].edges + nodes[1].edges
        if len(set(combined)) == len(combined):
            return False
        else:
            return True

    def on_nodes(self, obj, value):
        if 'container' in dir(self):
            if (self.container.map_option == 1):
                root.map.clear_visual()
                root.map.apply_visual()

    @property
    def nodes_xmin(self):
        return min([i.coordinates[0] for i in self.nodes])

    @property
    def nodes_xmax(self):
        return max([i.coordinates[0] for i in self.nodes])

    @property
    def nodes_ymin(self):
        return min([i.coordinates[1] for i in self.nodes])

    @property
    def nodes_ymax(self):
        return max([i.coordinates[1] for i in self.nodes]) 

    @property
    def edges(self):
        x = []
        for i in self.nodes:
            x = x + i.edges
        return list(set(x))

    def find_subgraph(self, start_edge):
        edges = [i for i in self.edges]
        subgraph = Graph(nodes = start_edge.nodes, container = root.axis)

        n = None
        while len(edges) != n:
            n = len(edges)
            to_be_removed = []
            for edge in edges:
                for j in edge.nodes:
                    if j in subgraph.nodes:
                        new_nodes = [k for k in edge.nodes if k not in subgraph.nodes]
                        subgraph.nodes = subgraph.nodes + new_nodes
                        to_be_removed.append(edge)
                        break
            for i in to_be_removed:
                edges.remove(i)

        return subgraph

        
class Axis(Widget):

    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.add_node_option = -1
        self.connect_nodes_option = -1
        self.edit_node_option = -1
        self.connected_subgraph_option = -1
        self.map_option = -1
         
        self.a_to_b = []
        self.graph = Graph(container = self)

        self.edge_drawer = Widget()
        self.add_widget(self.edge_drawer)
    
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        x = touch.x; y = touch.y

        axis = True
        for i in self.graph.nodes:
            if i.collide_point(x, y):
                axis = False
                break

        if axis:
            self.touch_list = [(x, y)]
            xo, yo = root.coordinates.x[0], root.coordinates.y[0]
            if self.add_node_option == 1:
                node = Node(None, str(len(self.children)-1), [xo + x, yo + y], \
                            color = (202/255,204/255,206/255,0.9))
                self.add_widget(node)
                self.graph.nodes.append(node)
            
    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        x = touch.x; y = touch.y

        axis = True
        for i in self.graph.nodes:
            if i.collide_point(x, y):
                axis = False
                break

        if axis and (1 not in [self.add_node_option]):
            delta_pos = (x - self.touch_list[-1][0], y - self.touch_list[-1][1])
            for i in self.graph.nodes:
                i.node_center = (i.node_center[0] + delta_pos[0], i.node_center[1] + delta_pos[1])
            for e in self.graph.edges:
                e.update_line()  
            self.touch_list.append((x, y))
            root.coordinates.x = [root.coordinates.x[0] - delta_pos[0], root.coordinates.x[1] - delta_pos[0]]
            root.coordinates.y = [root.coordinates.y[0] - delta_pos[1], root.coordinates.y[1] - delta_pos[1]]
            root.coordinates.update_ticks()
         
    def add_node(self, obj):
        self.add_node_option *= -1

        for i in self.graph.nodes:
                i.press_count = -1
                i.background_color = (0, 0, 0, 0)
                i.node_text.color = (1, 1, 1, 0.2)

        if self.add_node_option == 1:
            obj.text = "Stop" 
            self.parent.reset_button.disabled = True
            self.parent.connect_button.disabled = True
            self.parent.connected_subgraph_button.disabled = True
            self.parent.edit_button.disabled = True
        else:
            obj.text = "Add Node"
            self.parent.reset_button.disabled = False
            self.parent.connect_button.disabled = False
            self.parent.connected_subgraph_button.disabled = False
            self.parent.edit_button.disabled = False

    def connect_nodes(self, obj):
        self.connect_nodes_option *= -1

        for i in self.graph.nodes:
            i.press_count = -1
            i.background_color = (0, 0, 0, 0)
            i.node_text.color = (1, 1, 1, 0.2)

        if self.connect_nodes_option == 1:    
            obj.text = "Stop" 
            self.parent.reset_button.disabled = True
            self.parent.node_button.disabled = True
            self.parent.connected_subgraph_button.disabled = True
            self.parent.edit_button.disabled = True
        else:
            obj.text = "Connect Nodes"
            self.parent.reset_button.disabled = False
            self.parent.node_button.disabled = False
            self.parent.connected_subgraph_button.disabled = False
            self.parent.edit_button.disabled = False
            self.a_to_b = []

    def edit_node(self, obj):
        self.edit_node_option *= -1

        for i in self.graph.nodes:
            i.press_count = -1
            i.background_color = (0, 0, 0, 0)
            i.node_text.color = (1, 1, 1, 0.2)

        if self.edit_node_option == 1:    
            obj.text = "Stop"
            self.parent.edit_text.background_color = [1, 1, 1, 1]
            self.parent.edit_text.disabled = False
            self.parent.reset_button.disabled = True
            self.parent.node_button.disabled = True
            self.parent.connect_button.disabled = True
            self.parent.connected_subgraph_button.disabled = True
        else:
            obj.text = "Edit Node"
            self.parent.edit_text.background_color = [0, 0, 0, 0]
            self.parent.edit_text.disabled = True
            self.parent.edit_text.text = ""
            self.parent.reset_button.disabled = False
            self.parent.node_button.disabled = False
            self.parent.connect_button.disabled = False
            self.parent.connected_subgraph_button.disabled = False
            self.a_to_b = []

    def on_edit_text(self, obj, value):
        for i in self.graph.nodes:
            if i.press_count == 1:
                i.node_text.text = value
                i.visual_text = value

    def connected_subgraph(self, obj):
        self.connected_subgraph_option *= -1
        for i in self.graph.nodes:
            i.press_count = -1
            i.background_color = (0, 0, 0, 0)
            i.node_text.color = (1, 1, 1, 0.2)
        if self.connected_subgraph_option == 1:    
            obj.text = "Stop" 
            self.parent.reset_button.disabled = True
            self.parent.node_button.disabled = True
            self.parent.connect_button.disabled = True
            self.parent.edit_button.disabled = True
        else:
            obj.text = "Connected\nSubgraph"
            self.parent.reset_button.disabled = False
            self.parent.node_button.disabled = False
            self.parent.connect_button.disabled = False
            self.parent.edit_button.disabled = False

    def import_data(self, obj):
        dataset = list(numpy.load("data.npy"))
        nodes = []
        for i in dataset:
            x = random.uniform(0, 2*800)
            y = random.uniform(0, 2*600)
            node = Node(None, i['name'], [x, y], \
                            color = (202/255,204/255,206/255,0.9))
            self.graph.nodes.append(node)
            self.add_widget(node)
            nodes.append((node, i['neighbor']))
        for node in nodes:
            neighbors = [i for i in nodes if i[0].visual_text in node[1]]
            for i in neighbors:
                node[0].connect_node(i[0])

    def show_map(self, obj):
        self.map_option *= -1

        if self.map_option == 1:    
            obj.text = "Close\nNodes Map" 
            root.map.apply_visual()
        else:
            obj.text = "Show\nNodes Map"
            root.map.clear_visual()

    def goto(self, obj):
        x, y = 400, 300
        text = root.goto_box.text.replace(' ', '')
        des_text = text.split(',')
        if len(des_text) == 2:
            if valid_coordinate(des_text[0]) and valid_coordinate(des_text[1]): 
                x_des, y_des = float(des_text[0]) - root.coordinates.x[0], \
                           float(des_text[1]) - root.coordinates.y[0]
                delta_pos = (x - x_des, y - y_des)
                for i in self.graph.nodes:
                    i.node_center = (i.node_center[0] + delta_pos[0], i.node_center[1] + delta_pos[1])
                for e in self.graph.edges:
                    e.update_line()
                root.coordinates.x = [root.coordinates.x[0] - delta_pos[0], root.coordinates.x[1] - delta_pos[0]]
                root.coordinates.y = [root.coordinates.y[0] - delta_pos[1], root.coordinates.y[1] - delta_pos[1]]
                root.coordinates.update_ticks()
            else:
                root.goto_box.text = "Invalid coordinates"
        else:
            root.goto_box.text = "Invalid coordinates"

    def gen_plot(self, obj):

        if len(self.graph.nodes) > 0:

            self.fig, self.ax = plt.subplots()
            self.ax.set_axis_bgcolor(Window.clearcolor)
            self.ax.axis('square')
            for e in self.graph.edges:
                points = e.line_coordinates
                self.ax.plot([points[0], points[2]], [points[1], points[3]], '-', color = e.color)

            for i in self.graph.nodes:
                x, y = i.coordinates[0], i.coordinates[1]
                circle = Circle(xy = [x, y], radius = 12.5, fc = i.visual_color, ec = "black")
                self.ax.add_patch(circle)
                self.ax.text(x, y, i.visual_text, fontsize = 8)

        
            self.ax.set_xlim([self.graph.nodes_xmin, self.graph.nodes_xmax])
            self.ax.set_ylim([self.graph.nodes_ymin, self.graph.nodes_ymax])
            plt.show(self.fig)

root = MainScreen()
class graphvyApp(App):
    def build(self):
        return root

if __name__ == "__main__":
    app = graphvyApp()
    app.run()
