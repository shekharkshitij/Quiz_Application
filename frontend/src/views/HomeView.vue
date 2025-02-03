<template>
    <div>
      <!-- Navbar
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
        <div class="container">
          <a class="navbar-brand fw-bold" href="#">Quiz Management System</a>
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
                <router-link to="/" class="nav-link active">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">Register</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav> -->
  
      <!-- Hero Section -->
      <header class="hero-section text-white text-center d-flex align-items-center">
        <div class="container">
          <h1 class="display-3 fw-bold">Welcome to Quiz Master!</h1>
          <p class="lead mt-3">
            The ultimate platform to test your knowledge and skills.
          </p>
          <div class="mt-4">
            <router-link to="/login" class="btn btn-primary btn-lg shadow-lg me-3"
              >Login</router-link
            >
            <router-link
              to="/register"
              class="btn btn-outline-light btn-lg shadow-lg"
              >Register</router-link
            >
          </div>
        </div>
      </header>
  
      <!-- Features Section -->
      <section class="features py-5">
        <div class="container">
          <h2 class="text-center mb-5 fw-bold">Explore Our Features</h2>
          <div class="row">
            <div class="col-md-4">
              <div class="card shadow-lg feature-card h-100 text-center">
                <div class="card-body">
                  <i class="bi bi-pencil-square text-primary fs-1 mb-3"></i>
                  <h5 class="card-title">Take Quizzes</h5>
                  <p class="card-text">
                    Participate in interactive quizzes and compete with friends.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card shadow-lg feature-card h-100 text-center">
                <div class="card-body">
                  <i class="bi bi-bar-chart-line text-success fs-1 mb-3"></i>
                  <h5 class="card-title">Track Scores</h5>
                  <p class="card-text">
                    Analyze your progress and improve your skills with insights.
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card shadow-lg feature-card h-100 text-center">
                <div class="card-body">
                  <i class="bi bi-lightbulb text-warning fs-1 mb-3"></i>
                  <h5 class="card-title">Learn More</h5>
                  <p class="card-text">
                    Enhance your knowledge with our curated quizzes and resources.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="bg-dark text-white text-center py-4">
        <p class="mb-0">
          &copy; 2024 Quiz Master. All Rights Reserved. Designed with ❤️ using
          Vue.js & Bootstrap.
        </p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: "HomeView",
  };
  </script>
  
  <style scoped>
  .hero-section {
    height: 80vh;
    background: linear-gradient(45deg, #007bff, #6610f2);
    color: white;
    padding-top: 100px;
  }
  
  .features h2 {
    font-family: "Poppins", sans-serif;
    color: #343a40;
  }
  
  .feature-card {
    border: none;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  }
  
  .feature-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  footer {
    background: #222;
  }
  </style>
  