import logging

from haystack_astra_utils import EMBEDDING_MODEL_NAME, ASTRA_DB_ID, ASTRA_DB_REGION, ASTRA_DB_KEYSPACE_NAME, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_COLLECTION_NAME

from haystack import Document, Pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

from astra_haystack.document_store import AstraDocumentStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# embedding_dim is the number of dimensions the embedding model supports.
document_store = AstraDocumentStore(
    astra_id=ASTRA_DB_ID,
    astra_region=ASTRA_DB_REGION,
    astra_collection=ASTRA_DB_COLLECTION_NAME,
    astra_keyspace=ASTRA_DB_KEYSPACE_NAME,
    astra_application_token=ASTRA_DB_APPLICATION_TOKEN,
    duplicates_policy=DuplicatePolicy.SKIP,
    embedding_dim=384,
)


# Add Documents
documents = [
    Document(content="There are over 7,000 languages spoken around the world today."),
    Document(
        content="Elephants have been observed to behave in a way that indicates"
        " a high level of self-awareness, such as recognizing themselves in mirrors."
    ),
    Document(
        content="In certain parts of the world, like the Maldives, Puerto Rico, "
        "and San Diego, you can witness the phenomenon of bioluminescent waves."
    ),
]
logger.info(f"Adding {len(documents)} documents to the document store.")

index_pipeline = Pipeline()
index_pipeline.add_component(
    instance=SentenceTransformersDocumentEmbedder(model=EMBEDDING_MODEL_NAME),
    name="embedder"
)
index_pipeline.add_component(instance=DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP), name="writer")
index_pipeline.connect("embedder.documents", "writer.documents")

index_pipeline.run({"embedder": {"documents": documents}})

print(document_store.count_documents())
