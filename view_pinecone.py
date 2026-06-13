"""Script to view vectors stored in Pinecone."""
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def view_pinecone_data():
    """Display information about vectors in Pinecone."""
    
    # Initialize Pinecone
    api_key = os.getenv('PINECONE_API_KEY')
    index_name = os.getenv('PINECONE_INDEX_NAME')
    
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    
    print("=" * 80)
    print("📌 PINECONE VECTOR DATABASE")
    print("=" * 80)
    
    # Get index stats
    stats = index.describe_index_stats()
    
    print(f"\n📊 Index: {index_name}")
    print("-" * 80)
    print(f"  Total Vectors: {stats.total_vector_count}")
    print(f"  Dimension: {stats.dimension}")
    
    if hasattr(stats, 'namespaces') and stats.namespaces:
        print(f"\n  Namespaces:")
        for ns_name, ns_stats in stats.namespaces.items():
            ns_display = ns_name if ns_name else "(default)"
            print(f"    - {ns_display}: {ns_stats.vector_count} vectors")
    
    print("\n🔍 Sample Vectors (first 5):")
    print("-" * 80)
    
    # Query to get some vectors (using a zero vector just to list)
    try:
        # Fetch some vector IDs by querying
        results = index.query(
            vector=[0.0] * 384,  # Dummy vector
            top_k=5,
            include_metadata=True
        )
        
        if results.matches:
            for i, match in enumerate(results.matches, 1):
                print(f"\n  {i}. Vector ID: {match.id}")
                if match.metadata:
                    print(f"     Document ID: {match.metadata.get('document_id', 'N/A')}")
                    print(f"     Filename: {match.metadata.get('source_filename', 'N/A')}")
                    print(f"     Chunk Index: {match.metadata.get('chunk_index', 'N/A')}")
                    print(f"     Strategy: {match.metadata.get('strategy', 'N/A')}")
                    text = match.metadata.get('text', '')
                    preview = text[:100] + "..." if len(text) > 100 else text
                    print(f"     Text Preview: {preview}")
        else:
            print("\n  No vectors found in query results.")
            
    except Exception as e:
        print(f"\n  Could not fetch sample vectors: {e}")
    
    print("\n" + "-" * 80)
    print("\n✅ Pinecone check complete!\n")

if __name__ == "__main__":
    view_pinecone_data()
