<template>
  <Header @changeView="changeView"></Header>
  <div id="app">
    <h2>Bienvenue sur le tableau de bord de visualisation des données des salles</h2>
    <div class="presentation">
      <p style="width: 40vw;">
        Sur ce tableau de bord mono-page, vous avez la possibilité de visualiser les données des capteurs AM107 situés dans les salles de l'IUT de Blagnac. <br>
        Grâce au plan interactif ci-dessous, à l'onglet "Salles" ou via la fonction de recherche et les recommandations qu'elle propose, vous pouvez accéder facilement à l'information désirée.
      </p> 
      <img src="https://upload.wikimedia.org/wikipedia/fr/8/8a/Logo_IUT_Blagnac.png" alt="Logo IUT Blagnac" style="display: block; margin-left: 0; width: 16vw;">

    </div>
    <component :is="currentView.component" v-bind="currentView.props" :key="key"></component>
  </div>
</template>


<script>
import FullIut from './components/batiments/FullIut.vue';
import Header from "@/components/Header.vue";
import RoomDetail from "@/components/roomDetail/roomDetail.vue";
import ListeSalles from "@/components/ListeSalles.vue";

export default {
  components: {
    RoomDetail,
    Header,
    FullIut,
    ListeSalles
  },
  data() {
    return {
      currentView: 'FullIut',
      props: {},
      key: "",
    };
  },
  methods: {
    changeView(component, props) {
      if ("room" in props) {this.key = props.room}
      this.currentView = { component, props };
    }
  },
  mounted() {
    this.changeView("FullIut", {});
  }
};
</script>


<style scoped>
  #app {
    width: 100%;
    padding-top: 80px; /* Adjust the padding to make space for the header */
    max-width: 80vw;
    justify-content: center;
  }
  .presentation {
    display: flex;
    flex-direction: row;
    align-items: flex-start; /* Align items to the start of the container */
    justify-content: flex-start; /* Start items from the beginning */
    margin: 0; /* Remove any default margin */
    padding: 0; /* Remove any default padding */
    background-color: var(--color-background-hover);
    width: auto;
    margin: 2vh 2vw;
    padding: 2vh 2vw;
    border-radius: 10px;
    gap: 3vh;
}
</style>
