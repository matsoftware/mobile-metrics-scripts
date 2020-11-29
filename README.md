# mobile-metrics-scripts
Container for scripts used to analyze mobile apps.

## IPA Size analysis

Usage:
```bash
./bin/ipa.py -h
usage: ipa.py [-h] --ipa-path A --external-frameworks-input-file-list E

Analysis of the size of an IPA file

optional arguments:
  -h, --help            show this help message and exit
  --ipa-path A          The path to the IPA file
  --external-frameworks-input-file-list E
                        The path to xcfilelist file containing the list of names of libraries considered external to the project.
```

