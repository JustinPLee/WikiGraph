
# WikiGraph

Makes graph from wikipedia links.

Gephi successfully loads 9481 nodes and 25648 edges (highest number tested so far) which seems close to its limit. 



## Project Description
This project visualizes connections between Wikipedia links using Python to fetch Wikipedia links and Networkx and Gephi to generate a graph. Depth and ratio variables can be changed to determine how many links are searched. The depth variable specifies how many times a link's children is searched. The ratio variable beween 0 and 1 tells what percentage to randomly sample from all links for each page.

## Dependencies
- python (v...)
- beautifulsoup (v...)
- requests (v...)
- networkx (v...)
- gephi (v...)


## How to run 
First choose a Wikipedia topic and depth and ratio. For example, if you wanted to search links from https://en.wikipedia.org/wiki/Discord, modify line 124 in main.py with the string. To modify the depth, go to line 125 and type an integer. To modify the ratio, go to line 101 and insert a decimal between 0 and 1. 

First parse wikipedia 

```
python main.py && python convert_networkx.py
```

```convert_networkx.py``` creates a ```.gexf``` file which can be read by Gephi. Networkx supports many different graph file types, but ```.gexf``` files are the default.

Next, open the ```.gexf``` file in Gephi and edit it until it looks complete.

## Picture of result
![alt text](https://github.com/JustinPLee/WikiGraph/blob/main/Earth-D2-R0.015.png?raw=true)
This graph shows related links (nodes) connected to other links by edges. I started with Earth as the Wikipedia subject using a depth of two and a ratio of 0.015. By looking at the connected edges, I can trace a link's connections to its origin.

[TODO] 
Allow ratio to be modified from main and pass it as a parameter
