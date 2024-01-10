<!-- Template de header pour les pages ( barre de recherche ) -->
<template>
  <div class="header">
    <div class="header__logo">
      <router-link to="/">
        <img src="../assets/logo.png" alt="logo" />
      </router-link>
    </div>
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
    width:100%;
    
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>