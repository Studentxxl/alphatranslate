def check_symbols(obj: str, forbidden_symbols: list):
    for i in obj:
        if i in forbidden_symbols:
            return False
    return True


