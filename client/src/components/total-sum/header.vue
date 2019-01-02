<template>
  <div>
    <div class="header-label">Total sum over time</div>
    <div class="fill"></div>

    <button class="i i-date_range" @click="toggleCalendar"></button>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

  export default {
    methods: {
      ...mapActions('totalSum', ['toggleCalendar'])
    }
  }
</script>


<style lang="scss" rel="stylesheet/scss">

</style>
