<template>
  <div class="settings-bar">
    <div class="bar" :class="{visible}">
      <slot></slot>
    </div>
    <div class="overlay-close" v-if="visible" @click="hide"></div>
  </div>
</template>

<script>
  export default {
    props: {
      visible: {
        required: true,
        default: () => false
      }
    },
    methods: {
      hide(){
        this.$emit('hide');
      }
    }
  }
</script>

<style lang="scss" rel="stylesheet/scss">
  @import '../scss/consts';

  .settings-bar {
    .bar {
      background: $bg-ui;
      position: fixed;
      z-index: $layer-60;
      top: 0;
      bottom: 0;
      width: $sidebar-width;
      right: 0;
      transform: translateX(100%);
      transition: 0.2s ease transform;
      padding: $sidebar-li-padding;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;

      &.visible {
        transform: none;
      }
    }
  }
</style>
