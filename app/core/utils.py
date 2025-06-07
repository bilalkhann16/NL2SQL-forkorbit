def create_text_prompt_from_list(schema_list):
    """
    Convert a list of schema dictionaries to a formatted text representation.

    Args:
        schema_list (list): List of dictionaries containing schema information

    Returns:
        str: Formatted text string with schema hierarchy
    """
    output = []

    for schema_dict in schema_list:
        for schema_name, tables in schema_dict.items():
            # Add schema header
            output.append(f"Schema: {schema_name}\n")

            for table_name, columns in tables.items():
                # Add table header
                output.append(f"Table: {table_name}\n")
                output.append("Columns:")

                # Add columns with their properties
                for idx, column in enumerate(columns, 1):
                    output.append(f"{idx}. {column['column_name']}")
                    output.append(f"   - Data Type: {column['data_type']}")
                    output.append(f"   - Max Length: {column['max_length']}")
                    output.append(f"   - Precision: {column['precision']}")
                    output.append(f"   - Scale: {column['scale']}")
                    output.append(
                        f"   - Nullable: {'Yes' if column['is_nullable'] else 'No'}"
                    )
                    output.append(
                        f"   - Identity: {'Yes' if column['is_identity'] else 'No'}"
                    )
                    output.append("")  # Empty line between columns

                output.append("")  # Empty line between tables

            output.append("")  # Empty line between schemas

    return "\n".join(output)
