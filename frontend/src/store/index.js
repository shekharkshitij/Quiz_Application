import { createStore } from "vuex";

const store = createStore({
  state: {
    user: null,
    token: null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    login({ commit }, { user, token }) {
      commit("setUser", user);
      commit("setToken", token);
      localStorage.setItem("auth_token", token); // Persist token
    },
    logout({ commit }) {
      commit("setUser", null);
      commit("setToken", null);
      localStorage.removeItem("auth_token"); // Clear token
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === "admin",
  },
});

export default store;
