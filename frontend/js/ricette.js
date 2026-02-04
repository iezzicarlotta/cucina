const recipesContainer = document.getElementById("recipes");
const genreFilter = document.getElementById("genre-filter");
const userInfo = document.getElementById("user-info");
let isAuthenticated = false;

async function loadSession() {
  const session = await api.get("/session");
  if (session.authenticated) {
    isAuthenticated = true;
    userInfo.textContent = `Ciao, ${session.username}`;
  } else {
    userInfo.textContent = "Non autenticato";
  }
}

function formatCurrency(value) {
  return new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
  }).format(value);
}

async function loadRecipes() {
  const genre = genreFilter.value;
  const path = genre ? `/ricette?genere=${encodeURIComponent(genre)}` : "/ricette";
  const recipes = await api.get(path);

  recipesContainer.innerHTML = "";
  recipes.forEach((recipe) => {
    const card = document.createElement("article");
    card.className = "card";

    card.innerHTML = `
      <img src="${recipe.image_url}" alt="${recipe.title}" />
      <div>
        <h2>${recipe.title}</h2>
        <p class="notice">${recipe.description}</p>
      </div>
      <div>
        <p>Costo per persona: <strong>${formatCurrency(recipe.costo_per_persona)}</strong></p>
      </div>
      <button class="button button-primary" data-id="${recipe.id}">
        Aggiungi al carrello
      </button>
    `;

    const button = card.querySelector("button");
    if (!isAuthenticated) {
      button.disabled = true;
      button.textContent = "Accedi per acquistare";
    }
    button.addEventListener("click", () => addToCart(recipe.id));

    recipesContainer.appendChild(card);
  });
}

async function addToCart(recipeId) {
  const people = prompt("Numero di persone?");
  if (!people) {
    return;
  }
  const response = await api.post("/carrello/add", {
    recipe_id: recipeId,
    people: Number(people),
  });
  alert(response.message || response.error);
}

genreFilter.addEventListener("change", loadRecipes);

loadSession().then(loadRecipes);
