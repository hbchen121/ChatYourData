import {postApi} from './api';

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
    ? {status: {loggedIn: true}, user}
    : {status: {loggedIn: false}, user: null};

export const auth = {
    namespaced: true,
    state: initialState,
    actions: {
        login({commit}, user) {
            console.log("1logsuccess")
            console.log("1auth.js", user)
            return login(user).then(
                user => {
                    console.log("logsuccess")
                    user = localStorage.getItem('user')
                    console.log("auth.js", user)
                    commit('loginSuccess', user);
                    console.log("auth.js-state1", this.state)
                    console.log("auth.js-state", user)
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                }
            );
        },
        logout({commit}) {
            logout();
            commit('logout');
        },
        register({commit}, user) {
            return register(user).then(
                response => {
                    commit('registerSuccess');
                    return Promise.resolve(response.data);
                },
                error => {
                    commit('registerFailure');
                    return Promise.reject(error);
                }
            );
        }
    },
    mutations: {
        loginSuccess(state, user) {
          console.log("in logsuccess", state, user)
            state.status.loggedIn = true;
            state.user = user;
            this.$store.getters['auth/user']
        },
        loginFailure(state) {
            state.status.loggedIn = false;
            state.user = null;
            this.$store.getters['auth/user']
        },
        logout(state) {
            state.status.loggedIn = false;
            state.user = null;
            this.$store.getters['auth/user']
        },
        registerSuccess(state) {
            state.status.loggedIn = false;
        },
        registerFailure(state) {
            state.status.loggedIn = false;
        }
    },
    getters: {
        user: state => state.user
    },
};

async function login(user) {
    // await postApi("token", user)
    return postApi("token", user)
        .then((response) => {
            if (response.status == 200) return response.json()
            else throw 'Login Failure 401'
        })
        .then((data) => {
            if (data.access_token) {
                console.log("data", data)
                localStorage.setItem('user', JSON.stringify(data));
                console.log("data-user", user)
                return data; // 添加返回值，返回 data 对象
            }else {
                throw 'Access token not found';
            }
        });
}

async function logout() {
    localStorage.removeItem('user');
}
