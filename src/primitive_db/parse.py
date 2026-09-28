def parse_clause(clause_tokens: list[str]) -> dict | None:
    """Превращает ['age', '=', '28'] в {'age': 28}"""
    if not clause_tokens:
        return None
    
    clause_str = " ".join(clause_tokens)
    if "=" not in clause_str:
        print(f'Ошибка: Неверный формат выражения "{clause_str}". Ожидается: поле = значение')
        return None
        
    key, val = clause_str.split("=", 1)
    key = key.strip()
    val = val.strip().strip("'\"")
    
    if val.isdigit():
        parsed_val = int(val)

    elif val.lower() in ("true", "false"):
        parsed_val = val.lower() == "true"

    else:
        parsed_val = val

    return {key: parsed_val}
