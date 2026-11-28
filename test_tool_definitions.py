

from tool_definitions import TOOLS
from fintech_tools import AVAILABLE_TOOLS


def main():

    print("\n========== TOOL DEFINITION TEST ==========")

    print("Total defined tools:", len(TOOLS))

    for tool in TOOLS:

        function = tool["function"]

        name = function["name"]

        print("\nTool name:", name)
        print("Description:", function["description"])

        assert tool["type"] == "function"
        assert name in AVAILABLE_TOOLS

        parameters = function["parameters"]

        assert parameters["type"] == "object"
        assert "properties" in parameters

        for required_field in parameters["required"]:
            assert required_field in parameters["properties"]

        print("Schema validation: PASS")
        print("Python implementation: PASS")

    assert len(TOOLS) == 3

    print("\n==========================================")
    print("ALL TOOL DEFINITION TESTS PASSED")
    print("==========================================")


if __name__ == "__main__":
    main()
