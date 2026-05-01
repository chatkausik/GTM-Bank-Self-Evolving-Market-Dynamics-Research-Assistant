import json
import chromadb
from .models import Memory


class ReasoningBank:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="gtm_memories",
            metadata={"hnsw:space": "cosine"},
        )

    def add_memory(self, memory: Memory) -> str:
        document_text = f"{memory.title}\n{memory.description}\n{memory.content}\n" + \
                        "\n".join(memory.lessons)
        self.collection.add(
            ids=[memory.id],
            documents=[document_text],
            metadatas=[{
                "title": memory.title,
                "description": memory.description,
                "content": memory.content,
                "outcome_type": memory.outcome_type,
                "merchant_segment": memory.merchant_segment,
                "pdlc_phase": memory.pdlc_phase,
                "product_category": memory.product_category,
                "lessons": json.dumps(memory.lessons),
                "competitor_context": memory.competitor_context or "",
                "timestamp": memory.timestamp,
                "source": memory.source,
            }],
        )
        return memory.id

    def memory_exists(self, memory_id: str) -> bool:
        result = self.collection.get(ids=[memory_id])
        return len(result["ids"]) > 0

    def retrieve_similar(
        self,
        query: str,
        n_results: int = 6,
        outcome_filter: str | None = None,
    ) -> list[dict]:
        total = self.collection.count()
        if total == 0:
            return []

        where = {"outcome_type": outcome_filter} if outcome_filter else None
        actual_n = min(n_results, total)

        results = self.collection.query(
            query_texts=[query],
            n_results=actual_n,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        memories = []
        for i, mem_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            memories.append({
                "id": mem_id,
                "title": meta["title"],
                "description": meta["description"],
                "content": meta["content"],
                "outcome_type": meta["outcome_type"],
                "merchant_segment": meta["merchant_segment"],
                "product_category": meta["product_category"],
                "lessons": json.loads(meta["lessons"]),
                "competitor_context": meta["competitor_context"],
                "timestamp": meta["timestamp"],
                "source": meta["source"],
                "relevance_score": round(1 - results["distances"][0][i], 3),
            })
        return memories

    def get_all_memories(self) -> list[dict]:
        if self.collection.count() == 0:
            return []
        results = self.collection.get(include=["metadatas"])
        memories = []
        for i, mem_id in enumerate(results["ids"]):
            meta = results["metadatas"][i]
            memories.append({
                "id": mem_id,
                "title": meta["title"],
                "description": meta["description"],
                "outcome_type": meta["outcome_type"],
                "merchant_segment": meta["merchant_segment"],
                "product_category": meta["product_category"],
                "timestamp": meta["timestamp"],
                "source": meta["source"],
            })
        memories.sort(key=lambda m: m["timestamp"], reverse=True)
        return memories

    def get_stats(self) -> dict:
        all_memories = self.get_all_memories()
        successes = sum(1 for m in all_memories if m["outcome_type"] == "success")
        failures = sum(1 for m in all_memories if m["outcome_type"] == "failure")
        segments = list({m["merchant_segment"] for m in all_memories})
        categories = list({m["product_category"] for m in all_memories})
        return {
            "total": len(all_memories),
            "successes": successes,
            "failures": failures,
            "unique_segments": len(segments),
            "unique_categories": len(categories),
        }
