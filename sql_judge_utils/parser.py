import re


def get_queries(file_path: str, separator_prefix="-- Section"):
    with open(file_path) as file_object:
        file_content = file_object.read().strip()
    sections = re.split(rf"{re.escape(separator_prefix)}\d+", file_content)
    sections = [s for s in sections if s]
    return sections


def get_query(file_path: str, query_number: int, separator_prefix="-- Section"):
    queries = get_queries(file_path, separator_prefix=separator_prefix)
    query = queries[query_number] if query_number < len(queries) else None
    return query
