const form = document.getElementById("login-form");
const message = document.getElementById("login-message");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const payload = {
    identifier: formData.get("identifier"),
    password: formData.get("password"),
  };
  const response = await api.post("/login", payload);
  if (response.error) {
    message.textContent = response.error;
    return;
  }
  window.location.href = "index.html";
});
