raions
======
[*raions*](http://raions.veritexgroup.com.ua/) is a simple Ukrainian realty estimation service.
It's main purpose is to aggregate real estate data and provide informative insights with the help 
of machine learning.

Previews
--------
![preview0](previews/preview0.png)

![preview1](previews/preview1.png)

![preview2](previews/preview2.png)

![preview3](previews/preview3.png)

![preview4](previews/preview4.png)

![preview5](previews/preview5.png)

Structure
---------
- **agony** - web app & UI provider, written on *django*;
- **reapy** - data miner & web scraper, written on *asyncio*. Should be launched via *cron*;
- **pythagoras** - data analysis part, which's gonna use *scikit-learn* (under construction).

Usage
-----
3 general programs you need to have on your machine are:
- **cron**, elegant task scheduler (any implementation you want);
- **nginx**, fast HTTP-server (it's and *gunicorn*'s configuration details can be found on any
free resource, like this [one](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04));
- **postgresql**, RDBMS, which also must include *PostGIS* extension.

The service doesn't automatically configure all these stuff so you need to set them manually. 
Besides *cron*'s and *nginx*'s configurations, your environment need 2 *postgresql*'s DBs (
the first one is for production use and the second one is for the test suits of *reapy*; both
of them need *PostGIS* extension installed). Generally, your deployment steps are:
1. Download & install all needed utilities;
2. Create 2 databases - for production and tests accordingly;
3. Run `$ ./deployment.sh`;
4. Configure *gunicorn* & *nginx*. 

Makefile
--------
We provide useful makefile for a local development. General commands are:
- **run-agony-dev** - launches *django* dev-server;
- **run-olx-flat-reaper** & **run-dom-ria-flat-reaper** - launch 2 the most popular *reapy*'s workers;
- **test-agony** & **test-reapy** - run appropriate test suites;
- **help** - outputs the command list.

License
-------
This software is published under the [GNU GPL v3](LICENSE).