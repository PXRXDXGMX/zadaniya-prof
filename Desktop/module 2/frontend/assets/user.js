const { createApp } = Vue;

const apiBase = localStorage.getItem("API_BASE") || window.location.origin;

createApp({
  data() {
    return {
      apiBase,
      requests: [],
      createForm: { pet_name: "", pet_photo: null },
      createErrors: {},
      createLoading: false,
    };
  },
  async mounted() {
    const me = await this.api("/api/auth/me");
    if (!me.ok || !me.data.authenticated) {
      window.location.href = "/";
      return;
    }
    if (me.data.role === "admin") {
      window.location.href = "/groom/";
      return;
    }
    await this.loadRequests();
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
    async loadRequests() {
      const { ok, data } = await this.api("/api/user/requests");
      this.requests = ok ? data.results : [];
    },
    onPetPhotoChange(event) {
      this.createForm.pet_photo = event.target.files[0] || null;
    },
    async createRequest() {
      this.createErrors = {};
      this.createLoading = true;

      const formData = new FormData();
      formData.append("pet_name", this.createForm.pet_name);
      if (this.createForm.pet_photo) {
        formData.append("pet_photo", this.createForm.pet_photo);
      }

      const { ok, data } = await this.api("/api/user/requests", {
        method: "POST",
        body: formData,
      });
      this.createLoading = false;

      if (!ok) {
        this.createErrors = data.errors || {};
        return;
      }

      this.createForm = { pet_name: "", pet_photo: null };
      await this.loadRequests();
    },
    async removeRequest(id) {
      const { ok, data } = await this.api(`/api/user/requests/${id}`, { method: "DELETE" });
      if (!ok) {
        alert(data.message || "Ошибка удаления");
        return;
      }
      await this.loadRequests();
    },
    async logout() {
      await this.api("/api/auth/logout", { method: "POST" });
      window.location.href = "/";
    },
  },
}).mount("#app");
