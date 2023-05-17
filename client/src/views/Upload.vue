<script>
import {ElMessage} from "element-plus";
import { mapGetters } from 'vuex'


export default {
  emits: ['uploadSuccess'],
  data() {
    return {
      supportFileType: ['application/pdf', 'application/epub+zip', 'text/markdown', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    }
  },

  methods: {
    beforeUpload(rawFile) {
      if (!this.supportFileType.includes(rawFile.type)) {
        console.log(rawFile.type);
        ElMessage.error('仅支持 .pdf, .epub, .txt 类型文件');
        return false;
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('文件大小不能超过 2MB!');
        return false;
      }
      return true;
    },
    uploadSuccess() {
      this.$emit('uploadSuccess');
    }
  },
  computed: {
    user() {
      return JSON.parse(localStorage.getItem('user'));
    }
  }

}
</script>

<template>
  <el-upload ref="uploadRef" class="upload-demo" action="/api/upload" :auto-upload="true" :show-file-list="false"
             :on-success="uploadSuccess" :before-upload="beforeUpload" :headers="{'user': JSON.stringify(user)}">
    <template #trigger>
      <el-button type="primary" style="width: 100%;">文件 </el-button>
    </template>
  </el-upload>
</template>
