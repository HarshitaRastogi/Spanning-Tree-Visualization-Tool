# Spanning-Tree-Visualization-Tool
This tool displays the physical topology and forwarding topology for each instance.
Steps to use the visualization tool 
Configuration file:
On linus server configure eapi.conf
$ vi ~/.eapi.conf

[connection:mt701]
host: 10.85.128.101
username: admin
password:
transport: https

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

Replace connection with hostname, host with management IP, username and
password for each switch and define transport mechanism as https.

Run the script:
$ python finalscript1.py 
This creates son files dynamically in the folder where the script is run. 

Open the HAM.html
View the output 
