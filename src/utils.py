from datetime import datetime
import json


def read_json(url: str):
    with open(url, 'r', encoding='utf-8') as data_file:
        return json.load(data_file)
    

def write_json(url: str, data:list):
    with open(url, 'w', encoding='utf-8') as data_file:
        json.dump(data, data_file, indent=4)


def paginate_list(lista, page_number, page_size):
    """
    Function to paginate a list.

    Args:
    - lista: The list to paginate.
    - page_number: The desired page number (starting from 1).
    - page_size: The size of the page.

    Returns:
    - A tuple containing the current page and the total pages.
    """

    # Calculate the start and end index for the current page
    start = (page_number - 1) * page_size
    end = start + page_size

    # Get the current page from the list
    current_page = lista[start:end]

    # Calculate the total pages
    total_pages = len(lista) // page_size
    if len(lista) % page_size != 0:
        total_pages += 1

    return current_page, total_pages


def find_max_id(dictionary_list, field_name):
    """
    Function to find the maximum value of the 'id' field in a list of dictionaries.

    Args:
    - dictionary_list: The list of dictionaries to search for the maximum value of the 'id' field.
    - field_name: Name of de field in the dict

    Returns:
    - The maximum value of the 'id' field found in the list of dictionaries.
    """
    # Initialize the maximum value as None
    max_id = None
    
    # Iterate over each dictionary in the list
    for dictionary in dictionary_list:
        # Get the value of the 'field_name' field from the current dictionary
        current_id = int(dictionary.get(field_name))
        
        # Update the maximum value if the current 'field_name' field is greater
        if current_id is not None:
            if max_id is None or current_id > max_id:
                max_id = current_id
    
    return max_id


def get_current_date():
    # Obtener la fecha y hora actual
    current_date = datetime.now()

    # Formatear la fecha y hora actual según el formato deseado
    return current_date.strftime('%Y-%m-%dT%H:%M:%S')