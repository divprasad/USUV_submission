## Overview

This repository is specific for Usutu virus submission and it has been adapted accordingly.

It contains scripts and dummy data for generating and submitting XML files to the European Nucleotide Archive (ENA). The scripts convert TSV files containing metadata into XML files with the required structure and submit the experiment, run, and sample metadata objects all in one go.

The wrapper script `make-submit-xml.sh` generates and submit (or modify existing) ENA metadata objects in XML format, using [programmatic submission](https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html).

---

## Installation

To install the required dependency, run:
```
pip install lxml
```

**Usage:**

```
make-submit-xml.sh -t  # Run in test mode (default)
make-submit-xml.sh -s  # Run in submission mode
make-submit-xml.sh -h  # Display help message
```

make-submit-xml.sh essentially combines all the three subparts (`create_sam_xml.py`, `create_exp_xml.py` , `create_run_xml.py`) of the submission file generation and submits for testing/production.


**Usage for creating individual xml:**
```
python3 create_sam_xml.py #converts the sam.tsv file into sam.xml file.
python3 create_exp_xml.py #converts the exp.tsv file into an exp.xml file.
python3 create_run_xml.py #converts the run.tsv file into run.xml file.
```

### Repository Structure

After cloning the repo and executing the wrapper `make-submit-xml.sh`, you get this directory sturcture

```
this_repo
├── .gitignore
├── LICENSE
├── README.md
├── make-submit-xml.sh
├── exp/
│   ├── create_exp_xml.py
│   ├── exp.tsv
│   └── exp.xml
├── run/
│   ├── create_run_xml.py
│   ├── run.tsv
│   └── run.xml
├── runExpSubmit/
│   ├── add_submission.xml
│   ├── modify_submission.xml
│   ├── exp.xml
│   └── run.xml
└── samSubmit/
    ├── add_submission.xml
    ├── modify_submission.xml
    ├── create_sam_xml.py
    ├── sam.tsv
    └── sam.xml
```


---

First set environment variables in terminal. This is a more secure way of handling credentials.
```
export U_NAME="your_username"
export PASS_WORD="your_password"
```

The wrapper script make-submit-xml.sh generates and submit (or modify existing) ENA metadata objects in XML format, using programmatic submission (https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html).

**Usage:**
```sh
make-submit-xml.sh -t  # Run in test mode (default)
make-submit-xml.sh -s  # Run in submission mode
make-submit-xml.sh -h  # Display help message
```

## Installation

To install the required dependencies, run:
```sh
pip install lxml
```

###

create_sam_xml.py script converts the sam.tsv file into sam.xml file.

**Usage:**
```sh
python3 create_sam_xml.py
```

###

create_exp_xml.py script converts the exp.tsv file into an exp.xml file.

**Usage:**
```sh
python3 create_exp_xml.py
```

###

create_run_xml.py script converts the run.tsv file into run.xml file.

**Usage:**
```sh
python3 create_run_xml.py
```

### Notes  

- Ensure that the sample metadata object is submitted before running the experiment and run scripts.
- The TSV files must include all required fields for generating the metadata XML.
