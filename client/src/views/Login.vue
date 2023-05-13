<template>
  <div class="container">
    <div class="login-wrapper">
      <div class="header">ChatYourData</div>
      <div class="msg"><a href="https://r3mu87a8e6.feishu.cn/wiki/wikcnoX22G5Q74NoRvkErsvaNre">使用教程</a> </div>
      <div class="form-wrapper">
        <div class="input-item">
          <el-input v-model.number="loginForm.username" type="text" name="Username" placeholder="用户名"></el-input>
        </div>
        <div class="input-item">
          <el-input v-model.number="loginForm.password" type="text" name="Password" placeholder="密码"></el-input>
        </div>
        <div class="btn" @click="submitLogin()">
          <el-button type="text" @click="submitLogin()" class="black-color-btn">登录/注册</el-button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        password: "",
        username: "",
      },
    };
  },
  methods: {
    submitLogin() {
      this.handleLogin(this.loginForm);
    },
    handleLogin(user) {
      this.$store.dispatch("auth/login", user).then(
          () => {
            console.log("Login.vue", user)
            this.$router.push("/");
          },
          (error) => {
            this.message =
                (error.response &&
                    error.response.data &&
                    error.response.data.message) ||
                error.message ||
                error.toString();
          }
      );
    },
  },
}
</script>

<style scoped>
@import "../styles/login.css";
</style>
