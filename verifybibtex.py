"""
This module is the main module of the VerifyBibTex tool. It checks a BibTex file for errors and outputs a report with error messages and warnings.
"""

import bibtexparser  # type: ignore
import argparse
import os
from bibtexparser import Library  # type: ignore
from functions import *
from typing import Dict

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for VerifyBibTex tool.
    
        Returns
        -------
            argparse.Namespace
                The parsed command-line arguments.
    
    """
    parser = argparse.ArgumentParser(description='VerifyBibTex: A tool to verify BibTex files.')
    parser.add_argument('bibtex_path', type=str, help='Path to Bibtex file')
    return parser.parse_args()

def main(library: bibtexparser.Library, verifybibtex_dict: Dict) -> None:
    """
    Function with main program logic of VerifyBibTex.

        Parameters
        ----------
            library: bibtexparser.Library
                The parsed bibtex data from the .bib file.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        
        Returns
        -------
            None
            
    """
    # Check for parsing errors
    if len(library.failed_blocks) > 0:
        check_parsing_errors(library.failed_blocks, verifybibtex_dict)
    else:
        verifybibtex_dict["general"].append("All blocks parsed successfully.")

    # Check for errors in bibtex entries
    for entry in library.entries:
        verifybibtex_dict["entries"][entry["ID"]] = {
            "critical": list(),
            "warning": list()
        }
        set_all_field_keys_lowercase(entry)
        check_invalid_fields(entry, verifybibtex_dict)
        check_unescaped_characters(entry, verifybibtex_dict)
        
        if entry["ENTRYTYPE"].lower() == 'article':
            check_article_doi(entry, verifybibtex_dict)
            check_article_pages(entry, verifybibtex_dict)
        elif entry["ENTRYTYPE"].lower() == 'incollection':
            check_incollection(entry, verifybibtex_dict)
        
        if entry["ENTRYTYPE"].lower() != 'thesis':
            check_type_field(entry, verifybibtex_dict)

        check_author_field(entry, verifybibtex_dict)
        check_curly_braces(entry, verifybibtex_dict)
        check_double_curly_braces(entry, verifybibtex_dict)

    write_output(verifybibtex_dict)

def run() -> None:
    """Execute the VerifyBibTex tool with command-line arguments.
    
        Returns
        -------
            None
    
    """
    args = parse_arguments()
    verifybibtex_dict = create_verifybibtex_dictionary()

    # Check if file exists
    if not os.path.isfile(args.bibtex_path):
        verifybibtex_dict["general"].append(f"{args.bibtex_path} is not a file.")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        return

    # Open file and check if it is a valid bibtex file with entries
    try:
        library = bibtexparser.parse_file(args.bibtex_path)
    except Exception:
        verifybibtex_dict["general"].append("No valid bibtex file!")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        return

    # File empty?
    if len(library.entries) == 0:
        verifybibtex_dict["general"].append(f"No bibliographical entries found in {args.bibtex_path}.")
        verifybibtex_dict["errors"] += 1
        write_output(verifybibtex_dict)
        return

    # Run main program logic if everything was fine
    main(library, verifybibtex_dict)

if __name__ == "__main__":
    run()
