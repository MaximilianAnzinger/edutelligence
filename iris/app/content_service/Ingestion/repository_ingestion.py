import os
from abc import ABC

import weaviate
from langchain.text_splitter import (
    Language,
    RecursiveCharacterTextSplitter,
)

from app.content_service.Ingestion.abstract_ingestion import AbstractIngestion
from app.llm import BasicRequestHandler
from app.llm.langchain.iris_langchain_embedding_model import IrisLangchainEmbeddingModel
from app.vector_database.repository_schema import (
    init_repository_schema,
    RepositorySchema,
)


def split_code(code: str, language: Language, chunk_size: int, chunk_overlap: int):
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=language, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return python_splitter.create_documents([code])


class RepositoryIngestion(AbstractIngestion, ABC):
    """
    Ingest the repositories into the weaviate database
    """

    def __init__(self, client: weaviate.WeaviateClient):
        self.collection = init_repository_schema(client)
        self.request_handler = BasicRequestHandler("gpt35")
        self.iris_embedding_model = IrisLangchainEmbeddingModel(self.request_handler)

    def chunk_files(self, path: str, programming_language: Language):
        """
        Chunk the code files in the root directory
        """
        chunk_size = 512
        overlap = 51
        files_contents = []
        for directory_path, subdir, files in os.walk(path):
            for filename in files:
                if filename.endswith("." + programming_language.value):
                    file_path = os.path.join(directory_path, filename)
                    with open(file_path, "r") as file:
                        code = file.read()
                    files_contents.append(
                        {
                            RepositorySchema.FILEPATH: filename,
                            RepositorySchema.CONTENT: code,
                        }
                    )
        for file in files_contents:
            chunks = split_code(
                file[RepositorySchema.CONTENT],
                programming_language.JAVA,
                chunk_size,
                overlap,
            )
            for chunk in chunks:
                files_contents.append(
                    {
                        RepositorySchema.CONTENT: chunk.page_content,
                        RepositorySchema.COURSE_ID: "tbd",
                        RepositorySchema.EXERCISE_ID: "tbd",
                        RepositorySchema.REPOSITORY_ID: "tbd",
                        RepositorySchema.FILEPATH: file[RepositorySchema.FILEPATH],
                    }
                )
        return files_contents

    def ingest(self, repo_path: str) -> bool:
        """
        Ingest the repositories into the weaviate database
        """
        chunks = self.chunk_files(repo_path)
        with self.collection.batch.dynamic() as batch:
            for index, chunk in enumerate(chunks):
                embed_chunk = self.iris_embedding_model.embed_query(
                    chunk[index][RepositorySchema.CONTENT]
                )
                batch.add_object(properties=chunk, vector=embed_chunk)
        return True
