<template>
  <div id="header">
    <button
      id="menu-btn"
      class="i i-menu"
      @click="toggleSidebar()"
    ></button>
    <router-view
      name="header"
      id="header-router-view"
    ></router-view>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  methods: {
    ...mapActions('ui', ['toggleSidebar'])
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
</style>
