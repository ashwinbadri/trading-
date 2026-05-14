from app.tools.tool_registry import tool_registry


print("Available tools:")

for name, tool in tool_registry.items():
    print(f"- {name}: {tool['description']}")


print("\nCalling get_stock_data tool:")

get_stock_data = tool_registry["get_stock_data"]["function"]

result = get_stock_data("AAPL")

print(result)