// frontend/src/components/VideoUpload.vue

<template>
  <div class="col-lg-3 video-upload-container">
    <div class="form-group">
     
      <div class="form-control-group">
        <label for="subtitleinput">Add Subtitles:</label>
        <input type="file" id="subtitleinput" accept=".srt,.ass, .lrc" @change="handleFileSelect" />
      </div>

      <div class="form-control-group">
        <label for="audioinput">Add Audio:</label>
        <input 
          type="file" 
          id="audioinput" 
          accept="audio/*" 
          @change="handleAudioSelect"
          />
      </div>

      <!-- Nuevos campos para fuente y tamaño -->
      <div class="form-control-group">
        <label>Font Style:</label>
        <select v-model="selectedFont" class="form-control">
          <option v-for="font in fontOptions" :key="font.value" :value="font.value">
            {{ font.name }}
          </option>
        </select>
      </div>

      <div class="form-control-group">
        <label>Text Size:</label>
        <input type="number" v-model="fontSize" class="form-control" min="10" max="100" />
      </div>
      <div class="form-buttons">
        <button class="btn btn-primary" @click="handleGenerate">Generate Video</button>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="progress-container" v-if="uploadProgress > 0">
      <div class="progress">
        <div
          id="uploadprogress"
          class="progress-bar"
          role="progressbar"
          :aria-valuenow="uploadProgress"
          aria-valuemin="0"
          aria-valuemax="100"
          :style="{ width: uploadProgress + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
  import '../App.css';
  export default {
    name: 'VideoUpload',
    props: {
      uploadProgress: Number,
    },
    data() {
      return {
        selectedFont: 'Product Sans',
        fontSize: 40,
        fontOptions: [
          { name: 'Product Sans', value: 'Product Sans' }, // Fuente original
          { name: 'Arial', value: 'Arial' },
          { name: 'Poppins Regular', value: 'Poppins Regular' },
          { name: 'Georgia', value: 'Georgia' },
          { name: 'Helvetica', value: 'Helvetica' },
          { name: 'Impact', value: 'Impact' },
          { name: 'Palatino', value: 'Palatino' },
          { name: 'Times New Roman', value: 'Times New Roman' },
          { name: 'Verdana', value: 'Verdana' },
          { name: 'Courier New', value: 'Courier New' },
          {name: 'Comic Sans MS', value: 'Comic Sans MS'},
          {name: 'Dancing Script', value: 'Dancing Script Regular'}
          
        ]
      };
    },
    methods: {
      handleDrop(event) {
        const files = event.dataTransfer.files;
        this.processFiles(files);
      },
      handleFileSelect(event) {
        const files = event.target.files;
        this.processFiles(files);
      },
      processFiles(files) {
        // Emit files to the parent component for further handling
        this.$emit('files-selected', files);
      },
      handleAudioSelect(event) {
        this.$emit('audio-selected', event.target.files[0]);
      },
      handleGenerate() {
        // Validar tamaño mínimo/máximo
        if (this.fontSize < 10 || this.fontSize > 100) {
          alert("Tamaño de texto debe ser entre 10 y 100");
          return;
        }
        
        this.$emit('generate-video', {
          font: this.selectedFont,
          fontSize: this.fontSize
        });
      }
    }
  };
</script>