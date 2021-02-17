# A collection of scripts to interract with the OrionVM API

## Set up
Clone this repository
`git clone https://github.com/888voip/orion`

Set up virtual environment
`python(3) -m venv <path>`

Activate venv
`source <path>/bin/activate`

Install requirements
`pip(3) install -r requirements.txt`

Create config file
* Create a file called `config.py` in the root of the project
* Obtain an Admin API key from the Orion Admin portal

config.py contents
```
admin_api_key = '<your api key>
```

## Usage
So far, just the instance list generator is done.
Run it with `python(3) instance_list_generator.py`

It will run and create a csv containing all found instances