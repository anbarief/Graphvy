# Minigraphviz (test version)

This is a small application that can visualize graph with node(s) and normal edge(s) made using Kivy (www.kivy.org). It has feaures of:

- Add node(s)

- Connect two nodes

- Highlight nodes of a connected subgraph

- Apply circular layout to the whole graph

- By default, the "Import Data" button will import a synthetic data of twitter users (real usernames but synthetic connectivity) and add it to the graph object of the app. To use different data, the filename must be `data.npy` and the format is a list of dictionaries of nodes and their neighbors ---> `[{'name': "name_of_node_1", 'neighbor': ["name_of_node_i", ....]}, ...]`

-----

Author: Arief Anbiya 

E-mail: anbarief@live.com

Year: 2019

Requirements:

-Python 3.5

-Kivy 1.10.0

-Numpy 1.14.1

To use the app, simply run the `minigraphviz.py`.

-----

![](demo1.gif)

![](demo2.gif)
