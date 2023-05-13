<script setup xmlns="http://www.w3.org/1999/html">
import {ElMessage} from 'element-plus'
// import { ElMessageBox } from 'element-plus'
import Upload from '../views/Upload.vue'
import Loading from '@/assets/loading.svg?component'
import {DeleteFilled} from '@element-plus/icons-vue'
import {docState, formatByteSize, docType, nameWithoutExt, docUrl, showLastMessage} from '../utils'
import {onBeforeMount, ref, watch, onMounted, nextTick, computed} from 'vue';
import {fetchDocList, fetchQuery, fetchMsg, fetchDelDoc, fetchApikey} from '../api'
import Logout from './Logout.vue';
import AddLink from '../views/AddLink.vue';
import Apikey from '../views/Apikey.vue';

var docList = ref([])
var active = ref(null)

const user = JSON.parse(localStorage.getItem('user'));


watch(active, () => {
  loadMsg()
})

function loadDos() {
  fetchDocList(user).then(res => {
    docList.value = res?.data || []

    if (active.value == null && docList.value.length > 0) {
      const doc = docList.value[0]
      active.value = doc
    }
  })
}

var messages = ref([])
var askErr = ref()

function loadMsg() {
  fetchMsg(active.value.doc_id).then(res => {
    if (res.code) {
      askErr.value = res.message
      ElMessage.error(res.message)
    } else {
      messages.value = res.data || []
    }
    showLastMessage(1000)
  })
}


var api_key = ref(null)

function loadApikey() {
  fetchApikey(user).then(res => {
    api_key.value = res?.data || null
    console.log("api_key", api_key)
  })
}


onBeforeMount(() => {
  loadDos()
  loadApikey()
})

const uploadSuccess = () => {
  loadDos()
  loadFileState()
  loadApikey()
}

const changeDoc = (doc) => {
  active.value = doc
}

var msgLoading = ref(false)
var input = ref('')

function query() {
  if (!input.value) {
    return
  }
  messages.value.push({
    content: input.value,
    role: 'user'
  })
  showLastMessage()
  msgLoading.value = true
  fetchQuery(active.value.doc_id, input.value).then(res => {
    messages.value.push({
      content: res?.data?.response || '',
      role: 'chatdata'
    })
    showLastMessage()
    msgLoading.value = false
  })
  input.value = ""
}

const refInput = ref(null)
const getFocus = () => {
  nextTick(() => {
    refInput.value.focus();
  })
}
onMounted(() => {
  getFocus()
})

function delDoc(doc_id) {
  if (active.value.doc_id == doc_id) {
    active.value = null
  }
  if (active.value == null && docList.value.length > 0) {
    const doc = docList.value[0]
    active.value = doc
  }

  fetchDelDoc(doc_id).then(() => {
    loadDos()
  })
}

const loadFileState = () => {
  if (docList.value.filter(e => e.state != 2).length > 0) {
    setTimeout(() => {
      loadDos()
      loadFileState()
    }, 2000)
  }
}

const onerror = (e) => {
  console.log(e)
}
</script>

<template>
  <div class="container">
    <div class="sidebar">
      <div style="overflow-y: scroll;">
        <div class="user-info">
<!--          <el-avatar :size="30" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"/>-->
          <span class="user-name">{{ "用户名: " + user.username.slice(0, 8) + "*" }}</span>
          <Logout @uploadSuccess="uploadSuccess"/>
        </div>
        <div class="api-info">
          <span class="user-name">{{ "API Key: " + api_key?.slice(0, 8) + "***" || "no api key" }}</span>
          <Apikey @uploadSuccess="uploadSuccess"/>
        </div>

        <div class="add-doc">
          <span class="user-name"><a href="https://r3mu87a8e6.feishu.cn/wiki/wikcnoX22G5Q74NoRvkErsvaNre">使用教程</a></span>
          <Upload @upload-success="uploadSuccess"/>
          <AddLink @upload-success="uploadSuccess"/>
        </div>
        <div class="doc-list" v-for="(item) in docList" :key="item.doc_id">
          <div :class="{ 'doc-item': true, ellipsis: true, 'doc-active': item.doc_id === active.doc_id }"
               :title="item.doc_name" @click="changeDoc(item)">
            <div class="doc-item-title">
              <span style="display: inline-block; width: 70%; overflow: hidden; text-overflow: ellipsis;">{{
                  nameWithoutExt(item.doc_name)
                }}</span>
              <el-icon @click.stop="delDoc(item.doc_id)" class="remove-icon">
                <DeleteFilled/>
              </el-icon>
            </div>
            <div class="doc-item-info">
              <span class="doc-item-info-cell">type: {{ docType(item) }}</span>
              <span class="doc-item-info-cell">size: {{ formatByteSize(item.size || 0) }}</span>
              <span class="doc-item-info-cell">index: {{ docState(item.state) }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
    <div class="doc">
      <div v-if="docList.length == 0" class="empty-info">
        <div>当前没有文档, 请先上传</div>
        <div>
          <Upload @upload-success="uploadSuccess"/>
        </div>
      </div>
      <iframe v-if="docList.length > 0 && active" :src="docUrl(active)" style="width:100%;height: 100%;"
              :key="active.doc_id" @onerror="onerror"></iframe>
    </div>
    <div class="chat">
      <div id="messages" class="messages">
        <div :class="{ 'message-item': true, 'message-user': item.role == 'user' }" v-for="(item, index) in messages"
             :key="index">
          {{ item.content }}
        </div>
      </div>
      <div class="loading">
        <el-icon :size="30" v-if="msgLoading">
          <Loading/>
        </el-icon>
      </div>
      <input ref="refInput" class="input" :placeholder="active?.state != 2 ? '索引构建中...' : '开始与你的文档对话吧'"
             :disabled="active?.state != 2 || msgLoading" v-model="input" @keyup.up.enter="query"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../styles/chatdata.css';
</style>

