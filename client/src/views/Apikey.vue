<template>
  <el-button type="primary" @click="add">设置</el-button>
</template>

<script lang="ts" setup>
import {ElMessage, ElMessageBox} from 'element-plus'
import {addApikey} from '../api'

const emit = defineEmits(['uploadSuccess'])
const user = JSON.parse(localStorage.getItem('user'));


const add = () => {
  ElMessageBox.prompt('设置你的 OpenAI API Key', 'OPENAI KEY', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    inputType: 'text'
  })
      .then(({value}) => {
        addApikey(value, user)
            .then(res => {
              emit('addApikeySuccess')
            })
            .catch(err => {
              ElMessage.error(err)
            })
      })
      .catch(err => {
        ElMessage.error(err)
      })
}
</script>
