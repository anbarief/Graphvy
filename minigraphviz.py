import random
import math
import copy
import numpy

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color, Line
from kivy.properties import ListProperty

wsize = Window.size
Window.clearcolor = (0.7, 0.7, 0.7, 0.9)
node_info = "Name: {}, Value: {}, Degree: {}, ID: {}"
radius = {'double': 50, 'normal': 25, 'small': 12.5, 'mini': 6.5}

class MainScreen(FloatLayout):

    def __init__(self):
        super().__init__()
        self.axis = Axis()
        self.add_widget(self.axis)
        self.axis.size_hint = (1, 1)
        self.buttons = []
        
        self.reset_button = Button(text = "Reset")
        self.add_widget(self.reset_button)
        self.reset_button.size_hint = (0.2, 0.1)
        self.reset_button.halign = "center"
        self.reset_button.bind(on_release = self.axis.reset)
        self.buttons.append(self.reset_button)

        self.node_button = Button(text = "Add Node")
        self.add_widget(self.node_button)
        self.node_button.size_hint = (0.2, 0.1)
        self.node_button.pos_hint = {'x':0.2, 'y':0}
        self.node_button.halign = "center"
        self.node_button.bind(on_release = self.axis.add_node)
        self.buttons.append(self.node_button)

        self.connect_button = Button(text = "Connect Nodes")
        self.add_widget(self.connect_button)
        self.connect_button.size_hint = (0.2, 0.1)
        self.connect_button.pos_hint = {'x':0.4, 'y':0}
        self.connect_button.halign = "center"
        self.connect_button.bind(on_release = self.axis.connect_nodes)
        self.buttons.append(self.connect_button)

        self.info_label = TextInput(text = "Info: ")
        self.add_widget(self.info_label)
        self.info_label.size_hint = (0.4, 0.2)
        self.info_label.pos_hint = {'x': 0.6, 'y': 0}
        self.info_label.halign = "left"
        self.info_label.valign = "top"
        self.info_label.text_size = [0.4*wsize[0], 0.1*wsize[1]] 
        self.info_label.disabled = True

        self.connected_subgraph_button = Button(text = "Connected Subgraph")
        self.add_widget(self.connected_subgraph_button)
        self.connected_subgraph_button.size_hint = (0.2, 0.1)
        self.connected_subgraph_button.pos_hint = {'x':0.8, 'y': 0.2}
        self.connected_subgraph_button.halign = "center"
        self.connected_subgraph_button.bind(on_release = self.axis.connected_subgraph)
        self.buttons.append(self.connected_subgraph_button)

        self.circular_layout_button = Button(text = "Apply Circular Layout")
        self.add_widget(self.circular_layout_button)
        self.circular_layout_button.size_hint = (0.2, 0.1)
        self.circular_layout_button.pos_hint = {'x':0.8, 'y': 0.3}
        self.circular_layout_button.halign = "center"
        self.circular_layout_button.bind(on_release = self.axis.circular_layout)
        self.buttons.append(self.circular_layout_button)

        self.mini_scale_button = Button(text = "25%")
        self.add_widget(self.mini_scale_button)
        self.mini_scale_button.size_hint = (0.1, 0.1)
        self.mini_scale_button.pos_hint = {'x':0.8, 'y': 0.4}
        self.mini_scale_button.halign = "center"
        self.mini_scale_button.bind(on_release = self.axis.mini_scale)
        self.buttons.append(self.mini_scale_button)

        self.small_scale_button = Button(text = "50%")
        self.add_widget(self.small_scale_button)
        self.small_scale_button.size_hint = (0.1, 0.1)
        self.small_scale_button.pos_hint = {'x':0.9, 'y': 0.4}
        self.small_scale_button.halign = "center"
        self.small_scale_button.bind(on_release = self.axis.small_scale)
        self.buttons.append(self.small_scale_button)

        self.normal_scale_button = Button(text = "100%")
        self.add_widget(self.normal_scale_button)
        self.normal_scale_button.size_hint = (0.1, 0.1)
        self.normal_scale_button.pos_hint = {'x':0.8, 'y': 0.5}
        self.normal_scale_button.halign = "center"
        self.normal_scale_button.bind(on_release = self.axis.normal_scale)
        self.normal_scale_button.disabled = True
        self.buttons.append(self.normal_scale_button)
        
        self.double_scale_button = Button(text = "200%")
        self.add_widget(self.double_scale_button)
        self.double_scale_button.size_hint = (0.1, 0.1)
        self.double_scale_button.pos_hint = {'x':0.9, 'y': 0.5}
        self.double_scale_button.halign = "center"
        self.double_scale_button.bind(on_release = self.axis.double_scale)
        self.buttons.append(self.double_scale_button)

        self.import_csv_button = Button(text = "Import CSV")
        self.add_widget(self.import_csv_button)
        self.import_csv_button.size_hint = (0.2, 0.1)
        self.import_csv_button.pos_hint = {'x':0.8, 'y': 0.6}
        self.import_csv_button.halign = "center"
        self.import_csv_button.bind(on_release = self.axis.import_csv)

     
class Node(Button):
    
    widget_pos = ListProperty()
    widget_size = ListProperty()
    node_center = ListProperty()

    def __init__(self, value, text, center, color, circle_scale = 'normal'):
        super().__init__()
        self.value = value
        self.visual_text = text
        self.visual_color = color
        self.scale = circle_scale
        self.r = radius[circle_scale]
        self.background_color = (0, 0, 0, 0)
        self.pos = [center[0]-self.r, center[1]-self.r]
        self.size = (2*self.r, 2*self.r)

        self.visual_widget = Widget()
        self.add_widget(self.visual_widget)
        self.visual_widget.pos = self.pos
        self.visual_widget.size = self.size

        self.apply_visual(source = "circle2_{}.png".format(self.scale), color = self.visual_color)

        self.edges = []
        self.neighbor = []
        self.press_count = -1
        
        self.widget_pos = self.pos
        self.widget_size = self.size
        self.node_center = center
        
    def apply_visual(self, source = "circle2_normal.png", color = (0,0.2,1,1)):
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
        self.node_text = Label(text = self.visual_text, font_size = 20, font_name = 'DejaVuSans')
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
            color = Color(0, 0.2, 0.9, 0.8)
            root.axis.edge_drawer.canvas.add(color)
            root.axis.edge_drawer.canvas.add(line)

            edge_obj = NormalEdge(nodes, line)
            nodes[0].add_edge(edge_obj)
            nodes[0].neighbor.append(nodes[1])
            nodes[1].add_edge(edge_obj)
            nodes[1].neighbor.append(nodes[0])
        else:
            pass
        
    def move(self, touch):
        new_pos = [touch.x, touch.y]
        self.pos = [new_pos[0]-self.r, new_pos[1]-self.r]
        self.circle.pos = self.pos
        self.node_text.pos = self.pos
    
    def on_press(self):
        super().on_press()

        self.press_count *= -1
        if self.press_count == 1:
            self.background_color = (0, 0.8, 0.9, 0.5)
            self.node_text.color = (1, 1, 1, 1)

            root.info_label.text = "Info: " + node_info.format(self.node_text.text, self.value, self.degree, self)
            
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
                        color = Color(0, 0.2, 0.9, 0.8)
                        root.axis.edge_drawer.canvas.add(color)
                        root.axis.edge_drawer.canvas.add(line)

                        edge_obj = NormalEdge(nodes, line)
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

        else:
            self.background_color = (0, 0, 0, 0)
            self.node_text.color = (1, 1, 1, 0.2)
            if self.parent.connect_nodes_option == 1:
                if self.parent.a_to_b != []:
                    self.parent.a_to_b.pop()


class NormalEdge:

    def __init__(self, nodes, line):
        self.nodes = nodes
        self.line = line

    def update_line(self):
        self.line.points = [self.nodes[0].center[0], self.nodes[0].center[1], \
                            self.nodes[1].center[0], self.nodes[1].center[1]]
        

class Graph:

    def __init__(self, nodes = None, name = ""):
        if nodes == None:
            self.nodes = []
        else:
            self.nodes = nodes
        self.name = name
        self.connected_subgraphs = []
        self.previous_selected_subgraph = None
        self.visual_size = {'lw': 2}

    def connected_by_normal_edge(self, nodes):
        combined = nodes[0].edges + nodes[1].edges
        if len(set(combined)) == len(combined):
            return False
        else:
            return True

    @property
    def edges(self):
        x = []
        for i in self.nodes:
            x = x + i.edges
        return list(set(x))

    def find_subgraph(self, start_edge):
        edges = [i for i in self.edges]
        subgraph = Graph(nodes = start_edge.nodes)

        n = None
        while len(edges) != n:
            n = len(edges)
            for edge in edges:
                for j in edge.nodes:
                    if j in subgraph.nodes:
                        new_nodes = [k for k in edge.nodes if k not in subgraph.nodes]
                        subgraph.nodes += new_nodes
                        edges.remove(edge)
                        break

        return subgraph

        
class Axis(Widget):

    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.add_node_option = -1
        self.connect_nodes_option = -1
        self.connected_subgraph_option = -1
        self.a_to_b = []
        self.graph = Graph()

        self.edge_drawer = Widget()
        self.add_widget(self.edge_drawer)
        self.scale = "normal"

        if self.parent != None:
            for i in self.parent.buttons:
                i.disabled = False
            self.parent.normal_scale_button.disabled = True

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
            if self.add_node_option == 1:
                node = Node(None, str(len(self.children)-1), [x, y], \
                            (0, 0.6, 1), circle_scale = self.scale)
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
        
    def reset(self, obj):
        self.clear_widgets(self.children)
        self.start()
        
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
        else:
            obj.text = "Add Node"
            self.parent.reset_button.disabled = False
            self.parent.connect_button.disabled = False
            self.parent.connected_subgraph_button.disabled = False

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
        else:
            obj.text = "Connect Nodes"
            self.parent.reset_button.disabled = False
            self.parent.node_button.disabled = False
            self.parent.connected_subgraph_button.disabled = False
            self.a_to_b = []
        
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
        else:
            obj.text = "Connected Subgraph"
            self.parent.reset_button.disabled = False
            self.parent.node_button.disabled = False
            self.parent.connect_button.disabled = False

    def circular_layout(self, obj):
        n = len(self.graph.nodes)
        r = n*(self.graph.nodes[0].r)
        delta = 2*math.pi/n
        for i in range(n):
            node = self.graph.nodes[i]
            point = [0.5*wsize[0] + r*math.cos( delta*i ), \
                     0.5*wsize[1] + r*math.sin( delta*i )]
            node.node_center = point
            print(i)
        for i in self.graph.edges:
            i.update_line()
        
    def mini_scale(self, obj):
        if self.scale == "normal":
            k = 1/4
        elif self.scale == "small":
            k = 1/2
        elif self.scale == "double":
            k = 1/8
        self.axis_change_scale(k, {'type': "mini", \
                                   'lw': 1/2, \
                                   'img': "circle2_mini.png",\
                                   })

    def small_scale(self, obj):
        if self.scale == "normal":
            k = 1/2
        elif self.scale == "double":
            k = 1/4
        elif self.scale == "mini":
            k = 2
        self.axis_change_scale(k, {'type': "small", \
                                   'lw': 1, \
                                   'img': "circle2_small.png",\
                                   })

    def normal_scale(self, obj):
        if self.scale == "double":
            k = 1/2
        elif self.scale == "small":
            k = 2
        elif self.scale == "mini":
            k = 4
        self.axis_change_scale(k, {'type': "normal", \
                                   'lw': 2, \
                                   'img': "circle2_normal.png",\
                                   })

    def double_scale(self, obj):
        if self.scale == "normal":
            k = 2
        elif self.scale == "small":
            k = 4
        elif self.scale == "mini":
            k = 8
        self.axis_change_scale(k, {'type': "double", \
                                   'lw': 4, \
                                   'img': "circle2_double.png",\
                                   })

    def axis_change_scale(self, k, scale):
        self.scale = scale['type']
        self.graph.visual_size['lw'] = scale['lw']
        for i in self.graph.nodes:
            i.r = radius[self.scale]
            i.update_visual(scale['img'], i.visual_color)
            i.node_center[0] = k*i.node_center[0]
            i.node_center[1] = k*i.node_center[1]
            i.widget_size[0] = k*i.widget_size[0]
            i.widget_size[1] = k*i.widget_size[1]
        for e in self.graph.edges:
            e.line.width = self.graph.visual_size['lw']
            e.update_line()
        self.parent.mini_scale_button.disabled = False
        self.parent.small_scale_button.disabled = False
        self.parent.normal_scale_button.disabled = False
        self.parent.double_scale_button.disabled = False
        if self.scale == "mini":
            self.parent.mini_scale_button.disabled = True
        elif self.scale == "small":
            self.parent.small_scale_button.disabled = True
        elif self.scale == "normal":
            self.parent.normal_scale_button.disabled = True
        else:
            self.parent.double_scale_button.disabled = True

    def import_csv(self, obj):
        if self.scale == "normal":
            k = 1
        elif self.scale == "small":
            k = 1/2
        elif self.scale == "mini":
            k = 1/4
        else:
            k = 2
        dataset = list(numpy.load("synthetic_data.npy"))
        nodes = []
        for i in dataset:
            x = random.uniform(0, 2*k*800)
            y = random.uniform(0, 2*k*600)
            node = Node(None, i['name'], [x, y], \
                            (0, 0.6, 1), circle_scale = self.scale)
            self.graph.nodes.append(node)
            self.add_widget(node)
            nodes.append((node, i['neighbor']))
        for node in nodes:
            neighbors = [i for i in nodes if i[0].visual_text in node[1]]
            for i in neighbors:
                node[0].connect_node(i[0])
        
            
if __name__ == "__main__":
        
    root = MainScreen()
    class minigraphvizApp(App):
        def build(self):
            return root

    app = minigraphvizApp()
    app.run()
