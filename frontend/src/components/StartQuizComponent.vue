<template>
    <div class="start-quiz">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
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
  
      <!-- Quiz Content -->
      <div class="container mt-5">
        <div v-if="questions.length > 0">
          <h1 class="text-center">{{ quiz?.name || "Quiz Name" }}</h1>
          <p class="text-center text-muted">{{ quiz?.description || "Quiz Description" }}</p>
  
          <!-- Questions Section -->
          <div class="questions-container">
            <form @submit.prevent="submitQuiz">
              <div
                v-for="(question, index) in questions"
                :key="question.id"
                class="question-card"
              >
                <h4>Question {{ index + 1 }}: {{ question.text }}</h4>
                <div class="options">
                  <div
                    v-for="(option, idx) in question.options"
                    :key="idx"
                    class="form-check"
                  >
                    <input
                      type="radio"
                      :id="`question-${question.id}-option-${idx}`"
                      :name="`question-${question.id}`"
                      :value="idx + 1"
                      v-model="userAnswers[question.id]"
                      class="form-check-input"
                    />
                    <label
                      :for="`question-${question.id}-option-${idx}`"
                      class="form-check-label"
                    >
                      {{ option }}
                    </label>
                  </div>
                </div>
              </div>
  
              <div class="text-center mt-4">
                <button type="submit" class="btn btn-success">
                  Submit Quiz
                </button>
              </div>
            </form>
          </div>
        </div>
        <div v-else>
          <h3 class="text-center text-danger">Loading quiz details...</h3>
        </div>
      </div>
    </div>
  </template>
  
  ---
  
  ### **Script Section**
  
  ```javascript
  <script>
  import axios from "axios";
import { mapActions, mapState } from "vuex";
import api from "../api/api";
  
  export default {
    name: "StartQuizComponent",
    data() {
      return {
        quiz: {}, // Quiz details
        questions: [], // List of questions
        userAnswers: {}, // User's answers
      };
    },
    computed: {
      ...mapState(["user"]),
      quizId() {
        return this.$route.params.quizId; // Get the quiz ID from the route
      },
    },
    methods: {
      ...mapActions(["logout"]),
      async handleLogout() {
        try {
          await this.logout();
          this.$router.push("/login");
        } catch (error) {
          console.error("Logout failed:", error.message);
          alert("Logout failed. Please try again.");
        }
      },
      async fetchQuizDetails() {
        try {
          const response = await api.getQuestions(this.quizId); // API call for quiz questions
          this.questions = response; // Assuming response is an array of questions
          console.log("Questions fetched:", this.questions);
        } catch (error) {
          console.error("Error fetching questions:", error.message || error);
          alert("Failed to fetch questions. Please try again.");
        }
      },
      async submitQuiz() {
        try {
          const response = await axios.post(
            `http://localhost:5000/api/v1/quizzes/${this.quizId}/submit`,
            { answers: this.userAnswers }, // Send user's answers
            {
              headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
            }
          ); 
          alert(`You scored ${response.data.score} out of ${response.data.total_questions}`);
          // Optionally, navigate to a dashboard or result page
          this.$router.push("/user-dashboard");
        } catch (error) {
          console.error("Error submitting quiz:", error.message);
          alert("Failed to submit quiz. Please try again.");
        }
      },
    },
    mounted() {
      this.fetchQuizDetails();
    },
  };
  </script>
<style scoped>
.start-quiz {
  background: linear-gradient(to bottom, #6a11cb, #2575fc);
  min-height: 100vh;
  padding: 20px 0;
  color: #ffffff;
}

.questions-container {
  max-width: 800px;
  margin: 0 auto;
  background: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  color: #333;
}

.question-card {
  margin-bottom: 20px;
}

.options {
  margin-top: 10px;
}

.btn-success {
  padding: 10px 20px;
  font-size: 16px;
}

.text-muted {
  color: #6c757d !important;
}
</style>
  