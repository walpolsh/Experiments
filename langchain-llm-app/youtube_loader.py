from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
video_url = "https://youtu.be/lG7Uxts9SXs?si=yk3-hTH3YFinYvPW"
def create_vector_db_from_url(video__url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video__url)
    transcript = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs, embeddings)
    return db

def get_response_from_query(db, query, k=4):
    # 4097 tokens per req max
    # k is the number of documents to send, chunk size 1000*4 = 4000
    docs = db.similarity_search(query, k) 
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = OpenAI(
        model ="text-davinci-003"
    )
    prompt = PromptTemplate(
        input_variable = ["question", "docs"],
        template=f"""
            You are a helpful assistant. 
            Answer the following question: {question}
            By searching the following transcript: {docs}
        """
    )
    chain = LLMChain(llm = llm, prompt = prompt)
    response = chain.run(question=query, docs = docs_page_content).replace("\n", "")
    return response




