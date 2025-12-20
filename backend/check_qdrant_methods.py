from qdrant_client import QdrantClient

# Create a client instance (without connecting to check methods)
# We'll create it with a dummy URL to avoid actual connection
client = QdrantClient(url="http://localhost:6333")

# List all available methods
print("Available methods in QdrantClient:")
methods = [method for method in dir(client) if not method.startswith('_')]
for method in sorted(methods):
    print(f"  {method}")

# Look specifically for search-related methods
print("\nSearch-related methods:")
search_methods = [method for method in methods if 'search' in method.lower()]
for method in search_methods:
    print(f"  {method}")