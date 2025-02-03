<template>
  <div class="manage-subjects">
    <!-- Navbar -->
    <!-- <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-brand">Quiz Management System</div>
        <div class="navbar-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <button @click="logout" class="nav-link btn-logout">Logout</button>
        </div>
      </div>
    </nav> -->

    <!-- Subjects Management -->
    <div v-if="isAdmin" class="subjects-container">
      <h2 class="title">Subjects</h2>
      <form @submit.prevent="addSubject" class="subject-form">
        <input
          v-model="name"
          class="form-control"
          placeholder="Enter Subject Name"
          required
        />
        <textarea
          v-model="description"
          class="form-control"
          placeholder="Enter Subject Description"
        ></textarea>
        <button type="submit" class="btn-add">Add Subject</button>
      </form>
      <ul class="subject-list">
        <li v-for="subject in subjects" :key="subject.id" class="subject-item">
          <div class="subject-details">
            <span class="subject-name">{{ subject.name }}</span>
            <div class="subject-actions">
              <button @click="viewChapters(subject.id)" class="btn-action">
                View Chapters
              </button>
              <button @click="deleteSubject(subject.id)" class="btn-action btn-delete">
                Delete
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  name: "ManageSubjects",
  data() {
    return {
      subjects: [],
      name: "",
      description: "",
    };
  },
  computed: {
    ...mapGetters(["isAdmin"]),
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await axios.get("http://localhost:5000/api/v1/subjects", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
        });
        this.subjects = response.data;
      } catch (error) {
        console.error(
          "Error fetching subjects:",
          error.response?.data?.message || error.message
        );
        alert("Failed to load subjects. Please try again.");
      }
    },
    async addSubject() {
      if (this.name.trim() === "") {
        alert("Subject name is required.");
        return;
      }
      try {
        await axios.post(
          "http://localhost:5000/api/v1/subjects",
          {
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
        this.fetchSubjects();
      } catch (error) {
        console.error(
          "Error adding subject:",
          error.response?.data?.message || error.message
        );
        alert("Failed to add subject. Please try again.");
      }
    },
    async deleteSubject(id) {
      if (confirm("Are you sure you want to delete this subject?")) {
        try {
          await axios.delete(`http://localhost:5000/api/v1/subjects/${id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
          });
          this.fetchSubjects();
        } catch (error) {
          console.error(
            "Error deleting subject:",
            error.response?.data?.message || error.message
          );
          alert("Failed to delete subject. Please try again.");
        }
      }
    },
    viewChapters(subjectId) {
      this.$router.push({ name: "ManageChapters", params: { subjectId } });
    },
    logout() {
      localStorage.removeItem("auth_token");
      this.$router.push("/login");
    },
  },
  created() {
    this.fetchSubjects();
  },
};
</script>


<style scoped>
/* Navbar Styling */
.navbar {
  background: #2d6a4f; /* Environmental green */
  color: white;
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-brand {
  font-size: 20px;
  font-weight: bold;
}

.navbar-links {
  display: flex;
  gap: 15px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.nav-link:hover {
  text-decoration: underline;
}

.btn-logout {
  background: none;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.btn-logout:hover {
  text-decoration: underline;
}

/* Main Container Styling */
.manage-subjects {
  background: linear-gradient(to bottom right, #95d5b2, #74c69d);
  min-height: 100vh;
  padding: 20px;
  color: #333;
}

.subjects-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #2d6a4f;
}

/* Form Styling */
.subject-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

.btn-add {
  background: #40916c;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.btn-add:hover {
  background: #2d6a4f;
}

/* Subject List Styling */
.subject-list {
  list-style: none;
  padding: 0;
}

.subject-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  background: #d8f3dc;
  border-radius: 5px;
}

.subject-details {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.subject-name {
  font-size: 18px;
  font-weight: bold;
}

.subject-actions {
  display: flex;
  gap: 10px;
}

.btn-action {
  background: #52b788;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-action:hover {
  background: #40916c;
}

.btn-delete {
  background: #e63946;
}

.btn-delete:hover {
  background: #d62828;
}
</style>
