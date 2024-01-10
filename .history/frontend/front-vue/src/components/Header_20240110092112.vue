<!-- Template de header pour les pages ( barre de recherche ) -->
<!-- Le composant est modulaire et ne doit pas dépendre du reste de l'application -->
<template>
  <div class="header">
    
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Rechercher...">
        <button class="search-button">Rechercher</button>
    </div>

      <router-link to="/Carte">
        <i class="Carte"></i>
        <span class="Carte">Carte</span>
      </router-link>

    </div>
  </div>
</template>

<style>
.header {

    position: fixed;
    top: 0;
    left: 0;


    width:100%;
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #fff;
    color:black;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}


.search-container {
    display: flex;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    border-radius: 5px;
}

.search-input {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 5px 0 0 5px;
    font-size: 16px;
}

.search-button {
    background-color: #3498db;
    color: #fff;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 0 5px 5px 0;
    font-size: 16px;
}

.search-button:hover {
    background-color: #2980b9;
}

</style>