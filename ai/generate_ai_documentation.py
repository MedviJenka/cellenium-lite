import os
import openai
import faiss
import numpy as np
from dataclasses import dataclass
from infrastructure.data.constants import GLOBAL_PATH


class BiniDoc:
    def __init__(self) -> None:
        self.project_data = []

    def extract_project_data(self):
        project_data = []
        for root, _, files in os.walk(GLOBAL_PATH):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            project_data.append({"file": file_path, "content": content})
                    except UnicodeDecodeError:
                        print(f"Skipping non-UTF-8 file: {file_path}")
        print(f"Extracted {len(project_data)} Python files.")
        return project_data

    def generate_embeddings(self, model="text-embedding-ada-002"):
        self.project_data = self.extract_project_data()
        if not self.project_data:
            raise ValueError("No project data found. Ensure GLOBAL_PATH is correct and contains .py files.")

        for item in self.project_data:
            try:
                embedding_response = openai.Embedding.create(input=item["content"], model=model)
                item["embedding"] = embedding_response["data"][0]["embedding"]
                print(f"Generated embedding for file: {item['file']}")
            except Exception as e:
                print(f"Failed to generate embedding for {item['file']}: {e}")
        return self.project_data


@dataclass
class VectorDB:
    bini_doc: BiniDoc

    def __post_init__(self):
        self.data = self.bini_doc.generate_embeddings()
        self.index = self.create_index()

    def create_index(self):
        if not self.data or not any("embedding" in item for item in self.data):
            raise ValueError("No embeddings found to index. Ensure embedding generation is successful.")

        dimension = len(self.data[0]["embedding"])
        index = faiss.IndexFlatL2(dimension)
        vectors = np.array([item["embedding"] for item in self.data if "embedding" in item]).astype("float32")
        index.add(vectors)
        self.metadata = {i: item for i, item in enumerate(self.data) if "embedding" in item}
        return index

    def query(self, embedding, k=5):
        distances, indices = self.index.search(np.array([embedding]).astype("float32"), k)
        results = [self.metadata[i] for i in indices[0]]
        return results


class QueryDB:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def query_project(self, query, k=5):
        from dotenv import load_dotenv
        load_dotenv()
        openai.api_key_path = os.getenv('OPENAI_API_KEY')

        try:
            query_embedding = openai.Embedding.create(
                input=query, model="text-embedding-ada-002"
            )["data"][0]["embedding"]
            return self.vector_db.query(query_embedding, k)
        except Exception as e:
            print(f"Failed to query the project: {e}")
            return []

    def execute(self, query: str) -> None:
        results = self.query_project(query)
        if not results:
            print("No relevant results found.")
            return

        context = "\n".join(
            [f"File: {item['file']}\nContent:\n{item['content']}" for item in results]
        )
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a documentation assistant."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ]
        )
        print("\nGenerated Answer:\n")
        print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    bini_doc = BiniDoc()
    vector_db = VectorDB(bini_doc)
    query_db = QueryDB(vector_db)

    print("Generative AI Documentation System Initialized!")
    while True:
        user_query = input("\nYour Query: ")
        if user_query.strip():
            query_db.execute(user_query)
