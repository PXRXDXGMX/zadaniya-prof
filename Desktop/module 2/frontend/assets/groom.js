const { createApp } = Vue;

const apiBase = localStorage.getItem("API_BASE") || window.location.origin;

createApp({
  data() {
    return {
      apiBase,
      requests: [],
      resultPhotos: {},
      itemErrors: {},
    };
  },
  async mounted() {
    const me = await this.api("/api/auth/me");
    if (!me.ok || !me.data.authenticated || me.data.role !== "admin") {
      window.location.href = "/";
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
      const { ok, data } = await this.api("/api/groom/requests");
      this.requests = ok ? data.results : [];
    },
    onResultChange(event, id) {
      this.resultPhotos[id] = event.target.files[0] || null;
    },
    async toProcessing(id) {
      const formData = new FormData();
      formData.append("status", "processing");
      const { ok, data } = await this.api(`/api/groom/requests/${id}/status`, {
        method: "POST",
        body: formData,
      });
      if (!ok) {
        alert(data.message || "Ошибка смены статуса");
        return;
      }
      await this.loadRequests();
    },
    async toCompleted(id) {
      this.itemErrors[id] = "";
      const formData = new FormData();
      formData.append("status", "completed");
      if (this.resultPhotos[id]) {
        formData.append("result_photo", this.resultPhotos[id]);
      }
      const { ok, data } = await this.api(`/api/groom/requests/${id}/status`, {
        method: "POST",
        body: formData,
      });
      if (!ok) {
        this.itemErrors[id] = data?.errors?.result_photo || data.message || "Ошибка";
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
