# VerifyBibTeX-OS (1.0.0)

## Introduction
VerifyBibTeX-OS is a Python application that checks your BibTeX file for potential errors. It outputs the results in the command line and writes them to a file called `verifybibtex-report.md`. The checks are particularly focusing on information necessary for valid citations in the APA style. For an overview of the checks, see the Features section below. The application heavily relies on the `bibtexparser` package ([Link](https://bibtexparser.readthedocs.io/en/main/index.html)).

## Installation
The preferred way to run VerifyBibTex is via Docker. This way, you can avoid any dependency issues. First, you need to install the Docker engine your machine. You can find the installation instructions [here](https://docs.docker.com/get-docker/).


### GitHub Container Registry
You can pull the Docker image from the GitHub Container Registry. To do so, run the following command: `docker pull ghcr.io/phimisci/verifybibtex-os:latest`.

`docker pull ghcr.io/phimisci/verifybibtex-os:latest`


### Docker local build
In order to run VerifyBibTex via Docker using a local build, follow these steps:

1. Clone this repository.
2. Assuming that yoh have Docker installed, you can now use `docker build -t verifybibtex .` in the root folder of this repository to create the Docker image.

### Local installation
Even though the Docker installation is preferred, you can also run VerifyBibTex locally. In order to do so, follow these steps:

1. Clone this repository.
2. Make sure that Python (3.8 or higher) is installed on your machine.
3. Install dependencies via `pip install --no-cache-dir --force-reinstall -r requirements.txt`
4. Make sure you have a `report` subfolder in the directory where you want to run the application.

## Usage
If you are using Docker, you can run VerifyBibTex via the following command: `docker run --rm -e BIBTEX_FILE=<FILE_NAME>.bib -v $(pwd):/app/report verifybibtex`, where you replace `<FILE_NAME>` with the name of your BibTeX file. In case you have been downloading the Docker image from the GitHub Container Registry, just replace `verifybibtex` with `ghcr.io/phimisci/verifybibtex-os:latest`. The report `verifybibtex-report.txt` will be written to the root folder of this repository. If you are running VerifyBibTex locally, you can use the command `python verifybibtex.py path/to/bibliography.bib` via command line interface. The report will be written to the `report` subfolder.

VerifyBibTex checks your bibtex file for potential errors. It outputs the results in the command line and writes them to `verifybibtex-report.md`. There are three types of errors. **Important**: VerifyBibTeX assumes that the BibTeX file uses line breaks within each entry. If your file does not use line breaks (which is a valid option for BibTeX files), the application will not work correctly.

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

### General errors
These errors concern the overall structure of the .bib file. If these errors are present, the file is not a valid bibtex bibliography. This may include overall parsing errors, invalid blocks, or empty files.

### Critical errors
Critical errors are errors that are likely to cause problems when using the bibliography in a citation manager or when compiling a document. These errors should be fixed before using the bibliography. This section also includes obviously missing information, such as missing book or article titles etc.

1. Checks if every field except the last one ends with a comma.
2. Checks if characters, such as "&", "%", and "\#", are escaped.
3. Checks if incollection has date, booktitle, and editor fields.
4. Checks if article has a title field.
5. Checks if a field is entirely wrapped in curly braces.

### Warnings
Warnings are less critical than errors but should still be fixed. They may indicate potential problems with the bibliography or with the citation. This section includes warnings about missing information that is not critical for the citation but may be important for the reader.

1. Checks if less critical characters, such as "$", "^", _", and "~", are escaped.
2. For articles: Checks if article has a DOI or URL.
3. For articles: Checks if article has an indicated page range or article numbers.
4. For incollections: Checks if incollection entries have an editor, publisher, and a page range.
5. In case of thesis entries, make sure that they do not have a "type" field.
6. Checks if author or editor fields include 'et al' or 'and others' (which should be avoided).
7. Checks if title fields include many curly braces. If so, warn the user to check whether this is correct.

## About
This application was developed by Thomas Jurczyk (thomjur on GitHub) for the journal [Philosophy and the Mind Sciences](https://philosophymindscience.org/) as part of a project funded by the German Research Foundation (DFG).

## Versions

### 1.0.0 (07.11.2024)
- Open Source release of VerifyBibTex.
