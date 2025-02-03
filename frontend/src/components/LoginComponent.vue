<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" class="btn-login">Login</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <p class="register-link">
          New to the site? <router-link to="/register">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  name: "LoginComponent",
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    ...mapActions(["login"]), // Vuex login action
    async handleLogin() {
      try {
        const response = await axios.post("http://localhost:5000/api/v1/login", {
          email: this.email,
          password: this.password,
        });

        const { auth_token } = response.data;

        if (!auth_token) {
          throw new Error("No auth_token received from the server.");
        }

        // Decode JWT to extract user role
        const payload = JSON.parse(atob(auth_token.split(".")[1]));
        const user = {
          email: payload.email,
          role: payload.role || "user", // Default role is "user" if undefined
        };

        // Save token and user details in Vuex
        this.login({ user, token: auth_token });

        // Redirect based on role
        if (user.role === "admin") {
          this.$router.push("/admin-dashboard");
        } else {
          this.$router.push("/user-dashboard");
        }
      } catch (error) {
        console.error("Login failed:", error.response?.data?.message || error.message);
        this.errorMessage =
          error.response?.data?.message || "Login failed. Please try again.";
      }
    },
  },
};
</script>

<style scoped>
/* Styling remains unchanged */
.login-page {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  color: white;
  padding-top: 60px;
}

.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  height: calc(100% - 60px);
  width: 100%;
}

.login-card {
  background-color: #fff;
  color: #333;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

h2 {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #2575fc;
  box-shadow: 0 0 5px rgba(37, 117, 252, 0.5);
}

.btn-login {
  background-color: #2575fc;
  color: #fff;
  border: none;
  padding: 0.7rem 1rem;
  font-size: 1rem;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

.btn-login:hover {
  background-color: #0e62d2;
}

.error-message {
  color: #e63946;
  margin-top: 1rem;
}

.register-link {
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.register-link a {
  color: #2575fc;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
