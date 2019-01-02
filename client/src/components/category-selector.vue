<template>
  <div class="category-container">
    <input
      type="text"
      class="text"
      autocomplete="off"
      placeholder="Category"
      required
      v-model="categoryTitle"
      @click="toggleDropdown"
    >
    <span @click="toggleDropdown">V</span>
    <nav
      v-if="showCategorySelector"
      class="selector"
    >
      <ul class="selector-group">
        <category-item
          v-for="model in filteredChoices"
          :key="model.id"
          :model="model"
          :max-depth="isFiltered ? 0 : -1"
          v-on:itemSelected="selected"
        />
      </ul>
    </nav>
  </div>
</template>

<script>
import CategoryItem from './category-selector-item.vue';
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

export default {
  name: 'CategorySelector',
  props: {
    category: { type: Object, default: null }
  },
  components: {
    CategoryItem
  },
  data() {
    return {
      categoryTitle: this.category ? this.category.title : "",
      showCategorySelector: false,
    };
  },

  computed: {
    ...mapState('categories', {
      categoryTree: 'itemTree',
      categoryList: 'items'
    }),
    filteredChoices() {
      return this.categoryTree;
    },
    isFiltered() {
      return this.categoryTitle && this.categoryTitle != this.category.title;
    },
  },

  methods: {
    toggleDropdown() {
      this.showCategorySelector = !this.showCategorySelector;
    },

    close() {
      this.showCategorySelector = false;
    },

    selected(category) {
      this.$emit("itemSelected", category);
      this.showCategorySelector = false;
      this.categoryTitle = category.title;
    },

  },

  created() {
    this.$store.dispatch('categories/fetchAll');
  },

  updated() {
    // QnD hack for zebra stripes
    const zebraElements = [].slice.call(document.getElementsByClassName('zebra'));
    var counter = 0;
    zebraElements.forEach(element => {
      if (counter % 2 == 0) {
        element.className = element.className + " even";
      } else {
        element.className = element.className + " odd";
      }
      counter++;
    });
  }

}
</script>

<style>
</style>
