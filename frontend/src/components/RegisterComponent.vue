<template>
  <div>
    <!-- Register Page -->
    <div class="register-page">
      <div class="register-container">
        <h2 class="text-center">Register</h2>
        <form @submit.prevent="register" class="form-container">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              placeholder="Enter your username"
              required
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="form-control"
              placeholder="Enter your password"
              required
            />
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              class="form-control"
              placeholder="Confirm your password"
              required
            />
          </div>
          <div class="form-group">
            <label for="dob">Date of Birth</label>
            <input
              id="dob"
              v-model="form.dob"
              type="date"
              class="form-control"
              required
            />
          </div>
          <div class="form-group">
            <label for="qualification">Qualification</label>
            <input
              id="qualification"
              v-model="form.qualification"
              type="text"
              class="form-control"
              placeholder="Enter your qualification"
              required
            />
          </div>
          <div class="form-group">
            <label for="fullName">Full Name</label>
            <input
              id="fullName"
              v-model="form.fullName"
              type="text"
              class="form-control"
              placeholder="Enter your full name"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100 mt-4">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api/api";

export default {
  name: "RegisterComponent",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        dob: "",
        qualification: "",
        fullName: "",
      },
    };
  },
  methods: {
    async register() {
      if (this.form.password !== this.form.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      try {
        await api.register(this.form);
        alert("Registration successful!");
        this.$router.push("/login");
      } catch (error) {
        alert(error.response?.data?.message || "Error during registration");
      }
    },
  },
};
</script>

<style scoped>
/* Register Page Styling */
.register-page {
  background: linear-gradient(to bottom right, #4f62c9, #9fa0fa);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-container {
  background: white;
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.text-center {
  text-align: center;
  margin-bottom: 20px;
  color: #4f62c9;
  font-weight: bold;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px; /* Spacing between form groups */
}

.form-group {
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #4f62c9;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #4f62c9;
  box-shadow: 0px 0px 5px rgba(79, 98, 201, 0.5);
}

.btn {
  background: #4f62c9;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.btn:hover {
  background: #3d4fa1;
}

.w-100 {
  width: 100%;
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>
