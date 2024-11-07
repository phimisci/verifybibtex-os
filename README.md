# VerifyBibTex (1.0.0)

# Introduction
VerifyBibTex is a simple Python application that checks your BibTeX file for potential errors. It outputs the results in the command line and writes them to a file called `verifybibtex-report.txt`. The checks are particularly focusing on information necessary for valid citations in the APA style. For an overview of the checks, see the Features section below.

# Installation
## Docker local build
The preferred way to run VerifyBibTex is via Docker. This way, you can avoid any dependency issues. In order to run VerifyBibTex via Docker, follow these steps:

1. Clone this repository.
2. Next, you need to install the Docker engine on your machine. You can find the installation instructions [here](https://docs.docker.com/get-docker/).
3. Once Docker is installed, you can `docker build -t verifybibtex .` in the root folder of this repository, which will create a Docker image called `verifybibtex`.

## Local installation
Even though the Docker installation is preferred, you can also run VerifyBibTex locally. In order to do so, follow these steps:

1. Clone this repository.
2. Make sure that Python (3.8 or higher) is installed on your machine.
3. Install dependencies via `pip install --no-cache-dir --force-reinstall -r requirements.txt`
4. Make sure you have a `report` subfolder in the directory where you want to run the application.

# Usage
If you are using Docker, you can run VerifyBibTex via the following command: `docker run --rm -e BIBTEX_FILE=<FILE_NAME>.bib -v $(pwd):/app/report verifybibtex`, where you replace `<FILE_NAME>` with the name of your BibTeX file. The report `verifybibtex-report.txt` will be written to the root folder of this repository. If you are running VerifyBibTex locally, you can use the command `python verifybibtex.py path/to/bibliography.bib` via command line interface. The report will be written to the `report` subfolder.

VerifyBibTex checks your bibtex file for potential errors. It outputs the results in the command line and writes them to `verifybibtex-report.txt`. There are three types of errors. **Important**: VerifyBibTeX assumes that the BibTeX file uses line breaks within each entry. If your file does not use line breaks (which is a valid option for BibTeX files), the application will not work correctly.

Correct:

```bibtex
@article{key,
    author = {Author},
    title = {Title},
    journal = {Journal},
    year = {2023},
    volume = {1},
    number = {1},
    pages = {1-10},
    doi = {10.1234/5678}
}	
```

Incorrect:

```bibtex
@article{key, author = {Author}, title = {Title}, journal = {Journal}, year = {2023}, volume = {1}, number = {1}, pages = {1-10}, doi = {10.1234/5678}}
```

## General errors
These errors concern the overall structure of the .bib file. If these errors are present, the file is not a valid bibtex bibliography. This may include overall parsing errors, invalid blocks, or empty files.

## Critical errors



## Warnings


3. Checks if title includes more than one pair of curly braces. If so, warn the user to check whether this is correct.
1. Checks if article has a DOI.
2. Checks if article has pages or article numbers.
3. Checks if article includes title.
4. Checks if incollection has "date", "year", or "pubstate" field.
5. Checks if a field is entirely wrapped in curly braces (critical) or has many curly braces (warning).
6. Checks if an author or editor field includes "et al" or "and others" (warning).
7. Checks if every fields correctly ends with a comma.
8. Checks if several characters, such as "&", "%", and "\#", are escaped.

# About
This application was developed by Thomas Jurczyk (thomjur on GitHub) for the journal [Philosophy and the Mind Sciences](https://philosophymindscience.org/) as part of a project funded by the German Research Foundation (DFG).

# Changes

## 1.0.0 (07.11.2024)

- Open Source release of VerifyBibTex

## 0.2.2 (03.07.2024)

- no warning raised if incollection has date or pubstate field
- added check if characters "&", "%", and "\#" were escaped, if not raise error
- added check if ^ \# _ $ were escaped, if not raise warning 

## 0.2.1 (05.03.2024)

Bug fixes:

- changeed DOI pattern to match short DOIs
- changed enumerations in write function
- entries with no warnings are no longer listed
- changed some labels (critical -> Important warnings)
- adding unit tests
- values with several lines breaks should no longer raise "ends with no comma" warning
- all field keys are set lowercase to avoid ignoring keys such as `DOI`
- removed address and publisher field warnings when wrapped in double curly braces

## 0.2.0 (01.03.2024)

Major changes to the application. Instead of logging, VerifyBibTex now uses a simple report file to display the results. The report file is called `bibtex-analysis-status-report.txt` and is written to the current working directory. The report file is overwritten every time the application is run.

The report file includes the following information:
- General information about the file (e.g., number of entries, number of errors)
- More detailed information about the errors that were found
- A list of all entries that were checked
- The errors are subdivided into "critical" and "warning"
- The author and editor fields are now checked for "et al" and "and others" and the user is warned if these are found
- Checks if every field ends with a comma (missing commas can lead to parsing errors during production)

## 0.1.1 (12.12.2023)
The application can now be mounted using Docker. However, you can still use it like before, see installation instructions below.

## 0.1.0 (14.07.2023)
The new version 0.1.0 uses bibtexparser 2.X. Since this package is not available via pip install, make sure to use the correct commands when installing the dependencies (`--no-cache-dir --force-reinstall`). The major upgrade is that VerifyBibTex can now check and display errors during parsing.

## 0.0.1 (16.04.2023)

Initial version.




