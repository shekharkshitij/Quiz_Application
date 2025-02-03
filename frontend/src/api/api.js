import axios from "axios";

// Create Axios instance
const api = axios.create({
  baseURL: "http://localhost:5000/api/v1", // Replace with your backend base URL if different
  timeout: 10000, // Optional: Set a timeout for requests
});

// Add a request interceptor to include the Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("auth_token"); // Retrieve token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Add the token to headers
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Function to set the token (useful for login)
export const setAuthToken = (token) => {
  localStorage.setItem("auth_token", token); // Store the token in localStorage
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`; // Apply the token immediately
};

// Function to remove the token (useful for logout)
export const removeAuthToken = () => {
  localStorage.removeItem("auth_token"); // Remove the token from localStorage
  delete api.defaults.headers.common["Authorization"]; // Remove it from Axios headers
};

// Auth API
export const login = async (credentials) => {
  try {
    const response = await api.post("/login", credentials); // Login request
    const token = response.data.auth_token; // Extract token from response
    if (token) {
      setAuthToken(token); // Set the token globally
    }
    return response.data; // Return the full response data
  } catch (error) {
    console.error("Error during login:", error.response?.data || error.message);
    throw error;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post("/register", userData); // Register request
    return response.data;
  } catch (error) {
    console.error("Error during registration:", error.response?.data || error.message);
    throw error;
  }
};

export const logout = async () => {
  removeAuthToken(); // Remove token globally
};

// Subject API
export const getSubjects = async () => {
  try {
    const response = await api.get("/subjects"); // Fetch all subjects
    return response.data;
  } catch (error) {
    console.error("Error fetching subjects:", error.response?.data || error.message);
    throw error;
  }
};

export const addSubject = async (subjectData) => {
  try {
    const response = await api.post("/subjects", subjectData); // Add a new subject
    return response.data;
  } catch (error) {
    console.error("Error adding subject:", error.response?.data || error.message);
    throw error;
  }
};

export const updateSubject = async (subjectId, subjectData) => {
  try {
    const response = await api.put(`/subjects/${subjectId}`, subjectData); // Update a subject
    return response.data;
  } catch (error) {
    console.error("Error updating subject:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteSubject = async (subjectId) => {
  try {
    const response = await api.delete(`/subjects/${subjectId}`); // Delete a subject
    return response.data;
  } catch (error) {
    console.error("Error deleting subject:", error.response?.data || error.message);
    throw error;
  }
};

// Chapter API
export const getChapters = async (subjectId) => {
  try {
    const response = await api.get(`/subjects/${subjectId}/chapters`); // Fetch all chapters for a subject
    return response.data;
  } catch (error) {
    console.error("Error fetching chapters:", error.response?.data || error.message);
    throw error;
  }
};

export const addChapter = async (chapterData) => {
  try {
    const response = await api.post("/chapters", chapterData); // Add a new chapter
    return response.data;
  } catch (error) {
    console.error("Error adding chapter:", error.response?.data || error.message);
    throw error;
  }
};

export const updateChapter = async (chapterId, chapterData) => {
  try {
    const response = await api.put(`/chapters/${chapterId}`, chapterData); // Update a chapter
    return response.data;
  } catch (error) {
    console.error("Error updating chapter:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteChapter = async (chapterId) => {
  try {
    const response = await api.delete(`/chapters/${chapterId}`); // Delete a chapter
    return response.data;
  } catch (error) {
    console.error("Error deleting chapter:", error.response?.data || error.message);
    throw error;
  }
};

// Quiz API
export const getQuizzes = async (chapterId) => {
  const response = await api.get(`/quizzes?chapter_id=${chapterId}`);
  return response.data;
};

export const addQuiz = async (quizData) => {
  try {
    const response = await api.post("/quizzes", quizData); // Add a new quiz
    return response.data;
  } catch (error) {
    console.error("Error adding quiz:", error.response?.data || error.message);
    throw error;
  }
};

export const updateQuiz = async (quizId, quizData) => {
  try {
    const response = await api.put(`/quizzes/${quizId}`, quizData); // Update a quiz
    return response.data;
  } catch (error) {
    console.error("Error updating quiz:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteQuiz = async (quizId) => {
  try {
    const response = await api.delete(`/quizzes/${quizId}`); // Delete a quiz
    return response.data;
  } catch (error) {
    console.error("Error deleting quiz:", error.response?.data || error.message);
    throw error;
  }
};

// Question API
export const getQuestions = async (quizId) => {
  try {
    const response = await api.get(`/quizzes/${quizId}/questions`); // Fetch all questions for a quiz
    return response.data;
  } catch (error) {
    console.error("Error fetching questions:", error.response?.data || error.message);
    throw error;
  }
};

export const addQuestion = async (questionData) => {
  try {
    const response = await api.post("/questions", questionData); // Add a new question
    return response.data;
  } catch (error) {
    console.error("Error adding question:", error.response?.data || error.message);
    throw error;
  }
};

export const updateQuestion = async (questionId, questionData) => {
  try {
    const response = await api.put(`/questions/${questionId}`, questionData); // Update a question
    return response.data;
  } catch (error) {
    console.error("Error updating question:", error.response?.data || error.message);
    throw error;
  }
};

export const deleteQuestion = async (questionId) => {
  try {
    const response = await api.delete(`/questions/${questionId}`); // Delete a question
    return response.data;
  } catch (error) {
    console.error("Error deleting question:", error.response?.data || error.message);
    throw error;
  }
};

// Score API
export const getScores = async () => {
  try {
    const response = await api.get("/scores"); // Fetch all scores
    return response.data;
  } catch (error) {
    console.error("Error fetching scores:", error.response?.data || error.message);
    throw error;
  }
};

// Export all API functions
export default {
  login,
  register,
  logout,
  getSubjects,
  addSubject,
  updateSubject,
  deleteSubject,
  getChapters,
  addChapter,
  updateChapter,
  deleteChapter,
  getQuizzes,
  addQuiz,
  updateQuiz,
  deleteQuiz,
  getQuestions,
  addQuestion,
  updateQuestion,
  deleteQuestion,
  getScores,
};
