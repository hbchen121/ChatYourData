<template>
  <el-button type="primary" @click="submitLogout()">注销</el-button>
</template>

<script>
export default {
  methods: {
    submitLogout() {
      this.handleLogout();
    },
    handleLogout() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/');
      this.$nextTick(() => {
        window.location.reload()
      })
    },
  },
};
</script>

<style>
</style>

