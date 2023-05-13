import {createApp} from 'vue'
import ElementPlus from 'element-plus'
import 'normalize.css/normalize.css'
import 'element-plus/dist/index.css'
import './styles/style.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import App from './App.vue'

import {auth} from "./auth";
import {createStore} from 'vuex';
import {createRouter, createWebHistory} from 'vue-router';
import Home from './views/Home.vue';
import chatdata from "./views/Chatdata.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', name: 'Home', component: Home},
        {
            path: '/chat', name: "chatdata", component: chatdata
        }
    ],
})

const store = createStore({
    modules: {
        auth,
    },
});

const app = createApp(App)
app.use(router)
app.use(store)
app.use(ElementPlus)
app.mount('#app')
