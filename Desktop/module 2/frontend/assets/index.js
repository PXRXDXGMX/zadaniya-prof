const { createApp } = Vue;

const apiBase = localStorage.getItem("API_BASE") || window.location.origin;

createApp({
  data() {
    return {
      apiBase,
      completed: [],
      loginForm: { username: "", password: "" },
      registerForm: {
        full_name: "",
        username: "",
        email: "",
        password: "",
        password_repeat: "",
        consent: false,
      },
      errors: {},
      loginError: "",
      loadingLogin: false,
      loadingRegister: false,
    };
  },
  mounted() {
    this.loadCompleted();
  },
  methods: {
    async api(path, options = {}) {
      const response = await fetch(`${this.apiBase}${path}`, {
        credentials: "include",
        ...options,
      });
      let data = {};
      try {
        data = await response.json();
      } catch (e) {}
      return { ok: response.ok, data };
    },
    async loadCompleted() {
      const { ok, data } = await this.api("/api/public/completed");
      this.completed = ok ? data.results : [];
    },
    async login() {
      this.loginError = "";
      this.loadingLogin = true;
      const { ok, data } = await this.api("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.loginForm),
      });
      this.loadingLogin = false;

      if (!ok) {
        this.loginError = data.message || "Ошибка входа";
        return;
      }

      window.location.href = data.role === "admin" ? "/groom/" : "/user/";
    },
    async register() {
      this.errors = {};
      this.loadingRegister = true;
      const { ok, data } = await this.api("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.registerForm),
      });
      this.loadingRegister = false;

      if (!ok) {
        this.errors = data.errors || {};
        if (!Object.keys(this.errors).length && data.message) {
          this.loginError = data.message;
        }
        return;
      }

      window.location.href = "/user/";
    },
  },
}).mount("#app");
