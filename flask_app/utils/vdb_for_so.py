from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _scrap_texts_from_dir(path: str) -> list:
    """Подготавливает текста из директории."""
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Папка не найдена: {path}")

    text_loader = DirectoryLoader(path)
    loader = text_loader.load()
    return loader


def split_text(path, chunk_size, overlap, len_fn, is_separator_regex):
    """Сплитит текст используя RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len_fn,
        is_separator_regex=is_separator_regex
    )

    treated_research_paper = _scrap_texts_from_dir(path)
    chunks = text_splitter.split_documents(treated_research_paper)
    return chunks


TEXTS_PATH = os.path.join(BASE_DIR, 'text_database', 'socionics_texts')
BEHAV_PATH = os.path.join(BASE_DIR, 'text_database', 'socionics_behav')
VECTOR_DIR = os.path.join(BASE_DIR, 'vectors_db')

for p in [TEXTS_PATH, BEHAV_PATH]:
    if not os.path.exists(p):
        print(f"⚠️  Создай папку: {p}")

treated_texts = split_text(TEXTS_PATH, 6000, 300, len, is_separator_regex=False)
treated_texts_behav = split_text(BEHAV_PATH, 2125, 100, len, is_separator_regex=False)

embeddings = OllamaEmbeddings(model='nomic-embed-text-v2-moe')


def _init_hybrid_retriever(texts, k: int, fetch_k: int, lambda_mult: float, persistent_directory: str):
    """Инициализирует ретривер гибридного типа BM25 + Vector search."""

    bm25_retr = BM25Retriever.from_documents(texts)
    bm25_retr.k = k

    os.makedirs(persistent_directory, exist_ok=True)

    db = Chroma.from_documents(texts, embedding=embeddings, persist_directory=persistent_directory)
    retriver_soc = db.as_retriever(
        search_type='mmr',
        search_kwargs={"k": k, 'fetch_k': fetch_k, "lambda_mult": lambda_mult}
    )

    return retriver_soc, bm25_retr


def hybrid_retriever(texts, first_steps_k, fetch_k, lambda_mult, vector_weight, bm25_weights, persistent_directory):
    """Создает ретривер гибридного типа BM25 + Vector search через EnsembleRetriever."""
    retriever_soc, bm25_retr = _init_hybrid_retriever(
        texts, first_steps_k, fetch_k, lambda_mult, persistent_directory
    )

    ensemble_retriever = EnsembleRetriever(
        retrievers=[retriever_soc, bm25_retr],
        weights=[vector_weight, bm25_weights]
    )

    return ensemble_retriever


retriever_soc = hybrid_retriever(
    treated_texts, 2, 60, 0.25, 0.80, 0.20,
    os.path.join(VECTOR_DIR, 'chroma_socionics')
)
retriever_soc_behav = hybrid_retriever(
    treated_texts_behav, 2, 30, 0.35, 0.70, 0.30,
    os.path.join(VECTOR_DIR, 'chroma_socionics_behav')
)
