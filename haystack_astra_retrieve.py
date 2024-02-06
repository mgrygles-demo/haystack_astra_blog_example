import logging
import pprint

from haystack_astra_utils import OPENAI_API_KEY, EMBEDDING_MODEL_NAME, ASTRA_DB_ID, ASTRA_DB_REGION, ASTRA_DB_KEYSPACE_NAME, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_COLLECTION_NAME
from haystack import Pipeline 
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from astra_haystack.retriever import AstraRetriever
from astra_haystack.document_store import AstraDocumentStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

prompt_template = """
                Given these documents, answer the question.
                Documents:
                {% for doc in documents %}
                    {{ doc.content }}
                {% endfor %}
                Question: {{question}}
                Answer:
                """
                
document_store = AstraDocumentStore(
    astra_id=ASTRA_DB_ID,
    astra_region=ASTRA_DB_REGION,
    astra_collection=ASTRA_DB_COLLECTION_NAME,
    astra_keyspace=ASTRA_DB_KEYSPACE_NAME,
    astra_application_token=ASTRA_DB_APPLICATION_TOKEN,
    duplicates_policy="skip",
    embedding_dim=384
)
    

rag_pipeline = Pipeline()
rag_pipeline.add_component(
    instance=SentenceTransformersTextEmbedder(model=EMBEDDING_MODEL_NAME),
    name="embedder",
)
rag_pipeline.add_component(instance=AstraRetriever(document_store=document_store), name="retriever")
rag_pipeline.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
rag_pipeline.add_component(instance=OpenAIGenerator(api_key=OPENAI_API_KEY), name="llm")
rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
rag_pipeline.connect("embedder", "retriever")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("llm.meta", "answer_builder.meta")
rag_pipeline.connect("retriever", "answer_builder.documents")

logger.info("Pipeline created")

# Run the pipeline
question = "How many languages are there in the world today?"
##question = "Tell me something about a killer whale"
result = rag_pipeline.run(
    {
        "embedder": {"text": question},
        "retriever": {"top_k": 1},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

logger.info(result)

pp = pprint.PrettyPrinter(width=60)
pp.pprint(result)
