import { docState, formatByteSize, docType, nameWithoutExt, docUrl, showLastMessage }  from './utils'

export const state = {
  docList: [],
  active: null,
  messages: [],
  msgLoading: false,
  input: '',
  askErr: ''
}

export const mutations = {
  setDocList(state, list) {
    state.docList = list
  },
  setActive(state, doc) {
    state.active = doc
  },
  setMessages(state, msgs) {
    state.messages = msgs
  },
  setMsgLoading(state, loading) {
    state.msgLoading = loading
  },
  setInput(state, input) {
    state.input = input
  },
  setAskErr(state, err) {
    state.askErr = err
  }
}

export default {
  state,
  mutations
}