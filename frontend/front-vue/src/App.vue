<template>
  <Header @changeView="changeView"></Header>
  <div id="app">
    <component :is="currentView.component" v-bind="currentView.props" :key="key"></component>
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


<style >
#app {
    padding-top: 80px; /* Adjust the padding to make space for the header */
}
</style>
