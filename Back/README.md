# Guide d'installation MyAPI

- Ouvrir mysql et importer database.sql

- Faire un .env avec les variables suivantes: 

`DB_HOST= localhost`

`DB_PORT= 3306`

`DB_NAME= myapi`

`DB_USER= root`

`DB_PASSWORD= root`


- Se placer à la racine du projet et run 
` python -m venv env `

`source env/bin/activate ` sur macOs OU `source env/Scripts/activate` sur Windows


- Toujours à la racine, run 

` pip install -r requirements.txt `


- Enfin, pour lancer l'api : 

` cd App && python __init.py__ `
