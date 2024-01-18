<template>
  <div id="app">
    <Header @changeView="changeView"></Header>
    <component :is="currentView"></component>
  </div>
</template>


<script>
import FullIut from './components/FullIut.vue';
import Header from "@/components/Header.vue";
import RoomDetail from "@/components/roomDetail.vue";

export default {
  components: {
    RoomDetail,
    Header,
    FullIut
  },
  data() {
    return {
      currentView: 'FullIut'
    };
  },
  methods: {
    changeView(view) {
      this.currentView = view;
    }
  }
};
</script>


<style >
#app {
    padding-top: 80px; /* Adjust the padding to make space for the header */
}
</style>
