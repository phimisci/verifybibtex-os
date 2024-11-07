import re
from typing import Dict
import bibtexparser # type: ignore

def check_article_doi(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if article document has DOI or URL.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    # Check if doi or url is present
    if (entry.fields_dict.get("doi") == None) and (entry.fields_dict.get("url") == None):
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            f"No DOI or URL could be found!")
        verifybibtex_dict["errors"] += 1
    elif entry.fields_dict.get("doi") != None:
        # Check if doi is correct (not including any domains but only the ID)
        pattern = re.compile(r"^10.*?\/[-._;()/:a-zA-Z0-9]+$")
        doi = str(entry["doi"])
        if not re.match(pattern, doi):
            verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                f"This entry seems to have malformatted DOI: {doi}.")
            verifybibtex_dict["errors"] += 1
        
        # Check if doi ends with a full stop, which might be an error
        if str(entry["doi"])[-1] == ".":
            verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                f"This entries' DOI ends with a full stop, which might cause problems: {doi}")
            verifybibtex_dict["errors"] += 1

def check_article_pages(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if article document has pages.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    if entry.fields_dict.get("pages") == None:
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            "Article has no indicated page range. Please check if this is correct.")
        verifybibtex_dict["errors"] += 1

def check_author_field(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    '''Function to check if author/editor field is valid.
    
        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    author_pattern = re.compile(r"et al|and others",re.IGNORECASE)
    if entry.fields_dict.get("author") != None:
        if re.search(author_pattern, entry["author"]):
            verifybibtex_dict["entries"][entry['ID']]["warning"].append(
                "Author field contains 'et al' or 'and others'. Please avoid using these abbreviations and list all authors instead. Individual authors should be separated by 'and'.")
            verifybibtex_dict["errors"] += 1
    if entry.fields_dict.get("editor") != None:
        if re.search(author_pattern, entry["editor"]):
            verifybibtex_dict["entries"][entry['ID']]["warning"].append(
                "Editor field contains 'et al' or 'and others'. Please avoid using these abbreviations and list all editors instead. Individual editors should be separated by 'and'.")
            verifybibtex_dict["errors"] += 1

def check_curly_braces(entry: bibtexparser.model.Entry,  verifybibtex_dict: Dict) -> None:
    ''' Function to check if a title includes many curly braces to secure capitalization. This might be intentional but could also lead to problems. Example: "Going {n}owhere: {A} {j}ourney to {heaven}"

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    if entry.fields_dict.get("title") == None:
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            "Entry has no title.")
        verifybibtex_dict["errors"] += 1
    else:
        title = entry["title"]
        # Count occurences if {}
        curly_braces_counter = title.count(r"{") if title is not None else 0
        if curly_braces_counter > 1:
            verifybibtex_dict["entries"][entry['ID']]["warning"].append(
                f"Found several {{}} groups in title. Please check if this is correct.")
            verifybibtex_dict["errors"] += 1

def check_double_curly_braces(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if some fields are wrapped in double curly braces. If so, warn the user.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    # Fields to ignore
    ignored_fields_list = [
        "pages",
        "volume",
        "number",
        "year",
        "date",
        "pubstate",
        "doi",
        "publisher",
        "address"
    ]
    # Create pattern to find double curly braces (in this case: only single braces) at start and end of string
    pattern = re.compile(r"^\{.*\}$")
    for key in entry.fields_dict.keys():
        if re.match(pattern, entry[key]) and key not in ignored_fields_list:
            # Check if string is really wrapped in curly braces or only starts and ends with pairs of braces
            # TODO: There are still uncaught cases maybe
            if len(entry[key]) < 4:  # make sure string is long enough for a check
                verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                    f"{key} field is wrapped in double curly braces.")
                verifybibtex_dict["errors"] += 1
            elif helper_check_curly_braces_pairs(entry[key][1:-1]):
                verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                    f"{key} field is wrapped in double curly braces.")
                verifybibtex_dict["errors"] += 1

def check_invalid_fields(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if a field is valid. For example, every field entry should end with a comma.
    
            Parameters
            ----------
                entry: bibtexparser.model.Entry
                    The bibtexparser.model.Entry with .bib entry from BibDatabase.        
                verifybibtex_dict: Dict
                    Dictionary to collect error messages for BibTex entries.

            Returns
            -------
                None
    '''
    raw_entry = entry.raw
    # Split the raw entry into lines
    raw_lines_list = raw_entry.split("\n")
    # Check if the entry has more than 3 lines (which is the minimum for a valid entry)
    if len(raw_lines_list) > 3: 
        for line in raw_lines_list[:-2]:
            # Make sure to skip empty lines
            if line.strip() != "":
                # Check if line ends with a comma
                if (line.strip().endswith(",") == False) and (line.strip()[-1] == "}"):
                    verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                        f"The following line does not end with a comma (which leads to parsing errors): {line}")
                    verifybibtex_dict["errors"] += 1

def check_incollection(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if a chapter entry (@incollection) includes all necessary information such as editors, booktitle, etc.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    if entry.fields_dict.get("editor") == None:
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            "This chapter has no editors. Is that correct?")
        verifybibtex_dict["errors"] += 1

    if entry.fields_dict.get("booktitle") == None:
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            "This chapter has no book title.")
        verifybibtex_dict["errors"] += 1

    if entry.fields_dict.get("year") == None and entry.fields_dict.get("date") == None and entry.fields_dict.get("pubstate") == None:
        verifybibtex_dict["entries"][entry['ID']]["critical"].append(
            "This chapter has no date of publication."
        )
        verifybibtex_dict["errors"] += 1

    if entry.fields_dict.get("pages") == None:
        verifybibtex_dict["entries"][entry['ID']]["warning"].append(
            "This chapter has no indicated page range. Please check if this is correct.")
        verifybibtex_dict["errors"] += 1

    if entry.fields_dict.get("publisher") == None:
        verifybibtex_dict["entries"][entry['ID']]["warning"].append(
            "This chapter has no publisher.")
        verifybibtex_dict["errors"] += 1

def check_parsing_errors(failed_blocks: bibtexparser.model.ParsingFailedBlock, verifybibtex_dict: Dict) -> None:
    """Function to check for parsing errors and add them to dictionary. bibtexparser 2.X needed!

        Parameters
        ----------
            failed_blocks : bibtexparser.model.ParsingFailedBlock
                List of failed blocks during parsing.
            verifybibtex_dict : Dict
                Dictionary to collect error messages for BibTex entries.

        Returns
        -------
            None
    """    
    for block in failed_blocks:
        verifybibtex_dict["general"].append(f"Parsing error occurred here: {block.raw}") # TODO: Exchange with block.error once this works
        verifybibtex_dict["errors"] += 1

def check_type_field(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    '''Function to check if an entry contains a type field.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.

        Returns
        -------
            None
    '''
    if entry.fields_dict.get("type") != None:
        verifybibtex_dict["entries"][entry['ID']]["warning"].append(
            "This entry contains a type field, which should generally be avoided.")
        verifybibtex_dict["errors"] += 1

def check_unescaped_characters(entry: bibtexparser.model.Entry, verifybibtex_dict: Dict) -> None:
    ''' Function to check if a field contains unescaped characters which should be escaped, such as &, #, or %. This might be intentional but could also lead to severe problems.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.

            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.
        Returns
        -------
            None
    '''
    for key in entry.fields_dict.keys():
        # First search for characters that should be escaped
        if re.search(r"\s&|\s#|\s%", entry[key]):
            verifybibtex_dict["entries"][entry['ID']]["critical"].append(
                f"{key} field contains unescaped characters (& or # or %). Please make sure to escape these characters using a backslash.")
            verifybibtex_dict["errors"] += 1
        if re.search(r"\s\$|\s\^|\s_|\s~", entry[key]):
            verifybibtex_dict["entries"][entry['ID']]["warning"].append(
                f"{key} field contains characters that might need to be escaped ($ or ^ or _ or ~). Please check if this is correct.")
            verifybibtex_dict["errors"] += 1

def create_verifybibtex_dictionary() -> Dict:
    '''Function to create a dictionary to collect error messages for BibTeX entries.

        Returns
        -------
            (Dict) Dictionary to collect error messages for BibTeX entries.

    '''

    return {
        "entries": dict(),
        "errors": 0,
        "general": list(),
    }

def helper_check_curly_braces_pairs(text: str) -> bool:
    '''Function to check if a string has matching curly braces pairs

        Parameters
        ----------
            text: str
                The text that should be checked.

        Returns
        -------
            (bool) True if pairs or no curly braces, False if there are braces with no corresponding closing/opening brace.

    '''
    braces_stack = list()
    for char in text:
        if char == r"{":
            braces_stack.append(r"{")
        if char == r"}":
            if not braces_stack:
                return False
            else:
                braces_stack.pop()

    return not braces_stack

def set_all_field_keys_lowercase(entry: bibtexparser.model.Entry) -> None:
    '''Function to set all field keys to lowercase.

        Parameters
        ----------
            entry: bibtexparser.model.Entry
                The dictionary with .bib entry from BibDatabase.
            
    '''
    for field in entry.fields:
        field.key = field.key.lower()

def write_output(verifybibtex_dict: Dict) -> None:
    '''Function to write the output of VerifyBibTex to a file.

        Parameters
        ----------
            verifybibtex_dict: Dict
                Dictionary to collect error messages for BibTex entries.

    '''
    with open("report/verifybibtex-report.md", "w") as file:
        # write general information
        file.write("# VerifyBibTex Report (1.0.0)\n\n")
        file.write("## General\n")
        for no,message in enumerate(verifybibtex_dict["general"]):
            file.write(f"{no+1}. {message}\n")
        file.write("\n")
        file.write(f"Found {verifybibtex_dict['errors']} errors.\n")

        # write specific information about entries
        file.write("\n")
        file.write("## Entries\n")
        for key, value in verifybibtex_dict["entries"].items():
            # skip if this entry has no errors
            if len(value["critical"]) == 0 and len(value["warning"]) == 0:
                continue
            file.write(f"### {key}\n")
            if len(value["critical"]) > 0:
                file.write(f"#### Important warnings\n")
                for no, message in enumerate(value["critical"]):
                    file.write(f"{no+1}. {message}\n")
                file.write("\n")
            if len(value["warning"]) > 0:
                file.write(f"#### Other warnings\n")
                for no,message in enumerate(value["warning"]):
                    file.write(f"{no+1}. {message}\n")
                file.write("\n")