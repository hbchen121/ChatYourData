<template>
  <Login v-if="!isLoggedIn()" @loginSuccess="handleLoginSuccess" />
  <chatdata v-if="isLoggedIn()" />
</template>

<script>
import Login from "./Login.vue";
import chatdata from "./Chatdata.vue";

export default {
  components: {
    Login,
    chatdata
  },
  methods: {
    isLoggedIn(){
      return this.$store.state.auth.status.loggedIn;
    },
    handleLoginSuccess() {
      this.$router.push('/chat');
    }
  }
};
</script>