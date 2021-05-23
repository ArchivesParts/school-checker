# school-checker
This project contain a tools useful to connect and extract school results from 'Ecole Direct' and provide some tools to enhance visibilty on school results

# Install & Launch 
## Installation 
```shell
source .env/bin/activate
pip install -r requierement.txt
export FLASK_APP=src/app.py
flask run
```

## Configuration file
You must create a configuration file in the src folder named config.py which contain the same structure than the config.py.tpl file
## Launch

```shell
flask run
```

During developpement your can make this export to activate the developpement mode before ***flask running***
> export FLASK_ENV=development 