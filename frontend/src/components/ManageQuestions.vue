<template>
  <div class="manage-questions">
    <h2 class="title">Manage Questions</h2>

    <!-- Add Question Form -->
    <form @submit.prevent="addQuestion" class="question-form">
      <textarea
        v-model="text"
        placeholder="Enter Question Text"
        required
        class="form-control question-text"
      ></textarea>
      <div class="options-container">
        <input
          v-model="option1"
          placeholder="Option 1"
          required
          class="form-control option-input"
        />
        <input
          v-model="option2"
          placeholder="Option 2"
          required
          class="form-control option-input"
        />
        <input
          v-model="option3"
          placeholder="Option 3"
          required
          class="form-control option-input"
        />
        <input
          v-model="option4"
          placeholder="Option 4"
          required
          class="form-control option-input"
        />
      </div>
      <input
        type="number"
        v-model.number="correctOption"
        placeholder="Correct Option (1-4)"
        min="1"
        max="4"
        required
        class="form-control correct-option-input"
      />
      <button type="submit" class="btn btn-add-question">Add Question</button>
    </form>

    <!-- Question List -->
    <ul class="question-list">
      <li
        v-for="question in questions"
        :key="question.id"
        class="question-item"
      >
        <div class="question-text">
          <strong>{{ question.text }}</strong>
          <ul class="options">
            <li v-for="(option, index) in question.options" :key="index">
              <span class="option-label">Option {{ index + 1 }}:</span> {{ option }}
            </li>
          </ul>
        </div>
        <div class="question-actions">
          <button
            class="btn btn-delete"
            @click="deleteQuestion(question.id)"
          >
            Delete
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from "../api/api";

export default {
  name: "ManageQuestions",
  props: ["quizId"],
  data() {
    return {
      questions: [],
      text: "",
      option1: "",
      option2: "",
      option3: "",
      option4: "",
      correctOption: "",
    };
  },
  methods: {
    async fetchQuestions() {
      try {
        const response = await api.getQuestions(this.quizId);
        this.questions = response; // Assuming response is an array of questions
      } catch (error) {
        console.error("Error fetching questions:", error.message || error);
        alert("Failed to fetch questions. Please try again.");
      }
    },
    async addQuestion() {
      if (![1, 2, 3, 4].includes(this.correctOption)) {
        alert("Correct Option must be between 1 and 4.");
        return;
      }

      try {
        await api.addQuestion({
          quiz_id: this.quizId,
          text: this.text,
          option1: this.option1,
          option2: this.option2,
          option3: this.option3,
          option4: this.option4,
          correct_option: this.correctOption,
        });

        this.text = "";
        this.option1 = "";
        this.option2 = "";
        this.option3 = "";
        this.option4 = "";
        this.correctOption = "";

        this.fetchQuestions();
      } catch (error) {
        console.error("Error adding question:", error.message || error);
        alert("Failed to add question. Please try again.");
      }
    },
    async deleteQuestion(id) {
      if (confirm("Are you sure you want to delete this question?")) {
        try {
          await api.deleteQuestion(id);
          this.fetchQuestions();
        } catch (error) {
          console.error("Error deleting question:", error.message || error);
          alert("Failed to delete question. Please try again.");
        }
      }
    },
  },
  created() {
    this.fetchQuestions();
  },
};
</script>

<style scoped>
.manage-questions {
  background: linear-gradient(135deg, #ff9a9e, #fad0c4);
  padding: 20px;
  border-radius: 15px;
  max-width: 900px;
  margin: 20px auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.title {
  text-align: center;
  color: #fff;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.question-form {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.options-container {
  display: flex;
  gap: 10px;
}

.option-input {
  flex: 1;
}

.correct-option-input {
  width: 100%;
}

.btn-add-question {
  background-color: #6a11cb;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s;
}

.btn-add-question:hover {
  background-color: #2575fc;
}

.question-list {
  list-style: none;
  padding: 0;
}

.question-item {
  background: #f7f8fa;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-text {
  margin-bottom: 10px;
}

.options {
  list-style: none;
  margin: 0;
  padding: 0;
}

.options li {
  font-size: 14px;
}

.option-label {
  font-weight: bold;
  color: #6a11cb;
}

.btn-delete {
  background-color: #ff4d4d;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-delete:hover {
  background-color: #d43d3d;
}
</style>
