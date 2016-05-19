# Spanning-Tree-Visualization-Tool

#### IMPORTANT, THIS TOOL UTILIZES ARISTA SPECIFIC TECHNOLOGY (EAPI) AND SO CANNOT BE USED WITH SWITCHES MANUFACTURED BY ANY OTHER VENDOR

Overview:

Implementing Spanning-Tree in a customer network creates complications with regard to visibility of the forwarding topology used by frames. In each Switch it is only possible to view the port roles and states of local interfaces, they do not know what the logical loop free toplogy looks like. This tool displays the converged loop free topology for each instance of Spanning-Tree running on each Switch. The merits of this tool are highlighted when a large scale of layer 2 Switches running Rapid Spanning Tree Protocol are deployed in the network or if Multiple Spanning Tree Protocol (MSTP) is configured on the Switches.

Steps to use the visualization tool

1) Configuration file

In order to view the converged topology created by Spanning Tree on the Switches, the information relevant to Spanning-Tree must be fetched from the participating Switches. To specify the Switches from where this information needs to be pulled, a configuration file is used. This file is stored on the Server which will display the converged topology.

On linux server configure eapi.conf
$ vi ~/.eapi.conf

[connection:mt701]
host: 10.85.128.101                          // Management IP of the Switch
username: admin                              
password:
transport: https                             // Protocol used over Layer 4 to fetch the information

[connection:mt702]
host:10.85.128.102
username: admin
password:
transport: https

[connection:mt703]
host: 10.85.128.103
username: admin
password:
transport: https

[connection:mt704]
host:10.85.128.104
username: admin
password:
transport: https

2) Running finalscript1.py

This python script fetches the output of "show spanning-tree detail","show lldp neighbors","show interfaces switchport". These outputs are used to create JSON files which will in turn be used to construct the logical loop free topology. 
This script is to be run on the server which will display Visual output.

3) Web Server

The script which displays the logical loop free topology requires access to the JSON output files created in the previous step. To do so, a Web Server application is to be installed which will host these JSON output files. As such the folder hosted by the Web Server must contain the script finalscript1.py as well.

The Web Server application used in this project: "Web Server for Chrome"
https://chrome.google.com/webstore/detail/web-server-for-chrome/ofhbbkphhbklhfoeikjpcbhemlocgigb?hl=en

4) HTML file

The HTML file opens the JSON files in the javascript section. D3 (javascript library) is used to represent the forwarding topology using graphs(nodes and edges). The nodes and edges are labelled in the graph. D3 uses an attribute "gravity" that moves the labels along the edges when the nodes are moved. To avoid confusion, the hostnames of switches are marked alongwith the ports.

