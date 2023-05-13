# encoding:utf-8
import os
import os.path as osp
import time

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from langchain import OpenAI
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def chat_data(input_text, filename):
    time.sleep(3)
    return input_text
    # documents = SimpleDirectoryReader(input_files=[filename]).load_data()
    # os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'
    # index_file = f"cache/{osp.basename(filename)}.json"
    # if osp.exists(index_file):
    #     index = GPTSimpleVectorIndex.load_from_disk(index_file)
    # else:
    #     index = GPTSimpleVectorIndex.from_documents(documents)
    #     index.save_to_disk(index_file, encoding='utf-8')
    # response = index.query(input_text)
    # return response


if __name__ == '__main__':
    import IPython
    filename = 'cache/未命名文本.txt'
    input_text = '文章标题是什么？'
    rsp = chat_data(input_text, filename)
    print(rsp.response)
    IPython.embed()
    pass
