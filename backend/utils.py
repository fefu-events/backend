def encode_query_params(params: dict[str, any]) -> str:
    result = "?"
    processed_params_in_list: list[str] = []
    for name, value in params.items():
        if type(value) == list:
            for item in value:
                processed_params_in_list.append(
                    f"{name}={item}"
                )
        elif type(value) == bool:
            processed_params_in_list.append(
                f"{name}={value}"
            )
        elif value is None:
            continue
        else:
            processed_params_in_list.append(
                f"{name}={value}"
            )

    return f"{result}{'&'.join(processed_params_in_list)}"
