from functions import check_invalid_fields, set_all_field_keys_lowercase, check_article_doi
import bibtexparser # type: ignore

def test_check_invalid_fields_1():
    '''Check several possible errors caught.'''
    # load file
    lib = bibtexparser.parse_file("test/testbib.bib")
    # create dummy dict
    verifybibtex_dict = {
        'entries': {
            'scikit-learn': {
                'critical': [],
            },
            'scikit-learn2': {
                'critical': [],
            },
            'banisch2021': {
                'critical': [],
            }
        },
        'errors': 0
    }
    
    # setting all keys lowercase
    set_all_field_keys_lowercase(lib.entries[0])
    set_all_field_keys_lowercase(lib.entries[1])
    set_all_field_keys_lowercase(lib.entries[2])

    # check if missing commas are not misinterpreted
    check_invalid_fields(lib.entries[0], verifybibtex_dict)
    assert verifybibtex_dict['entries']['scikit-learn']['critical'] == []
    # check if missing comma after author field is caught
    check_invalid_fields(lib.entries[1], verifybibtex_dict)
    assert verifybibtex_dict['entries']['scikit-learn2']['critical'] == ['The following line does not end with a comma (which leads to parsing errors): \tauthor={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.}']
    # check if no missing doi error is raised
    check_article_doi(lib.entries[2], verifybibtex_dict)
    assert verifybibtex_dict['entries']['banisch2021']['critical'] == []

    assert verifybibtex_dict['errors'] == 1
    
    
    