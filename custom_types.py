import pydantic


class RAGChunkAndSrc(pydantic.BaseModel):
    chunk: list[str]
    source_id: str = None


class RAGUpsertresult(pydantic.BaseModel):
    inngested: int


class RAGSearchResult(pydantic.BaseModel):
    contexts: list[str]
    sources: list[str]


class RAGQueryResult(pydantic.BaseModel):
    answer: str
    sources: list[str]
    number_contexts: int