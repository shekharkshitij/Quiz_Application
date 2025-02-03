<template>
  <div class="admin-dashboard">
    <!-- <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">Quiz Management System</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <button @click="handleLogout" class="btn btn-danger btn-sm nav-link">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav> -->

    <!-- Admin Dashboard Content -->
    <div class="container mt-5">
      <h1 class="text-center mb-4 text-light">Admin Dashboard</h1>
      <div class="row g-4">
        <!-- Manage Subjects -->
        <div class="col-md-4">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">Manage Subjects</h5>
              <p class="card-text">Add, edit, or delete subjects for quizzes.</p>
              <router-link to="/manage-subjects" class="btn btn-primary">Go to Subjects</router-link>
            </div>
          </div>
        </div>
        <!-- Manage Quizzes -->
        <div class="col-md-4">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">Manage Quizzes</h5>
              <p class="card-text">Create, edit, or delete quizzes for students.</p>
              <router-link to="/manage-quizzes" class="btn btn-primary">Go to Quizzes</router-link>
            </div>
          </div>
        </div>
        <!-- View Scores -->
        <div class="col-md-4">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">View Scores</h5>
              <p class="card-text">View and analyze quiz scores of students.</p>
              <router-link to="/view-scores" class="btn btn-primary">Go to Scores</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "AdminDashboardComponent",
  methods: {
    ...mapActions(["logout"]), // Map Vuex logout action
    async handleLogout() {
      try {
        await this.logout(); // Call Vuex logout action
        localStorage.removeItem("auth_token"); // Ensure the token is removed
        this.$router.push("/login"); // Redirect to login after logout
      } catch (error) {
        console.error("Logout failed:", error.message);
        alert("Logout failed. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
  background: linear-gradient(to right, #4e54c8, #8f94fb); /* Gradient blue background */
  min-height: 100vh;
  padding-bottom: 20px;
}

.card {
  border-radius: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-weight: bold;
}

.text-light {
  color: #ffffff;
}
</style>
