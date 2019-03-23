# Graphvy (test version)

Basic graph (data) visualization using Kivy (www.kivy.org). It has features of:

- Add node(s)

- Connect two nodes

- Highlight nodes of a connected subgraph

- Edit node's name

- Nodes map

- By default, the "Import Data" button will import a synthetic data of twitter users (real usernames but synthetic connectivity) and add it to the graph object of the app. To use different data, the filename must be `data.npy` and the format is a list of dictionaries of nodes and their neighbors ---> `[{'name': "name_of_node_1", 'neighbor': ["name_of_node_i", ....]}, ...]`

-----

Author: Arief Anbiya 

E-mail: anbarief@live.com

Year: 2019

Requirements:

-Python 3.5

-Kivy 1.10.0

-Numpy 1.14.1

To use the app, simply run the `graphvy.py`.

-----
[b]Preview[/b]:

![](demo_01.gif)

![](demo_02.gif)

![](demo_03.gif)
