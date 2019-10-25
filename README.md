# Molly

Molly is a simple to use (noisy) multithreaded port scanner. You can use it to find 
potential vulnerabilities within your network.

## Installation
Make sure you have either pip or pipenv installed on your system and run:

```
pip install molly
```

or 
```
pipenv install molly
```

## Basic Usage
Molly comes with a simple subcommand conveniently called `scan`. 
It takes a target as an argument and two non-required options: `mode` and `workers`

```
molly scan <target> --mode<mode> --workers <workers>
```

Below are a few examples

### Very Simple Scan
```
molly scan scanme.nmap.org
```

### Scan the top 20 ports for a given target
```
molly scan scanme.nmap.org --mode common
```

### Increase the number of worker threads to improve speed
```
molly scan 192.168.0.4 --workers 200
```

#### Arguments and options

- `target`: the target to perform the scan against (can be a hostname or a valid IPv4 address)
- `mode`: the type of scan to perform. Choose between:
    - `basic` (default): Ports 1 to 1024.
    - `full`: all TCP ports.
    - `common`: top 20 ports (21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080 ).
    - `custom` (prompt): your desired port range (separated by a comma).
- `workers`: the number of worker threads to run


## Future features and Roadmap
While molly in its current state is not in alpha by any measure. I plan on adding more features to it as I go along and learn more about computer networking. The aim is for me to solidify my knowledge in the subject and to provide **you** with a solid application that you can use reliably.

The following is the list of features a plan on implementing:

- Ping sweeps
- Ip Ranges
- "Stealthy" port scanning

## Licence

WTFPL

## Contributing
This project is completely free and open source, therefore I not only welcome but encourage contributions from other developers. 

If you want to report a bug or ask for a new feature, I invite you to open a new issue.
Even better, if you want to dig in the code and offer your solution, open a PR with your changes (just make sure all the tests pass).