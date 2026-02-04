const cartItems = document.getElementById("cart-items");
const cartTotal = document.getElementById("cart-total");
const checkoutButton = document.getElementById("checkout");
const cartMessage = document.getElementById("cart-message");

function formatCurrency(value) {
  return new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
  }).format(value);
}

async function loadCart() {
  const response = await api.get("/carrello");
  if (response.error) {
    cartMessage.textContent = response.error;
    return;
  }
  cartItems.innerHTML = "";
  response.items.forEach((item) => {
    const element = document.createElement("div");
    element.className = "cart-item";
    element.innerHTML = `
      <div>
        <h3>${item.title}</h3>
        <p>Persone: ${item.people}</p>
        <p>Vino: ${item.wine_name || "Nessuno"}</p>
      </div>
      <div>
        <p>${formatCurrency(item.subtotal)}</p>
        <button class="button button-secondary" data-id="${item.id}">Rimuovi</button>
      </div>
    `;
    element.querySelector("button").addEventListener("click", () => removeItem(item.id));
    cartItems.appendChild(element);
  });
  cartTotal.textContent = `Totale: ${formatCurrency(response.total)}`;
}

async function removeItem(itemId) {
  await api.del("/carrello/remove", { item_id: itemId });
  loadCart();
}

checkoutButton.addEventListener("click", async () => {
  const response = await api.post("/checkout", {});
  cartMessage.textContent = response.message || response.error;
  loadCart();
});

loadCart();
