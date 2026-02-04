const api = {
  async get(path) {
    const response = await fetch(path, { credentials: "include" });
    return response.json();
  },
  async post(path, data) {
    const response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(data),
    });
    return response.json();
  },
  async del(path, data) {
    const response = await fetch(path, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(data),
    });
    return response.json();
  },
};
