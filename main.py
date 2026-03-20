import logging 
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage

from custom_types import RAGChunkAndSrc, RAGUpsertresult, RAGSearchResult, RAGQueryResult








load_dotenv()


inngest_client=inngest.Inngest(
    app_id="rag _app",
    logger=logging.getLogger('uvicorn'),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)



@inngest_client.create_function(
    fn_id="RAG: Inngest_PDF",
    trigger=inngest.TriggerEvent(event="rag/inngest_pdf")
)
async def rag_inngest_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id",pdf_path) # if source_id is not provided, use pdf_path as source_id
        chunks = load_and_chunk_pdf(pdf_path)

        return RAGChunkAndSrc(
            chunks=chunks,
            source_id=source_id
        )

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertresult:
        pass

    chunks_and_src = await ctx.step.run("load-and-chunk",lambda: _load(ctx),output_type=RAGChunkAndSrc)
    inngested =  await  ctx.step.run("embed-and-upsert",lambda: _upsert(chunks_and_src),output_type=RAGUpsertresult)

    return inngested.model_dump()

##model_dump is a pydantic method that converts the pydantic model to a dictionary. This is necessary because the inngest function needs to return a dictionary that can be serialized to JSON.


    

app = FastAPI()


inngest.fast_api.serve(app,inngest_client,[rag_inngest_pdf])