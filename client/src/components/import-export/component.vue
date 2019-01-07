<template>
  <div id="import-export">
    <div class="content">

      <!-- Items - Will be moved to an ext. component -->
      <h1>Items</h1>

      <!-- Export  -->
      <h2>Export</h2>
      <form @submit.prevent="doExportWrapped">
        <calendar
          :dateFrom="dateFrom"
          :dateTo="dateTo"
          @change="onChanged"
        ></calendar>
        <button :disabled="isExporting">
          Export as CSV
          <span v-if="isExporting">{{ progress }}</span>
        </button>
      </form>
      <!-- /Export  -->

      <!-- Import  -->
      <h2>Import</h2>
      <p>Only CSV files are supported. Example of the required structure:</p>
      <pre>date,price,tags<br>2017-08-11,-1200,"food,junk,chips,doritos"</pre>
      <!-- --- -->
      <form @submit.prevent="doImportWrapped">
        <div>
          <input
            type="file"
            @change="setImportedFile($event.target.files[0])"
          >
        </div>
        <button :disabled="!importedFile || isImporting">
          Import CSV
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
      <!-- /Import  -->
      <!-- /Items -->

      <!-- Categories - Will be moved to an ext. component -->
      <h1>Categories</h1>
      <h2>Import</h2>
      <p>TBD</p>
      <h2>Export</h2>
      <p>TBD</p>
      <!-- /Categories -->
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import FileSaver from 'file-saver';

import Calendar from '@/components/calendar';

export default {
  components: {
    Calendar
  },
  data() {
    return {
      progress: '',
      importProgress: '',
      importedFile: null,
    }
  },
  computed: {
    ...mapState('importExport', ['isExporting', 'isImporting', 'dateFrom', 'dateTo', 'exportedData']),
    ...mapGetters('importExport', ['exportFilename', 'importError', 'importCount'])
  },
  methods: {
    ...mapActions('importExport', ['doExport', 'setProperty', 'doImport', 'parseFile', 'hideUi']),
    onChanged(key, value) {
      this.setProperty({ key, value });
    },
    setImportedFile(f) {
      this.importedFile = f;
    },
    async doExportWrapped(e) {
      const progress = () => {
        setTimeout(() => {
          if (this.isExporting) {
            const dots = (this.progress.length + 1) % 4;

            this.progress = '.'.repeat(dots);
            setTimeout(progress, 400);
          }
          else {
            this.progress = '';
          }
        })
      };

      progress();

      await this.doExport();
      const blob = new Blob(this.exportedData, { type: 'application/octet-stream' });
      FileSaver.saveAs(blob, this.exportFilename);
    },
    doImportWrapped(e) {
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
      this.doImport(this.importedFile);
    }
  },
  beforeRouteLeave(to, from, next) {
    this.hideUi();
    next();
  },
}
</script>

<style lang="scss" rel="stylesheet/scss">
@import "../../scss/consts";

#import-export {
  // height: 100%;

  pre {
    border: $input-border;
    padding: 6px;
    background: $bg-ui;
    font-size: smaller;
  }
}
</style>
