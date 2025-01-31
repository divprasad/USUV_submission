# README

## Overview

This repository contains scripts and data for generating and submitting XML files to the European Nucleotide Archive (ENA). The scripts convert TSV files containing metadata into XML files with the required structure for submitting experiment, run, and sample metadata objects to ENA.

## Repository Structure

```
.
├── .gitignore
├── exp/
│   ├── create_exp_xml.py
│   ├── exp.tsv
│   ├── exp.xml
├── make-submit-xml.sh
├── run/
│   ├── create_run_xml.py
│   ├── run.tsv
│   ├── run.xml
├── runExpSubmit/
│   ├── 0.add.submission.xml
│   ├── exp.xml
│   ├── run.xml
├── samSubmit/
│   ├── 0.add.submission.xml
│   ├── create_sam_xml.py
│   ├── sam.tsv
│   ├── sam.xml
```

## Scripts

###

make-submit-xml.sh



This script generates and submits ENA XML files.

**Usage:**
```sh
makexml.sh -t  # Run in test mode (default)
makexml.sh -s  # Run in submission mode
makexml.sh -h  # Display help message
```

###

create_exp_xml.py



This script converts an

exp.tsv

 file into an

exp.xml

 file.

**Usage:**
```sh
python3 create_exp_xml.py
```

###

create_run_xml.py



This script converts a

run.tsv

 file into a

run.xml

 file.

**Usage:**
```sh
python3 create_run_xml.py
```

###

create_sam_xml.py



This script converts a

sam.tsv

 file into a

sam.xml

 file.

**Usage:**
```sh
python3 create_sam_xml.py 
```

## Installation

To install the required dependencies, run:
```sh
pip install lxml
```

## Notes

- Ensure that the sample metadata object is submitted before running the experiment and run scripts.
- The TSV files must include all required fields for generating the metadata XML.
