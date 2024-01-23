<template>
  <Header @changeView="changeView"></Header>
  <div id="app">
    <component :is="currentView.component" v-bind="currentView.props"></component>
  </div>
</template>


<script>
import FullIut from './components/FullIut.vue';
import Header from "@/components/Header.vue";
import RoomDetail from "@/components/roomDetail.vue";
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
      props: {}
    };
  },
  methods: {
    changeView(component, props) {
      console.log("caca",component,props);
      this.currentView = { component, props };
    }
  }
};
</script>


<style >
#app {
    padding-top: 80px; /* Adjust the padding to make space for the header */
}
</style>
