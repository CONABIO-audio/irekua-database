from hypothesis import strategies as st


valid_string = lambda min_size: st.text(
    alphabet=st.characters(
        blacklist_categories=("Cs", "Cc"),
    ),
    min_size=min_size,
    max_size=64,
)


def get_schema_strategy(type, required=None, optional=None):
    if required is None:
        required = {}

    if optional is None:
        optional = {}

    return lambda: st.fixed_dictionaries(
        {"type": st.just(type), **required},
        optional={
            "title": valid_string(4),
            "description": valid_string(10),
            **optional,
        },
    )


string_schema = get_schema_strategy(
    "string",
    optional={
        "minLength": st.integers(min_value=0, max_value=10),
        "maxLength": st.integers(min_value=10),
    },
)


integer_schema = get_schema_strategy(
    "integer",
    optional={
        "multipleOf": st.integers(min_value=1),
        "minimum": st.integers(),
        "maximum": st.integers(),
    },
)


number_schema = get_schema_strategy(
    "number",
    optional={
        "multipleOf": st.floats(
            allow_nan=False, allow_infinity=False, min_value=0.1
        ),
        "minimum": st.floats(allow_nan=False, allow_infinity=False),
        "maximum": st.floats(allow_nan=False, allow_infinity=False),
    },
)

random_schema = get_schema_strategy(
    "object",
    required={
        "$id": valid_string(10),
        "$schema": st.just("http://json-schema.org/draft/2019-09/schema#"),
        "properties": st.dictionaries(
            valid_string(4),
            st.one_of(
                string_schema(),
                integer_schema(),
                number_schema(),
            ),
        ),
    },
    optional={
        "additionalProperties": st.booleans(),
    },
)
