import os
import arxiv
import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
chroma_client = chromadb.PersistentClient(path="./data/chroma")
collection = chroma_client.get_or_create_collection(name="papers")


def fetch_and_store_papers(query: str, max_results: int = 5):
    """arXivから論文を取得してChromaDBに保存する"""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    stored = []
    for paper in search.results():
        doc_id = paper.entry_id.split("/")[-1]
        collection.upsert(
            ids=[doc_id],
            documents=[f"{paper.title}\n{paper.summary}"],
            metadatas=[{
                "title": paper.title,
                "url": paper.entry_id,
                "published": str(paper.published)
            }]
        )
        stored.append(paper.title)

    return stored


def search_and_answer(question: str, n_results: int = 3):
    """質問に関連する論文を検索してClaudeに回答させる"""
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    if not results["documents"][0]:
        return "関連する論文が見つかりませんでした。先に論文を取得してください。"

    context = "\n\n".join(results["documents"][0])
    titles = [m["title"] for m in results["metadatas"][0]]

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""以下の論文の情報をもとに質問に答えてください。

論文情報:
{context}

質問: {question}

日本語で回答してください。"""
        }]
    )

    return {
        "answer": message.content[0].text,
        "sources": titles
    }