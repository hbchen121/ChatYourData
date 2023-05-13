<template>
  <el-row>
    <p>Show user account details</p>
  </el-row>
  <el-row>
    <p>Token: {{ user?.access_token || "null" }}</p>
  </el-row>
  <el-row>
    <p>User: {{ user?.username || "null" }}</p>
  </el-row>
  <el-row>
    <Logout />
  </el-row>
</template>

<script>
import Logout from './Logout.vue';
import { mapGetters } from 'vuex'

export default {
  components: {
    Logout,
  },
  computed: {
    user() {
      return this.$store.getters['auth/user']
    }
  },
};
</script>

<style>
</style>
