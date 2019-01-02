<template>
  <div>
    <ul class="tree list-group">
      <category-item
        v-for="(category, index) in categories"
        :key="index"
        class="item list-group-item"
        :model="category"
        :maxDepth="0"
        v-on:itemAdded="addCategory"
        v-on:itemEdited="editCategory"
      />
      <li class="item list-group-item">
        <span
          class="add"
          v-if="!isAddingChild"
          @click="startAddChild"
        >
          <i class="fa fa-folder-plus"></i> Add new
        </span>

        <input
          autofocus
          autocomplete="off"
          placeholder="Category"
          class="add form-control"
          v-if="isAddingChild"
          v-model="newChild"
          v-focus="isAddingChild"
          @blur="doneAddChild"
          @keyup.enter="doneAddChild"
          @keyup.esc="cancelAddChild"
        />
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import CategoryItem from './category-item.vue'
export default {
  components: {
    CategoryItem
  },

  data() {
    return {
      isAddingChild: false,
      newChild: ''
    }
  },

  computed: {
    ...mapState("categories", { categories: "itemTree" }),
  },

  created() {
    this.$store.dispatch("categories/fetchAll");
  },

  methods: {
    ...mapActions("categories", {
      addCategory: 'addNew',
      removeCategory: 'remove',
      editCategory: 'edit'
    }),

    toggleSidebar() {
      this.toggleUI('showSidebar');
    },

    startAddChild() {
      this.isAddingChild = true;
      this.newChild = '';
    },

    doneAddChild() {
      if (!this.isAddingChild)
        return;
      console.log({ parent: null, value: this.newChild });
      this.addCategory({ parent: null, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },

    cancelAddChild() {
      this.isAddingChild = false;
      this.newChild = '';
    },
  },

  directives: {
    focus: function (el, binding) {
      if (binding.value) {
        el.focus();
      }
    }
  }

}
</script>

<style>
</style>
