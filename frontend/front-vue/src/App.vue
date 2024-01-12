<template>
  <div id="app">
    <Header></Header>
    <room-detail></room-detail>
    <FullIut />
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
};
</script>


<style >

</style>
