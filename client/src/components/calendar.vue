<template>
  <div class="calendar">
    <label for="calendar-date-from">Date from</label>
    <input id="calendar-date-from" type="date" :value="dateFrom" @input="onChanged('dateFrom', $event.target.value)">
    <label for="calendar-date-to">Date to</label>
    <input id="calendar-date-to" type="date" :value="dateTo" @input="onChanged('dateTo', $event.target.value)">
    <label for="calendar-interval" v-if="showInterval">Interval</label>
    <select id="calendar-interval" v-if="showInterval" :value="interval" @input="onChanged('interval', $event.target.value)">
      <option value="days">Days</option>
      <option value="weeks">Weeks</option>
      <option value="months">Months</option>
      <option value="years">Years</option>
    </select>
  </div>
</template>

<script>
  export default {
    props: {
      dateFrom: {
        required: true
      },
      dateTo: {
        required: true
      },
      interval: {
        required: false
      }
    },
    computed: {
      showInterval(){
        return this.interval !== undefined
      }
    },
    methods: {
      onChanged(property, value){
        this.$emit('change', property, value);
      }
    }
  }
</script>
