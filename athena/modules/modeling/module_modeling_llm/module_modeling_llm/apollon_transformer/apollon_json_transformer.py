import json

from module_modeling_llm.apollon_transformer.parser.uml_parser import UMLParser


class ApollonJSONTransformer:

    @staticmethod
    def transform_json(model: str) -> tuple[str, dict[str, str], str, dict[str, str]]:
        """
        Serialize a given Apollon diagram model to a string representation.
        This method converts the UML diagram model into a format similar to mermaid syntax, called "apollon".
    
        :param model: The Apollon diagram model to serialize.
        :return: A tuple containing the serialized model as a string and a dictionary mapping element and relation names
                 to their corresponding IDs.
        """

        model_dict = json.loads(model)

        parser = UMLParser(model_dict)

        diagram_type = model_dict.get("type", "unknown")
    
        # Convert the UML diagram to the apollon representation
        apollon_representation = parser.to_apollon()
    
        # Get the mapping of element, method, and attribute names to their corresponding IDs
        # This is used to resolve references to as the apollon representation only contains names and not IDs
        names = parser.get_element_id_mapping()

        id_type_mapping = parser.get_id_to_type_mapping()

        return apollon_representation, names, diagram_type, id_type_mapping
    