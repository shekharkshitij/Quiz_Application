<template>
  <div class="manage-quizzes">
    <h1 class="title">Manage Quizzes</h1>

    <!-- Form to Add a Quiz -->
    <form @submit.prevent="addQuiz" class="quiz-form">
      <input
        v-model="newQuiz.name"
        placeholder="Quiz Name"
        class="form-control input-field"
        required
      />
      <textarea
        v-model="newQuiz.description"
        placeholder="Description"
        class="form-control input-field"
      ></textarea>
      <button type="submit" class="btn btn-add">Add Quiz</button>
    </form>

    <!-- List of Quizzes -->
    <ul class="quiz-list">
      <li v-for="quiz in quizzes" :key="quiz.id" class="quiz-item">
        <div class="quiz-details">
          <h5 class="quiz-name">{{ quiz.name }}</h5>
          <p class="quiz-description">{{ quiz.description }}</p>
        </div>
        <div class="quiz-actions">
          <button
            @click="editQuiz(quiz)"
            class="btn btn-edit"
          >
            Edit
          </button>
          <button
            @click="deleteQuiz(quiz.id)"
            class="btn btn-delete"
          >
            Delete
          </button>
          <button
            @click="navigateToQuestions(quiz.id)"
            class="btn btn-manage"
          >
            Manage Questions
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../api/api";

export default {
  name: "ManageQuizzes",
  props: ["chapterId"],
  data() {
    return {
      quizzes: [],
      newQuiz: { name: "", description: "" },
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await api.getQuizzes(this.chapterId);
        this.quizzes = response;
      } catch (error) {
        console.error("Error fetching quizzes:", error.message || error);
        alert("Failed to fetch quizzes.");
      }
    },
    async addQuiz() {
      try {
        const data = {
          ...this.newQuiz,
          chapter_id: this.chapterId,
        };
        await api.addQuiz(data);
        this.newQuiz = { name: "", description: "" };
        this.fetchQuizzes();
      } catch (error) {
        console.error("Error adding quiz:", error.message || error);
        alert("Failed to add quiz. Please try again.");
      }
    },
    async editQuiz(quiz) {
      try {
        const newName = prompt("Enter new quiz name:", quiz.name);
        if (!newName) return;
        const updatedQuiz = { ...quiz, name: newName };
        await api.updateQuiz(updatedQuiz.id, updatedQuiz);
        this.fetchQuizzes();
      } catch (error) {
        console.error("Error editing quiz:", error.message || error);
        alert("Failed to edit quiz. Please try again.");
      }
    },
    async deleteQuiz(quizId) {
      try {
        if (confirm("Are you sure you want to delete this quiz?")) {
          await api.deleteQuiz(quizId);
          this.fetchQuizzes();
        }
      } catch (error) {
        console.error("Error deleting quiz:", error.message || error);
        alert("Failed to delete quiz. Please try again.");
      }
    },
    navigateToQuestions(quizId) {
      this.$router.push({ name: "ManageQuestions", params: { quizId } });
    },
  },
  mounted() {
    this.fetchQuizzes();
  },
};
</script>

<style scoped>
.manage-quizzes {
  max-width: 900px;
  margin: 20px auto;
  padding: 30px;
  background: linear-gradient(to bottom right, #6a11cb, #2575fc); /* Gradient background */
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  color: #ffffff;
}

.title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.quiz-form {
  margin-bottom: 25px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.quiz-form input,
.quiz-form textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.quiz-form button {
  background-color: #0056b3; /* Blue shade */
  color: #ffffff;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.quiz-form button:hover {
  background-color: #003f7f;
}

.quiz-list {
  list-style: none;
  padding: 0;
}

.quiz-item {
  background: rgba(255, 255, 255, 0.9); /* Light background */
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.quiz-details h5 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.quiz-details p {
  color: #34495e;
}

.quiz-actions {
  display: flex;
  gap: 15px;
}

.btn {
  padding: 10px 15px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  color: #fff;
}

.btn-edit {
  background-color: #f39c12;
}

.btn-edit:hover {
  background-color: #d35400;
}

.btn-delete {
  background-color: #e74c3c;
}

.btn-delete:hover {
  background-color: #c0392b;
}

.btn-manage {
  background-color: #27ae60;
}

.btn-manage:hover {
  background-color: #1e8449;
}
</style>
