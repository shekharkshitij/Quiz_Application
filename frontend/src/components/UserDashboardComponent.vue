<template>
    <div class="user-dashboard">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark w-100">
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
                <button @click="handleLogout" class="btn btn-danger btn-sm nav-link">
                  Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- User Dashboard Content -->
      <div class="container mt-5">
        <h1 class="text-center mb-4 text-light">Welcome, {{ user?.email }}</h1>
        <p class="text-center text-light">You are logged in as a User.</p>
        <div class="row g-4">
          <!-- Take Quiz -->
          <div class="col-md-4">
            <div class="card shadow-sm">
              <div class="card-body text-center">
                <h5 class="card-title">Take a Quiz</h5>
                <p class="card-text">Participate in quizzes and improve your knowledge.</p>
                <router-link to="/take-quiz" class="btn btn-primary">Start Quiz</router-link>
              </div>
            </div>
          </div>
          <!-- View Scores -->
          <div class="col-md-4">
            <div class="card shadow-sm">
              <div class="card-body text-center">
                <h5 class="card-title">View Scores</h5>
                <p class="card-text">Check your quiz scores and track your progress.</p>
                <router-link to="/view-scores" class="btn btn-primary">View Scores</router-link>
              </div>
            </div>
          </div>
          <!-- Profile -->
          <div class="col-md-4">
            <div class="card shadow-sm">
              <div class="card-body text-center">
                <h5 class="card-title">Profile</h5>
                <p class="card-text">Manage your account details and settings.</p>
                <router-link to="/profile" class="btn btn-primary">View Profile</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions, mapState } from "vuex";
  
  export default {
    name: "UserDashboardComponent",
    computed: {
      ...mapState(["user"]), // Map user state from Vuex
    },
    methods: {
      ...mapActions(["logout"]), // Map logout action from Vuex
      async handleLogout() {
        try {
          await this.logout(); // Call Vuex logout action
          this.$router.push("/login"); // Redirect to login page
        } catch (error) {
          console.error("Logout failed:", error.message);
          alert("Logout failed. Please try again.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .user-dashboard {
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
  