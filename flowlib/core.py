def pipeline(data, funcs):
    for func in funcs:
        data = func(data)
    return data
