<template>
  <div>

    <h2>The stuff</h2>

    <div class="treeSelf">
      <vue-drag-tree
        :data="categories"
        :allowDrag="allowDrag"
        :allowDrop="allowDrop"
        :defaultText="'New Category'"
        @current-clicked="curNodeClicked"
        @drag="dragHandler"
        @drag-enter="dragEnterHandler"
        @drag-leave="dragLeaveHandler"
        @drag-over="dragOverHandler"
        @drag-end="dragEndHandler"
        @drop="dropHandler"
        :disableDBClick="false"
        expand-all
      ></vue-drag-tree>
    </div>

    <!-- CATEGORIES  -->
    <h2>(Legacy)</h2>
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
    <!-- /CATEGORIES -->

    <import-export />

  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import FileSaver from "file-saver";
import CategoryItem from "./category-item.vue"
import ImportExport from "./import-export.vue"
export default {
  components: {
    CategoryItem, ImportExport
  },

  data() {
    return {
      isAddingChild: false,
      newChild: "",
    }
  },

  computed: {
    ...mapState('categories', { categories: 'itemTree' }),

  },

  created() {
    this.$store.dispatch('categories/fetchAll');
  },

  methods: {
    ...mapActions('categories', {
      addCategory: 'addNew',
      removeCategory: 'remove',
      editCategory: 'edit'
    }),

    toggleSidebar() {
      this.toggleUI('showSidebar');
    },

    startAddChild() {
      this.isAddingChild = true;
      this.newChild = "";
    },

    doneAddChild() {
      if (!this.isAddingChild)
        return;
      // console.log({ parent: null, value: this.newChild });
      this.addCategory({ parent: null, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = "";
    },

    cancelAddChild() {
      this.isAddingChild = false;
      this.newChild = "";
    },

    // -- Tree editor

    allowDrag(model, component) {
      return true;
    },
    allowDrop(model, component) {
      return true;
    },
    curNodeClicked(model, component) {
      console.log("curNodeClicked", model, component);
    },
    dragHandler(model, component, e) {
      console.log("dragHandler: ", model, component, e);
    },
    dragEnterHandler(model, component, e) {
      console.log("dragEnterHandler: ", model, component, e);
    },
    dragLeaveHandler(model, component, e) {
      console.log("dragLeaveHandler: ", model, component, e);
    },
    dragOverHandler(model, component, e) {
      console.log("dragOverHandler: ", model, component, e);
    },
    dragEndHandler(model, component, e) {
      console.log("dragEndHandler: ", model, component, e);
    },
    dropHandler(model, component, e) {
      console.log("dropHandler: ", model, component, e);
    }

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
