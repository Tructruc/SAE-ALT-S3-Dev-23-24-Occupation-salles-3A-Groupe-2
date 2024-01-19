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
  width: 16vw;
  height: 100%;
  background-color: var(--color-background-mute);
  padding: 2rem;
  border-radius: 5px;
}

h3 {
  font-weight: bold;
}

p {
  word-wrap: break-word;
}

</style>