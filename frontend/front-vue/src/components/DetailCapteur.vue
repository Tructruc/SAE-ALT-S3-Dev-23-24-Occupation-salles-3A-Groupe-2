<script>

export default {
  name: 'DetailCapteur',
  props: {
    name: {
      type: String,
      required: ""
    },
    deveui: {
      type: String,
      default: ""
    },
    building: {
      type: String,
      default: ''
    },
    floor: {
      type: String,
      default: ''
    },
    externalPower: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<template>
  <div>
    <h3>{{name}}</h3>
    <p>Deveui : {{deveui}}</p>
    <p>Batiment : {{building}}</p>
    <p>Étage : {{floor}}</p>
    <p>Alimentation externe : {{externalPower ?  "oui" : "non"}}</p>
  </div>
</template>

<style scoped>
div {
  width: 300px;
  height: 500px;
  background-color: var(--color-background-mute);
  padding: 30px;
  border-radius: 5px;
}

h3 {
  font-weight: bold;
}


</style>