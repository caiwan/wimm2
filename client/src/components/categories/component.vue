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
    <!-- ! import-export -  -->
    <h1>
      Import
    </h1>
    <div>
      <form @submit.prevent="doImportWrapped">
        <div>
          <input
            type="file"
            @change="setImportedFile($event.target.files[0])"
          >
        </div>
        <button :disabled="!importedFile || isImporting">
          Import JSON
          <span v-if="isImporting">{{ importProgress }} </span>
        </button>
        <div v-if="importError">
          Import failed for some with this reason:
          <pre>{{ importError }}</pre>
        </div>
        <div v-if="importCount">
          Imported {{ importCount }} items
        </div>
      </form>
    </div>
    <!--  -->
    <h1>
      Export
    </h1>
    <div>
      <form @submit.prevent="doExportWrapped">
        <button :disabled="isExporting">
          Export categories as JSON
          <span v-if="isExporting">{{ progress }}</span>
        </button>
      </form>
    </div>

    <!-- /import-export -  -->

  </div>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import FileSaver from 'file-saver';
import CategoryItem from './category-item.vue'
export default {
  components: {
    CategoryItem
  },

  data() {
    return {
      isAddingChild: false,
      newChild: '',
      // --- import-export --- 
      progress: '',
      importProgress: '',
      importedFile: null,
      // --- /import-export --- 

    }
  },

  computed: {
    ...mapState("categories", { categories: "itemTree" }),
    // --- import-export --- 
    ...mapState('categoriesImportExport', ['isExporting', 'isImporting', 'exportedData']),
    ...mapGetters('categoriesImportExport', ['exportFilename', 'importError', 'importCount'])
    // --- /import-export --- 
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

    // --- import-export --- 
    ...mapActions('categoriesImportExport', ['doExport', 'setProperty', 'doImport', 'parseFile', 'hideUi']),
    // --- /import-export --- 

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
      // console.log({ parent: null, value: this.newChild });
      this.addCategory({ parent: null, value: this.newChild });
      this.isAddingChild = false;
      this.newChild = '';
    },

    cancelAddChild() {
      this.isAddingChild = false;
      this.newChild = '';
    },

    // --- import-export --- 

    async doImportWrapped() {
      const progress = () => {
        setTimeout(() => {
          if (this.isImporting) {
            const dots = (this.importProgress.length + 1) % 4;

            this.importProgress = '.'.repeat(dots);
            setTimeout(progress, 400);
          }
          else {
            this.importProgress = '';
          }
        })
      };

      progress();
      await this.doImport(this.importedFile);
      await this.$store.dispatch("categories/fetchAll");

    },

    async doExportWrapped() {
      const progress = () => {
        setTimeout(() => {
          if (this.isImporting) {
            const dots = (this.importProgress.length + 1) % 4;

            this.importProgress = '.'.repeat(dots);
            setTimeout(progress, 400);
          }
          else {
            this.importProgress = '';
          }
        })
      }

      progress();

      await this.doExport();
      const blob = new Blob(this.exportedData, { type: 'application/octet-stream' });
      FileSaver.saveAs(blob, this.exportFilename);
    },


    setImportedFile(file) {
      this.importedFile = file;
    }
    // --- /import-export --- 

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
