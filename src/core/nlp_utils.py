def get_smells_by_ambiguity_type(ambiguity_types:list, smells:list):    
    result = []
    
    for elemento in smells:
        print(elemento)
        print(ambiguity_types)
        # Verificar si alguno de los campos especificados es "X"
        if any(elemento[campo] == 'X' for campo in ambiguity_types):
            result.append(elemento['word'].upper())

    return list(set(result))

