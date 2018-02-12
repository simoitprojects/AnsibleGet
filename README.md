# AnsibleGet
AnsibleGet allows you server to request remote ansible server to run playbooks

## When to use it (example)
When you are creating new servers and want to run ansible scripts on them
You don't want to install the whole ansible stack on each server 
Just use wget after server start to send a querry to this script to run specific playbook on requesting server 


## How to use it 
```BASH
wget http://10.0.0.1:8085/get_playbook?playbook=test&name=install_test
```
ip (10.0.0.1) - Replace with ip of the server running this script 
playbook=test - Replace test with your playbook name (playbooks need to be placed in playbook folder)
name=install_test - Replace install_test with a friendly name , this will be the name o the log file containing playbook output 


