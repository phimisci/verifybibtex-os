import bibtexparser  # type: ignore
import argparse
import os
from bibtexparser import Library  # type: ignore
from functions import *
from typing import Dict

#########################################
# ARGPARSE
#########################################

# PARSING ARGUMENTS
parser = argparse.ArgumentParser(
    description='VerifyBibTex: A tool to verify BibTex files.')
parser.add_argument('bibtex_path', type=str, help='Path to Bibtex file')
args = parser.parse_args()

# ARGPARSE ARGUMENT VARS
file_path = args.bibtex_path

def main(library: bibtexparser.Library, verifybibtex_dict: Dict) -> None:
    '''Function with main program logic of VerifyBibTex.

        Parameters
        ----------
            library: bibtexparser.Library
                The parsed bibtex data from the .bib file.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.

    '''
    # Check for parsing errors
    if len(library.failed_blocks) > 0:
        check_parsing_errors(library.failed_blocks, verifybibtex_dict)
    else:
        verifybibtex_dict["general"].append("All blocks parsed successfully.")

    # Check for errors in bibtex entries
    for entry in library.entries:
        # Create new entry field in verifybibtex_dict
        verifybibtex_dict["entries"][entry["ID"]] = {
            "critical": list(),
            "warning": list()
        }
        # Set all field keys lowercase
        set_all_field_keys_lowercase(entry)
        # Check for invalid fields (missing comma)
        check_invalid_fields(entry, verifybibtex_dict)
        # Check all entries for unescaped characters
        check_unescaped_characters(entry, verifybibtex_dict)
        # Check entries for errors
        if entry["ENTRYTYPE"].lower() == 'article':
            check_article_doi(entry, verifybibtex_dict)
            check_article_pages(entry, verifybibtex_dict)
        elif entry["ENTRYTYPE"].lower() == 'incollection':
            check_incollection(entry, verifybibtex_dict)
        # Check if an entry contains a type field
        if entry["ENTRYTYPE"].lower() != 'thesis':
            check_type_field(entry, verifybibtex_dict)
        ## Check for all entries
        check_author_field(entry, verifybibtex_dict)
        check_curly_braces(entry, verifybibtex_dict)
        check_double_curly_braces(entry, verifybibtex_dict)

    # write output
    write_output(verifybibtex_dict)


if __name__ == "__main__":
    # Create dictionary to collect error messages for BibTex entries
    verifybibtex_dict = create_verifybibtex_dictionary()

    # Check if file exists
    if not os.path.isfile(file_path):
        verifybibtex_dict["general"].append(f"{file_path} is not a file.")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        exit()

    # Open file and check if it is a valid bibtex file with entries
    try:
        library = bibtexparser.parse_file(file_path)
    except:
        verifybibtex_dict["general"].append("No valid bibtex file!")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        exit()

    # File empty?
    if len(library.entries) == 0:
        verifybibtex_dict["general"].append(f"No bibliographical entries found in {file_path}.")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        exit()

    # Run main program logic if everything was fine
    main(library, verifybibtex_dict)
