<template>
  <div id="app">
    <header>
      <h1>Quiz Master</h1>
      <nav v-if="isAuthenticated">
        <router-link to="/">Home</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link v-if="isAdmin" to="/admin">Admin Panel</router-link>
        <button @click="logout">Logout</button>
      </nav>
      <nav v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
  computed: {
    isAuthenticated() {
      // Check authentication state from Vuex
      return this.$store.getters.isAuthenticated;
    },
    isAdmin() {
      // Check if the user has an admin role from Vuex
      return this.$store.getters.userRole === "admin";
    },
  },
  methods: {
    logout() {
      // Dispatch logout action to clear JWT and user data
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
  },
};
</script>

<style scoped>
#app {
  text-align: center;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  color: white;
  padding: 10px 20px;
}

header h1 {
  margin: 0;
}

nav {
  display: flex;
  gap: 15px;
}

nav a,
nav button {
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

nav a:hover,
nav button:hover {
  text-decoration: underline;
}
</style>
