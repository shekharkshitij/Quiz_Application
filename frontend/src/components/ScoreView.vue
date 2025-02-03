<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">View Scores</h2>
    <div class="table-responsive">
      <table class="table table-striped table-bordered">
        <thead class="table-dark">
          <tr>
            <th>User</th>
            <th>Quiz</th>
            <th>Score</th>
            <th>Time Taken (mins)</th>
            <th>Attempted At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in scores" :key="score.id">
            <td>{{ score.user }}</td>
            <td>{{ score.quiz }}</td>
            <td>{{ score.total_scored }}</td>
            <td>{{ score.total_time_taken }}</td>
            <td>{{ new Date(score.time_stamp_of_attempt).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from "../api/api";

export default {
  name: "ScoreView",
  data() {
    return {
      scores: [],
    };
  },
  async created() {
    await this.fetchScores();
  },
  methods: {
    async fetchScores() {
      try {
        const response = await api.getScores();
        this.scores = response.data;
      } catch (error) {
        console.error("Failed to fetch scores:", error);
        alert("Unable to load scores. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

h2 {
  font-size: 1.8rem;
  color: #333;
}

.table {
  margin-top: 20px;
  font-size: 0.9rem;
}

.table-responsive {
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
}

thead.table-dark th {
  color: white;
  background-color: #343a40;
}

tr:hover {
  background-color: #f8f9fa;
}
</style>
