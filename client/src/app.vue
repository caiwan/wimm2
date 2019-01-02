<template>
  <div id="app">
    <sidebar></sidebar>
    <div
      id="spinner"
      :class="{visible: spinnerVisible}"
    ></div>
    <div
      id="overlay"
      :class="{visible: overlayVisible}"
    ></div>
    <header-bar v-if="!isInitializing"></header-bar>
    <router-view
      id="default-router-view"
      v-if="!isInitializing"
    ></router-view>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex';

import HeaderBar from './containers/header-bar';
import io from './services/io'
import Sidebar from './components/sidebar';

export default {
  name: 'app',
  components: {
    Sidebar,
    HeaderBar
  },
  computed: {
    ...mapGetters('ui', [
      'overlayVisible', 'spinnerVisible'
    ]),
    ...mapState('app', [
      'isInitializing'
    ])
  },
  methods: {
    ...mapActions('ui', [
      'hideUi'
    ]),
    ...mapActions('app', [
      'initialized'
    ])
  },
  watch: {
    $route(route) {
      this.hideUi();
    }
  },
  async created() {
    await io.initialized;
    this.initialized();
  }
}
</script>

<style lang="scss" rel="stylesheet/scss">
@import "./scss/style";
</style>
