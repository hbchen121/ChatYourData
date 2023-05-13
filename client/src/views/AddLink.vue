<template>
  <el-button type="primary" @click="open">链接</el-button>
</template>

<script lang="ts" setup>
import {ElMessage, ElMessageBox} from 'element-plus'
import {addAddLink} from '../api'
// import {Plus} from '@element-plus/icons-vue'
// import {useStore} from "vuex";
// import {computed} from "vue";

const emit = defineEmits(['uploadSuccess'])
// const store = useStore()
// const user = computed(() => store.getters['auth/user'])
const user = JSON.parse(localStorage.getItem('user'));

const open = () => {
  ElMessageBox.prompt('', '输入链接', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    inputPattern: /^(ftp|http|https):\/\/[^ "]+$/,
    inputErrorMessage: '不是一个有效链接',
  })
      .then(({value}) => {
        addAddLink(value, user)
            .then(res => {
              emit('uploadSuccess')
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
  