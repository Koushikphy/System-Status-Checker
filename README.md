# System Status Checker
### A dashboard like webserver to check system status of multiple PC/Workstation/Cluster in a single place. 


## Get Started:
1. Install Django-3 and clone this repo.
2. Make database migrations and create a superuser.
3. From the admin panel (`/admin/`) add your server, ip address, commands to run etc.
4. A list of predefined commands is already given in the `models.py` and they can be set using server type option.
5. Now go to home (`/home/`) to check the status of the added systems. Use refresh to get latest status.