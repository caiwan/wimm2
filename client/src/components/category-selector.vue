<template>
  <div class="category-container">
    <!-- TODO: add blur and focus properly -->

    <!-- @blur="close" -->

    <div class="category-input">
      <input
        type="text"
        class="text"
        autocomplete="off"
        placeholder="Category"
        required
        v-model="categoryTitle"
        @keydown.esc="close"
        @click="toggle"
      >
      <span @click="toggle">V</span>
    </div>
    <nav
      v-if="showCategorySelector"
      class="selector"
      v-box-placement
      @mousedown="deferBlur = true"
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
      showCategorySelector: false, deferBlur: false
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
    toggle() {
      this.showCategorySelector = !this.showCategorySelector;
    },

    close() {
      if (!this.deferBlur) {
        this.showCategorySelector = false;
      }
    },

    open() {
      this.showCategorySelector = true;
    },

    selected(category) {
      this.$emit("itemSelected", category);
      this.showCategorySelector = false;
      this.categoryTitle = category.title;
      this.deferBlur = false;
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
        element.classList.add('even');
      } else {
        element.classList.add('odd');
      }
      counter++;
    });
  },

  directives: {
    boxPlacement:
      {
        inserted(el, binding, vnode) {
          const rect = el.getBoundingClientRect();
          const p = rect.top + rect.height - window.innerHeight;
          if (p > 0) {
            el.classList.add('dropup');
            console.log('up!', p);
          } else {
            console.log('down', p);
          }
        },

        unbind(el, binding, vnode) {
          el.classList.remove('dropup');
        }

      }
  }

}
</script>

<style>
</style>
