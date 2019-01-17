<template>
  <div class="category-container">

    <div class="category-input">
      <!-- TODO: proper keyboard mgmt like it was done in tags  -->
      <input
        type="text"
        class="text"
        autocomplete="off"
        placeholder="Category"
        required
        v-model="categoryTitle"
        @input="inputChanged"
        @keydown="keydown"
        @click="toggle"
        @blur="close"
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
        <!-- TODO: select item w/ mouse hover + model -->
        <category-item
          v-for="model in filteredChoices"
          :key="model.id"
          :model="model"
          :selectedItem="selectedCategory"
          :max-depth="categoryTreeMaxDepth"
          v-on:itemSelected="selected"
          v-on:selectionChanged="selectionChanged"
        />
      </ul>
    </nav>
  </div>
</template>

<script>
import CategoryItem from './category-selector-item.vue';
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";

// TODO: -> util
const zebraify = function (element) {
  // QnD hack for zebra stripes
  const zebraElements = [].slice.call(element.getElementsByClassName('zebra'));
  var counter = 0;
  zebraElements.forEach(element => {
    if (counter % 2 == 0) {
      element.classList.add('even');
    } else {
      element.classList.add('odd');
    }
    counter++;
  });
}

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
      categoryTitle: this.category != null ? this.category.title : "",
      selectedCategory: null, _selectedIndex: 0, _selectDirection: 1,
      showCategorySelector: false, deferBlur: false,
      filteredChoices: [], _requestUpdate: false, _isUpdating: false,
      // isFiltered: false,
      // categoryTreeMaxDepth: 0
    };
  },

  computed: {
    ...mapState('categories', {
      categoryTree: 'itemTree',
      categoryList: 'items'
    }),

    isFiltered: () => this.filteredChoices !== this.categoryTree,
    categoryTreeMaxDepth: () => this.isFiltered ? 0 : -1,
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

    keydown(event) {
      if (event.key === 'Escape') {
        event.preventDefault();
        this.close();
      }
      else if (event.key === 'Enter' || event.key === 'Tab') {
        event.preventDefault();
        this.selected(this.selectedCategory);
      }
      else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        event.preventDefault();
        const choiseList = this.isFiltered ? this.filteredChoices : this.categoryList;
        const choiceLength = choiseList.length;
        const direction = this.$data._selectDirection;
        if (event.key === 'ArrowUp') { this.$data._selectedIndex = this.$data._selectedIndex + direction; }
        else if (event.key === 'ArrowDown') { this.$data._selectedIndex = this.$data._selectedIndex - direction; }
        if (this.$data._selectedIndex >= choiceLength) { this.$data._selectedIndex = 0; }
        if (this.$data._selectedIndex < 0) { this.$data._selectedIndex = choiceLength; }
        this.selectedCategory = choiseList[this.$data._selectedIndex];
      }
    },

    selected(category) {
      this.$emit("itemSelected", category);
      this.showCategorySelector = false;
      this.categoryTitle = category.title;
      this.deferBlur = false;
      this.$emit("blur");
    },

    selectionChanged(category) {
      // TODO -> hover
    },

    inputChanged(event) {
      this.$data._requestUpdate = true;
      this.showCategorySelector = true;
    },
  },

  async created() {
    await this.$store.dispatch('categories/fetchAll');
    this.filteredChoices = this.categoryTree;
    // TODO: select selected automatically
    this.selectedCategory = this.categoryList[0];
  },

  async updated() {
    zebraify(this.$el);

    if (this.$data._requestUpdate) {
      this.$data._requestUpdate = false;
      if (this.categoryTitle === "") {
        this.filteredChoices = this.categoryTree;
        // this.isFiltered = false;
      } else {
        // This will yield children too
        this.filteredChoices = this.categoryList.filter(item => item != null && item.title.toLowerCase().startsWith(this.categoryTitle.toLowerCase()));
      }
    };
  },

  watch: {
    filteredChoices() {
    }
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
            vnode.context.$data._selectDirection = -1;
          } else {
            console.log('down', p);
            vnode.context.$data._selectDirection = 1;
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
