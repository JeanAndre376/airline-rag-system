"""Airline RAG System - Data Preparation & Index Setup

This script:
1. Creates a Delta table with airline pricing knowledge chunks
2. Sets up Vector Search endpoint
3. Creates and syncs Vector Search index

Run this once to set up your RAG system.
"""

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.vectorsearch import (
    EndpointType, 
    DeltaSyncVectorIndexSpecRequest, 
    EmbeddingSourceColumn, 
    VectorIndexType, 
    PipelineType
)
from pyspark.sql import SparkSession, Row

# Configuration
CATALOG = "airlines"
SCHEMA = "silver_gold"
TABLE_NAME = "rag_knowledge_chunks"
ENDPOINT_NAME = "airline_rag_vs_endpoint"
INDEX_NAME = f"{CATALOG}.{SCHEMA}.rag_knowledge_index"
SOURCE_TABLE = f"{CATALOG}.{SCHEMA}.{TABLE_NAME}"
EMBEDDING_MODEL = "databricks-gte-large-en"

# Initialize clients
w = WorkspaceClient()
spark = SparkSession.builder.getOrCreate()


def create_knowledge_chunks():
    """Create Delta table with airline pricing knowledge chunks."""
    print("=" * 60)
    print("PHASE 1: DATA PREPARATION")
    print("=" * 60)
    
    # Knowledge base chunks
    chunks = [
        Row(
            id=1, 
            title="Fare Classes: Economy vs Business", 
            content="""Airlines segment tickets into fare classes, primarily Economy and Business (with some carriers also offering First and Premium Economy). Each class represents a different bundle of price, flexibility, and amenities — Business class typically includes more legroom, priority boarding, lounge access, and flexible change/cancellation policies, which is why it commands a significantly higher price than Economy. In this dataset, Business class flights average roughly 8x the price of Economy flights on the same routes."""
        ),
        Row(
            id=2, 
            title="Why Price Rises as Departure Approaches", 
            content="""Airlines use dynamic pricing and inventory management: each flight has a limited number of seats allocated to different price tiers within a fare class. As departure approaches, cheaper tiers typically sell out first, leaving only higher-priced seats available. In this dataset, average price rises sharply in the final few days before departure, then gradually declines and flattens out for bookings made 20+ days in advance."""
        ),
        Row(
            id=3, 
            title="Why Stops Affect Price", 
            content="""Direct flights are generally priced lower than one-stop or multi-stop itineraries. Connecting itineraries often combine two flight segments' worth of fare. In this dataset, average price increases from roughly ₹7,900 (zero stops) to ₹23,100 (one stop) to ₹24,600 (two or more stops)."""
        ),
        Row(
            id=4, 
            title="Airline Positioning: Full-Service vs Budget Carriers", 
            content="""Airlines fall into full-service network carriers and low-cost carriers. In this dataset, Vistara and Air India offer both Economy and Business class, positioning them as full-service carriers with higher average prices. SpiceJet, GO_FIRST, Indigo, and AirAsia offer Economy only, consistent with a budget carrier model."""
        ),
        Row(
            id=5, 
            title="Revenue Management and Yield", 
            content="""Airlines use revenue management systems to maximize revenue by balancing volume against yield. RM systems adjust which fare tiers are open based on booking pace and demand forecasts, which is why identical seats can sell at different prices depending on when booked. This dataset reflects historical average pricing patterns, not live inventory."""
        ),
        Row(
            id=6, 
            title="Route Pricing and Market Density", 
            content="""Route-level pricing is influenced by the number of competing airlines, route distance, and demand. In this dataset, all 30 routes are served by multiple airlines, so most routes show broadly similar average pricing (~₹22,000-25,000), with class and stops being the biggest price differentiators rather than route itself."""
        ),
        Row(
            id=7, 
            title="Dataset Scope and Limitations", 
            content="""This dataset covers domestic Indian flight listings across 6 airlines and 30 routes, with fields for airline, route, departure/arrival time buckets, stops, class, duration, days left before departure, and price. It does not include actual calendar dates, seasonality, real-time seat inventory, or competitor pricing. Predictions reflect booking-lead-time and route/class/airline patterns only."""
        )
    ]
    
    df_chunks = spark.createDataFrame(chunks)
    
    # Write to Delta with Change Data Feed enabled (required for Vector Search)
    print(f"\nCreating Delta table: {SOURCE_TABLE}")
    df_chunks.write.format("delta") \
        .mode("overwrite") \
        .option("delta.enableChangeDataFeed", "true") \
        .saveAsTable(SOURCE_TABLE)
    
    print(f"✓ Created table with {df_chunks.count()} chunks")
    print("\n" + "=" * 60)
    print("Phase 1 Complete")
    print("=" * 60)


def setup_vector_search():
    """Set up Vector Search endpoint and index."""
    print("\n" + "=" * 60)
    print("PHASE 2: VECTOR SEARCH SETUP")
    print("=" * 60)
    
    # Step 1: Create or get Vector Search endpoint
    print(f"\nStep 1: Setting up Vector Search endpoint...")
    try:
        endpoint = w.vector_search_endpoints.get_endpoint(ENDPOINT_NAME)
        print(f"✓ Endpoint '{ENDPOINT_NAME}' already exists")
        print(f"  Status: {endpoint.endpoint_status.state}")
    except Exception:
        print(f"Creating new endpoint '{ENDPOINT_NAME}'...")
        endpoint = w.vector_search_endpoints.create_endpoint_and_wait(
            name=ENDPOINT_NAME,
            endpoint_type=EndpointType.STANDARD
        )
        print(f"✓ Endpoint created: {endpoint.name}")
    
    # Step 2: Create Vector Search index
    print(f"\nStep 2: Creating Vector Search index...")
    print(f"  Source table: {SOURCE_TABLE}")
    print(f"  Embedding model: {EMBEDDING_MODEL}")
    
    try:
        # Create the embedding source column spec
        embedding_col = EmbeddingSourceColumn(
            name="content",
            embedding_model_endpoint_name=EMBEDDING_MODEL
        )
        
        # Create the delta sync spec
        delta_spec = DeltaSyncVectorIndexSpecRequest(
            source_table=SOURCE_TABLE,
            pipeline_type=PipelineType.TRIGGERED,
            embedding_source_columns=[embedding_col]
        )
        
        # Create the index
        index = w.vector_search_indexes.create_index(
            name=INDEX_NAME,
            endpoint_name=ENDPOINT_NAME,
            primary_key="id",
            index_type=VectorIndexType.DELTA_SYNC,
            delta_sync_index_spec=delta_spec
        )
        
        print(f"✓ Index creation initiated: {INDEX_NAME}")
        print("\n⏳ Index is now syncing (this can take a few minutes)...")
        
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✓ Index '{INDEX_NAME}' already exists")
        else:
            raise
    
    print("\n" + "=" * 60)
    print("Phase 2 Complete - Index syncing in background")
    print("=" * 60)


def check_index_status():
    """Check if Vector Search index is ready."""
    print("\n" + "=" * 60)
    print("CHECKING INDEX STATUS")
    print("=" * 60)
    
    index = w.vector_search_indexes.get_index(INDEX_NAME)
    
    if index.status.ready:
        print(f"\n✅ INDEX IS READY!")
        print(f"   Indexed {index.status.indexed_row_count} rows")
        print("\n✅ Setup Complete! Your RAG system is ready to use.")
        print("\nNext steps:")
        print("  1. Import: from rag_system import ask_rag")
        print("  2. Query: ask_rag('Why is Business class expensive?')")
    else:
        print(f"\n⏳ Still provisioning...")
        print(f"   Status: {index.status.message}")
        print("\nWait another minute and run check_index_status() again.")
    
    print("=" * 60)


if __name__ == "__main__":
    print("\nAirline RAG System - Setup")
    print("=" * 60)
    
    # Run setup
    create_knowledge_chunks()
    setup_vector_search()
    
    print("\n" + "=" * 60)
    print("SETUP INITIATED")
    print("=" * 60)
    print("\nThe Vector Search index is now syncing.")
    print("This typically takes 2-5 minutes.")
    print("\nRun check_index_status() to verify when ready.")
    print("=" * 60)
