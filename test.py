def remove_extension(filename):
    """
    This function takes a file name with extension and returns the file name without the extension.
    """
    dot_index = filename.rfind('.')
    if dot_index == -1:
        return filename
    else:
        return filename[:dot_index]
print(remove_extension('asd.9.23.2030.pdf'))