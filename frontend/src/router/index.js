import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

// Import Components and Views
import AdminDashboardComponent from "../components/AdminDashboardComponent.vue";
import LoginComponent from "../components/LoginComponent.vue";
import ManageChapters from "../components/ManageChapters.vue";
import ManageQuestions from "../components/ManageQuestions.vue";
import ManageQuizzes from "../components/ManageQuizzes.vue";
import ManageSubjects from "../components/ManageSubjects.vue";
import RegisterComponent from "../components/RegisterComponent.vue";
import ScoreView from "../components/ScoreView.vue";
import StartQuizComponent from "../components/StartQuizComponent.vue";
import TakeQuizComponent from "../components/TakeQuizComponent.vue";
import UserDashboardComponent from "../components/UserDashboardComponent.vue";
import HomeComponent from "../views/HomeView.vue";

const routes = [
  // Public Routes
  { path: "/", name: "Home", component: HomeComponent },
  { path: "/login", name: "Login", component: LoginComponent },
  { path: "/register", name: "Register", component: RegisterComponent },

  // Admin Routes
  {
    path: "/admin-dashboard",
    name: "AdminDashboard",
    component: AdminDashboardComponent,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/manage-subjects",
    name: "ManageSubjects",
    component: ManageSubjects,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/manage-subjects/:subjectId/chapters",
    name: "ManageChapters",
    component: ManageChapters,
    props: true,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/manage-chapters/:chapterId/quizzes",
    name: "ManageQuizzes",
    component: ManageQuizzes,
    props: true,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/manage-quizzes/:quizId/questions",
    name: "ManageQuestions",
    component: ManageQuestions,
    props: true,
    meta: { requiresAuth: true, role: "admin" },
  },

  // User Routes
  {
    path: "/user-dashboard",
    name: "UserDashboard",
    component: UserDashboardComponent,
    meta: { requiresAuth: true, role: "user" },
  },
  {
    path: "/take-quiz",
    name: "TakeQuiz",
    component: TakeQuizComponent,
    meta: { requiresAuth: true }, // Ensure only authenticated users can access
  },
  {
    path: '/start-quiz/:quizId',
    name: 'StartQuiz', // Unique name for starting a specific quiz
    component: StartQuizComponent, // Separate component for handling the quiz-taking process
    meta: { requiresAuth: true }, // Optional meta field for authentication
  },
  {
    path: "/view-scores",
    name: "ViewScores",
    component: ScoreView,
    meta: { requiresAuth: true, roles: ["admin", "user"] },
  },

  // Redirect any unmatched routes to Home
  { path: "/:catchAll(.*)", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard for Authentication and Role-Based Access Control
router.beforeEach((to, from, next) => {
  const token = store.state.token; // Token from Vuex store
  const user = store.state.user; // User info from Vuex store

  // Check if route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      console.warn("No token found. Redirecting to login.");
      return next({ name: "Login" });
    }

    // Check if user has the required role
    if (to.meta.role && user?.role !== to.meta.role) {
      console.warn("Role mismatch. Redirecting to appropriate dashboard.");
      return next({ name: user?.role === "admin" ? "AdminDashboard" : "UserDashboard" });
    }
  }

  // Allow access if all checks pass
  next();
});

export default router;
