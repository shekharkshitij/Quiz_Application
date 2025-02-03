<template>
  <div class="take-quiz">
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

    <!-- Welcome Section -->
    <div class="container mt-5 text-center">
      <h1 class="welcome-text">Welcome, {{ user?.email }}</h1>
      <p class="text-light mb-4">You are logged in as a User. Start by choosing a subject below.</p>
    </div>

    <!-- Steps: Subjects -> Chapters -> Quizzes -->
    <div class="container mt-4">
      <!-- Step 1: Choose Subject -->
      <div v-if="!selectedSubject" class="step-container">
        <h4 class="step-title">Choose a Subject</h4>
        <div class="row g-3">
          <div
            v-for="subject in subjects"
            :key="subject.id"
            class="col-md-4"
          >
            <div class="card shadow-sm subject-card">
              <div class="card-body text-center">
                <h5 class="card-title">{{ subject.name }}</h5>
                <p class="card-text">{{ subject.description }}</p>
                <button
                  @click="selectSubject(subject)"
                  class="btn btn-primary"
                >
                  Select
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Choose Chapter -->
      <div v-else-if="!selectedChapter" class="step-container">
        <h4 class="step-title">Choose a Chapter</h4>
        <div class="row g-3">
          <div
            v-for="chapter in chapters"
            :key="chapter.id"
            class="col-md-4"
          >
            <div class="card shadow-sm chapter-card">
              <div class="card-body text-center">
                <h5 class="card-title">{{ chapter.name }}</h5>
                <p class="card-text">{{ chapter.description }}</p>
                <button
                  @click="selectChapter(chapter)"
                  class="btn btn-success"
                >
                  Select
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 3: Choose Quiz -->
      <div v-else-if="!selectedQuiz" class="step-container">
        <h4 class="step-title">Choose a Quiz</h4>
        <div class="row g-3">
          <div
            v-for="quiz in quizzes"
            :key="quiz.id"
            class="col-md-4"
          >
            <div class="card shadow-sm quiz-card">
              <div class="card-body text-center">
                <h5 class="card-title">{{ quiz.name }}</h5>
                <p class="card-text">{{ quiz.description }}</p>
                <button
                  @click="selectQuiz(quiz)"
                  class="btn btn-warning"
                >
                  Select
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 4: Start Quiz -->
      <div v-else class="step-container text-center">
        <h4 class="step-title">You have selected: {{ selectedQuiz.name }}</h4>
        <p>{{ selectedQuiz.description }}</p>
        <router-link
          :to="{ name: 'StartQuiz', params: { quizId: selectedQuiz.id } }"
          class="btn btn-primary"
        >
          Start Quiz
        </router-link>
        <button @click="resetSelection" class="btn btn-secondary mt-2">
          Reset Selection
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapState } from "vuex";

export default {
  name: "TakeQuizComponent",
  data() {
    return {
      subjects: [], // All subjects
      chapters: [], // Chapters based on the subject
      quizzes: [], // Quizzes based on the chapter
      selectedSubject: null, // Selected subject
      selectedChapter: null, // Selected chapter
      selectedQuiz: null, // Selected quiz
    };
  },
  computed: {
    ...mapState(["user"]),
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
    async fetchSubjects() {
      try {
        const response = await axios.get("http://localhost:5000/api/v1/subjects", {
          headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
        });
        this.subjects = response.data;
      } catch (error) {
        console.error("Error fetching subjects:", error.message);
        alert("Failed to fetch subjects. Please try again.");
      }
    },
    async fetchChapters(subjectId) {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/v1/chapters/subject/${subjectId}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` } }
        );
        this.chapters = response.data;
      } catch (error) {
        console.error("Error fetching chapters:", error.message);
        alert("Failed to fetch chapters. Please try again.");
      }
    },
    async fetchQuizzes(chapterId) {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/v1/quizzes?chapter_id=${chapterId}`,
          { headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` } }
        );
        this.quizzes = response.data;
      } catch (error) {
        console.error("Error fetching quizzes:", error.message);
        alert("Failed to fetch quizzes. Please try again.");
      }
    },
    selectSubject(subject) {
      this.selectedSubject = subject;
      this.fetchChapters(subject.id);
    },
    selectChapter(chapter) {
      this.selectedChapter = chapter;
      this.fetchQuizzes(chapter.id);
    },
    selectQuiz(quiz) {
      this.selectedQuiz = quiz;
    },
    resetSelection() {
      this.selectedSubject = null;
      this.selectedChapter = null;
      this.selectedQuiz = null;
    },
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>

<style scoped>
.take-quiz {
  background: linear-gradient(to bottom, #6a11cb, #2575fc); /* Blue gradient */
  min-height: 100vh;
  padding: 30px 0;
  color: #ffffff;
}

.step-title {
  color: #ffffff;
  margin-bottom: 20px;
  font-weight: bold;
  text-align: center;
}

.card {
  transition: transform 0.3s, box-shadow 0.3s;
  border-radius: 15px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.3);
}

.subject-card {
  background-color: #f8f9fa;
}

.chapter-card {
  background-color: #e3f2fd;
}

.quiz-card {
  background-color: #fff3cd;
}

.btn-primary {
  background-color: #4caf50;
}

.btn-primary:hover {
  background-color: #388e3c;
}

.welcome-text {
  font-size: 2rem;
  font-weight: bold;
}
</style>
