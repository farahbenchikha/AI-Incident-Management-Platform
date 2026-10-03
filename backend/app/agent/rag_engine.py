import os
import glob
from typing import List, Dict, Any

class SimpleRAGEngine:
    """
    Moteur RAG (Retrieval-Augmented Generation) pour la base de connaissances SRE.
    Permet de découper les Runbooks SRE, calculer la similarité et retourner les procédures d'incident.
    """
    def __init__(self, runbooks_dir: str = "rag_docs/runbooks"):
        self.runbooks_dir = runbooks_dir
        self.documents: List[Dict[str, str]] = []
        self._load_documents()

    def _load_documents(self):
        """Charge tous les fichiers Runbooks Markdown (.md) présents dans le dossier."""
        self.documents = []
        files = glob.glob(os.path.join(self.runbooks_dir, "*.md"))
        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents.append({
                        "filename": os.path.basename(fpath),
                        "filepath": fpath,
                        "content": content
                    })
            except Exception as e:
                print(f"Erreur lors de la lecture de {fpath}: {e}")

    def search_similar_runbook(self, incident_query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Recherche sémantique basique par mots-clés et correspondance TF-IDF / termes SRE.
        Retourne les Runbooks les plus pertinents avec leur score de pertinence.
        """
        query_terms = set(incident_query.lower().split())
        results = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            score = 0
            
            # Calcul de pertinence basé sur la présence des termes clés SRE
            for term in query_terms:
                if len(term) > 2 and term in content_lower:
                    score += content_lower.count(term)
            
            if score > 0:
                results.append({
                    "filename": doc["filename"],
                    "score": score,
                    "content": doc["content"]
                })

        # Trier par score décroissant
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Instance globale
rag_engine = SimpleRAGEngine()
