<template>
  <div id="app">
    <RenderJSON />
  </div>
</template>

<script>
import RenderJSON from './components/RenderJSON.vue'

export default {
  name: 'App',
  components: {
    RenderJSON
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
