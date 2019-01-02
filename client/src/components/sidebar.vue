<template>
  <div id="sidebar">
    <ol :class="{visible}">
      <router-link
        tag="li"
        :to="{name: 'index'}"
      >Item overview</router-link>
      <router-link
        tag="li"
        :to="{name: 'budget-editor'}"
      >Budget, savings and debt</router-link>
      <router-link
        tag="li"
        :to="{name: 'category-editor'}"
      >Categories</router-link>
      <router-link
        tag="li"
        :to="{name: 'graph:total-sum'}"
      >Total sum over time</router-link>
      <router-link
        tag="li"
        :to="{name: 'graph:tag-total'}"
      >Total sum by tags</router-link>
      <router-link
        tag="li"
        :to="{name: 'graph:tag-time'}"
      >Tag sum over time</router-link>
      <router-link
        tag="li"
        :to="{name: 'import-export'}"
      >Import / export</router-link>
      <router-link
        tag="li"
        :to="{name: 'smart-import'}"
      >Smart bulk import (experimental)</router-link>
    </ol>
    <div
      class="overlay-close"
      v-if="visible"
      @click="toggle()"
    ></div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  computed: {
    ...mapState("ui", {
      visible: "sidebarVisible"
    })
  },
  methods: {
    ...mapActions("ui", {
      toggle: "toggleSidebar"
    })
  }
};
</script>

<style lang="scss" rel="stylesheet/scss">
@import "../scss/consts";

#sidebar {
  ol {
    background: $bg-ui;
    bottom: 0;
    box-sizing: border-box;
    left: 0;
    list-style: none;
    margin: 0;
    padding: 0;
    position: fixed;
    top: 0;
    transform: translateX(-100%);
    transition: $sidebar-transition;
    width: $sidebar-width;
    z-index: $layer-70;

    li {
      border-bottom: $border;
      box-sizing: border-box;
      padding: $sidebar-li-padding;
      cursor: pointer;
      user-select: none;

      &:hover {
        background: $sidebar-li-hover;
      }

      &.router-link-active {
        background: $sidebar-li-link-active;
      }
    }

    &.visible {
      transform: none;
    }
  }
}
</style>
