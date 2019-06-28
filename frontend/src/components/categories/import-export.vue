<template>
  <section>
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
  </section>
</template>

<script>
import { mapState, mapActions, mapMutations, mapGetters } from "vuex";
import FileSaver from 'file-saver';

export default {
  data() {
    return {
      progress: '',
      importProgress: '',
      importedFile: null,
    };
  },

  computed: {
    // --- import-export ---
    ...mapState('categoriesImportExport', ['isExporting', 'isImporting', 'exportedData']),
    ...mapGetters('categoriesImportExport', ['exportFilename', 'importError', 'importCount'])
    // --- /import-export ---
  },

  methods: {
    ...mapActions('categoriesImportExport', ['doExport', 'setProperty', 'doImport', 'parseFile', 'hideUi']),
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
  }
}
</script>

<style>
</style>
