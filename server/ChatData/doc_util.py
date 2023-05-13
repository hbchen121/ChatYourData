from PyPDF2 import PdfReader
import sys
import os
import os.path as osp
import logging
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, QuestionAnswerPrompt, LLMPredictor, \
    SimpleWebPageReader
from llama_index import ServiceContext
from langchain import OpenAI
from utils.consts import BASE_DIR
from epub2txt import epub2txt
import docx2txt

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

OPENAI_API_KEY = "OPENAI_API_KEY"
# OPENAI_API_KEY = ""

QUESTION_ANSWER_PROMPT_TMPL_2 = """
You are an AI assistant providing helpful advice. You are given the following extracted parts of a long document and a question. Provide a conversational answer based on the context provided.
If you can't find the answer in the context below, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
Context information is below.
=========
{context_str}
=========
{query_str}
"""

QA_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "{query_str}\n"
)


def set_api_key(api_key):
    global OPENAI_API_KEY
    OPENAI_API_KEY = api_key
    api_file = "api_key.txt"
    api_file_path = osp.join(BASE_DIR, api_file)
    with open(api_file_path, "w") as f:
        f.write(OPENAI_API_KEY)


def load_api_key():
    api_file = "api_key.txt"
    api_file_path = osp.join(BASE_DIR, api_file)
    if not osp.isfile(api_file_path):
        return ""
    with open(api_file_path, "r") as f:
        api_key = f.read()
    return api_key

def get_api_key():
    global OPENAI_API_KEY
    OPENAI_API_KEY = OPENAI_API_KEY or load_api_key()
    return OPENAI_API_KEY


def build_service_context(openai_api_key):
    llm_predictor = LLMPredictor(
        llm=OpenAI(temperature=0, model_name="text-davinci-002", openai_api_key=openai_api_key))
    # llm_predictor = LLMPredictor(llm=ChatOpenAI(
    #     temperature=0.2, model_name="gpt-3.5-turbo"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    return service_context

class Doc:
    def __init__(
            self,
            doc_id: str,
            filename: str = "",
            openai_api_key: str = "",
    ) -> None:
        self.dir_name = doc_id

        full_dir = osp.join(BASE_DIR, self.dir_name)
        if not osp.exists(full_dir):
            os.makedirs(full_dir)

        self.filename = filename
        self.file_path = osp.join(BASE_DIR, self.dir_name, filename)
        self.data_file = osp.join(BASE_DIR, self.dir_name, "data.txt")
        self.index_file = osp.join(BASE_DIR, self.dir_name, "index.json")
        print(full_dir)

        # self.openai_api_key = openai_api_key or get_api_key()
        # print(self.openai_api_key)
        # self.service_context = build_service_context(self.openai_api_key)

    async def save(self, content: bytes):
        with open(self.file_path, "wb") as f:
            f.write(content)

    def build_txt(self, doc_type: str):
        if doc_type == 'application/epub+zip':
            self.extract_epub()
        if doc_type == 'application/pdf':
            self.extract_pdf()
        if doc_type == 'text/plain' or doc_type == 'text/markdown':
            self.data_file = self.file_path
        if doc_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            self.extra_docx()

    def extract_epub(self):
        res = epub2txt(self.file_path)
        with open(self.data_file, "a") as file:
            for i in range(len(res)):
                file.write(res[i])

    def extract_pdf(self):
        reader = PdfReader(self.file_path)
        print("total pages ", len(reader.pages))
        with open(self.data_file, "a") as file:
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                file.write(text)

    def extra_docx(self):
        res = docx2txt.process(self.file_path)
        with open(self.data_file, "a") as file:
            file.write(res)

    def build_index(self, doc_type: str):
        if doc_type == 'web':
            self.build_web()
            return

        documents = SimpleDirectoryReader(
            input_files=[self.data_file]).load_data()
        service_context = self.service_context
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(self.index_file)

    def build_web(self):
        loader = SimpleWebPageReader(html_to_text=True)
        documents = loader.load_data(urls=[self.filename])
        service_context = self.service_context
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(self.index_file)

    def query(self, question: str):
        print("query2", self.index_file, self.file_path)
        index_file = self.index_file

        service_context = self.service_context
        if osp.exists(index_file) == False:
            documents = SimpleDirectoryReader(input_files=[self.file_path]).load_data()
            index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
            index.save_to_disk(index_file)
        else:
            index = GPTSimpleVectorIndex.load_from_disk(index_file, service_context=service_context)

        print("load index successful...")
        QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(
            QUESTION_ANSWER_PROMPT_TMPL_2)

        return index.query(
            query_str=question,
            text_qa_template=QUESTION_ANSWER_PROMPT,
            # response_mode="tree_summarize",
            similarity_top_k=3
        )

    def query2(self, question: str):
        print("query2", self.index_file, self.file_path)
        index_file = self.index_file

        service_context = self.service_context
        if osp.exists(index_file) == False:
            documents = SimpleDirectoryReader(input_files=[self.file_path]).load_data()
            index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
            index.save_to_disk(index_file)
        else:
            index = GPTSimpleVectorIndex.load_from_disk(index_file, service_context=service_context)

        QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(
            QUESTION_ANSWER_PROMPT_TMPL_2)

        return index.query(
            query_str=question,
            text_qa_template=QUESTION_ANSWER_PROMPT,
            response_mode="tree_summarize",
            similarity_top_k=3,
        )


# OPENAI_API_KEY = load_api_key()


if __name__ == '__main__':
    size = 10
    filename = "../requirements.txt"
    # with open(filename, "rb") as f:
    #     data = f.read()
    # doc_id = hashlib.md5(data).hexdigest()
    # doc = Doc(doc_id=doc_id, filename=filename)
    # # doc.save(content=data)
    # Docs(uid=0, doc_id=doc_id, doc_name=filename, doc_type="txt", size=size).insert()
    documents = SimpleDirectoryReader(input_files=[filename]).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents)
    import IPython
    IPython.embed()
