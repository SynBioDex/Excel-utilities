import re

def check_name(nm_to_chck):
    """the function verifies that the names is alphanumeric and
    separated by underscores if that is not the case the special characters are
    replaced by their unicode decimal code number

    Args:
        nm_to_chck (string): the name to be checked

    Returns:
        compliant_name (string): alphanumberic name with special
                                 characters replaced by _u###_
    """

    if not bool(re.match('^[a-zA-Z0-9]+$', nm_to_chck)):
        # replace special characters with numbers
        for ltr in nm_to_chck:
            if ord(ltr) > 122 or ord(ltr) < 48:
                # 122 is the highest decimal code number
                # for common latin ltrs or arabic numbers
                # this helps identify special characters like
                # ä or ñ, which isalnum() returns as true
                # the characters that don't meet this criterion are replaced
                # by their decimal code number separated by an underscore
                nm_to_chck = nm_to_chck.replace(ltr, str(f"_u{ord(ltr)}_"))
                # new_ltr = str(ltr.encode("unicode_escape"))
                # new_ltr = new_ltr.replace(r"b'\\", "").replace("'", "")
                # nm_to_chck = nm_to_chck.replace(ltr, f'_{new_ltr}_')
            elif ord(ltr) == 32:
                nm_to_chck = nm_to_chck.replace(ltr, "_")
            else:
                # remove all letters, numbers and whitespaces
                ltr = re.sub(r'[\w, \s]', '', ltr)
                # this enables replacing all other
                # special characters that are under 122
                if len(ltr) > 0:
                    nm_to_chck = nm_to_chck.replace(ltr, str(f"_u{ord(ltr)}_"))
    if len(nm_to_chck) > 0:
        if nm_to_chck[0].isnumeric():
            # ensures it doesn't start with a number
            nm_to_chck = f"_{nm_to_chck}"

    return(nm_to_chck)