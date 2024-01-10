<!-- Template de header pour les pages ( barre de recherche ) -->
<!-- Le composant est modulaire et ne doit pas dépendre du reste de l'application -->
<template>
  <div class="header">
    <div class="header__search">
      <input
        type="text"
        placeholder="Rechercher un produit"
        v-model="search"
        @keyup.enter="searchProduct"
      />
      <button @click="searchProduct">
        <i class="fas fa-search"></i>
      </button>
    </div>
    <div class="header__links">
      <router-link to="/cart">
        <i class="fas fa-shopping-cart"></i>
        <span class="header__links__cart">Panier</span>
        <span class="header__links__cart__number">{{ cartNumber }}</span>
      </router-link>
      <router-link to="/login">
        <i class="fas fa-user"></i>
        <span class="header__links__cart">Connexion</span>
      </router-link>
    </div>
  </div>
</template>

<style>
.header {
    position: sticky;
    top: 0;
    left: 0;

    width:100vw;
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #fff;
    color:black;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>