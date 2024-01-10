<!-- Template de header pour les pages ( barre de recherche ) -->
<!-- Le composant est modulaire et ne doit pas dépendre du reste de l'application -->
<template>
  <div class="header">

    <div style="display:flex; justify-content:space-between; width:30%;">
        <!-- on met des liens vers la page d'accueil de google-->
        <a href="/Accueil" target="_self">Accueil</a>
        
        <a href="/Carte" target="_self">Carte</a>

        <a href="https://www.example.com/" target="_self">Example.com</a>
    </div>
    
    <div class="search-container">
        <input type="text" class="search-input" placeholder="Rechercher salle ...">
        <button type="submit" class="search-button">
        </button>
        <font-awesome-icon :icon="['fas', 'magnifying-glass']" />

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
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.search-container {
    display: flex;
    width:30%;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
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