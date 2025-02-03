<template>
  <div class="manage-chapters yellow-page" >
    <h1 class="title">Chapters</h1>
    <form @submit.prevent="addChapter" class="chapter-form">
      <input
        v-model="name"
        placeholder="Enter Chapter Name"
        required
        class="form-control input-field"
      />
      <textarea
        v-model="description"
        placeholder="Enter Chapter Description"
        class="form-control input-field"
      ></textarea>
      <button type="submit" class="btn btn-add">Add Chapter</button>
    </form>
    <ul class="chapter-list">
      <li v-for="chapter in chapters" :key="chapter.id" class="chapter-item">
        <div class="chapter-details">
          <h5 class="chapter-name">{{ chapter.name }}</h5>
          <p class="chapter-description">{{ chapter.description }}</p>
        </div>
        <div class="chapter-actions">
          <button class="btn btn-view" @click="viewQuizzes(chapter.id)">
            View Quizzes
          </button>
          <button class="btn btn-delete" @click="deleteChapter(chapter.id)">
            Delete
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ManageChapters",
  props: ["subjectId"],
  data() {
    return {
      chapters: [],
      name: "",
      description: "",
    };
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/v1/chapters/subject/${this.subjectId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
          }
        );
        this.chapters = response.data;
      } catch (error) {
        console.error("Error fetching chapters:", error.message);
        alert("Failed to load chapters. Please try again.");
      }
    },
    async addChapter() {
      try {
        await axios.post(
          "http://localhost:5000/api/v1/chapters",
          {
            subject_id: this.subjectId,
            name: this.name,
            description: this.description,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
          }
        );
        this.name = "";
        this.description = "";
        this.fetchChapters();
      } catch (error) {
        console.error("Error adding chapter:", error.message);
        alert("Failed to add chapter. Please try again.");
      }
    },
    async deleteChapter(id) {
      try {
        await axios.delete(`http://localhost:5000/api/v1/chapters/${id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
        });
        this.fetchChapters();
      } catch (error) {
        console.error("Error deleting chapter:", error.message);
        alert("Failed to delete chapter. Please try again.");
      }
    },
    viewQuizzes(chapterId) {
      this.$router.push({ name: "ManageQuizzes", params: { chapterId } });
    },
  },
  created() {
    this.fetchChapters();
  },
};
</script>

<style scoped>

.yellow-page {
  background-color: #ffeb3b; /* Bright Yellow */
}

.manage-chapters {
  max-width: 900px;
  margin: 20px auto;
  padding: 30px;
  background: linear-gradient(to bottom right, #ffefba, #ffc107); /* Yellow gradient */
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  color: #212529;
}

.title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  font-weight: bold;
}

.chapter-form {
  margin-bottom: 20px;
  padding: 20px;
  background: rgba(255, 193, 7, 0.2); /* Light orange */
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.chapter-form input,
.chapter-form textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.chapter-form button {
  background-color: #ff9800; /* Orange */
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  font-weight: bold;
}

.chapter-form button:hover {
  background-color: #e65100; /* Darker orange */
}

.chapter-list {
  list-style: none;
  padding: 0;
}

.chapter-item {
  background: rgba(255, 193, 7, 0.2); /* Light orange */
  margin-bottom: 15px;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.chapter-details h5 {
  margin-bottom: 5px;
  color: #212529;
}

.chapter-details p {
  color: #495057;
}

.chapter-actions {
  display: flex;
  gap: 15px;
}

.btn {
  padding: 8px 15px;
  font-size: 14px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  color: #fff;
}

.btn-view {
  background-color: #28a745; /* Green */
}

.btn-view:hover {
  background-color: #218838; /* Darker green */
}

.btn-delete {
  background-color: #dc3545; /* Red */
}

.btn-delete:hover {
  background-color: #c82333; /* Darker red */
}
</style>
