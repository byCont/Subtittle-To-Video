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
        <div class="form-control-group-text">
          <label>Font Style:</label>
          <select v-model="selectedFont" class="form-control">
            <option
              class="option" 
              v-for="font in fontOptions" 
              :key="font.value" 
              :value="font.value"
              :style="{ fontFamily: font.value }"
            >
              {{ font.name }}
            </option>
          </select>
        </div>

        <div class="form-control-group-text">
          <label>Text Case:</label>
          <select v-model="selectedTextCase" class="form-control">            
            <option class="option" value="upper">AA</option>
            <option class="option" value="lower">Aa</option>
          </select>
        </div>

        <div class="form-control-group-text">
          <label>Text Size:</label>
          <select v-model="fontSize" class="form-control">
            <option value="25">25</option>
            <option value="30">30</option>
            <option value="90">90</option>
            <option value="95">95</option>
            <option value="110">110</option>
            <option value="120">120</option>
            <option value="130">130</option>
          </select>
        </div>

        <div class="form-control-group-text">
          <label>Background:</label>
          <input type="color" v-model="selectedColor" class="form-control">
        </div>

        <div class="form-buttons">
          <button class="btn btn-success" @click="handleGenerate">Generate Video</button>
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
      fontSize: 95,
      selectedTextCase: 'lower',
      fontOptions: [
        { name: 'Product Sans', value: 'Product Sans' }, // Fuente original
        { name: 'Product Sans Bold', value: 'Product Sans Bold' }, 
        { name: 'Arial', value: 'Arial' },
        { name: 'Poppins Regular', value: 'Poppins Regular' },
        { name: 'Poppins Bold', value: 'Poppins Bold'},
        { name: 'Poppins Italic', value: 'Poppins Italic'},
        { name: 'Impact', value: 'Impact' },
        { name: 'Times New Roman', value: 'Times New Roman' },
        { name: 'Verdana', value: 'Verdana' },
        { name: 'Comic Sans MS', value: 'Comic Sans MS' },
        { name: 'Dancing Script Regular', value: 'Dancing Script Regular' },
        { name: 'Barriecito', value: 'Barriecito Regular'},
        { name:  'Fauna One', value: 'Fauna One Regular'},
        { name: 'Gread Vibes', value: 'Great Vibes Regular'},
        { name: 'Lobster', value: 'Lobster Regular'},
        { name: 'Permanent Marker',value: 'Permanent Marker Regular'},
        { name: 'Satisfy', value: 'Satisfy Regular'},
        { name: 'Alfa Slab One Regular', value: 'Alfa Slab One Regular' }, 
        { name: 'Slabo', value: 'Slab 27px' }, 
        { name: 'Special Elite Regular', value: 'Special Elite Regular'}
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
      this.$emit('files-selected', files);
    },
    handleAudioSelect(event) {
      this.$emit('audio-selected', event.target.files[0]);
    },
    handleGenerate() {
      if (this.fontSize < 10 || this.fontSize > 201) {
        alert("Tamaño de texto debe ser entre 10 y 200");
        return;
      }

      const hexToFFmpegColor = (hex, alpha = 1) => {
        let r = hex.slice(1, 3);
        let g = hex.slice(3, 5);
        let b = hex.slice(5, 7);
        let a = Math.round(alpha * 255).toString(16).padStart(2, '0'); // Convertir alfa (0-1) a 00-FF
        return `#${r}${g}${b}${a}`;
      };

      this.$emit('generate-video', {
        font: this.selectedFont,
        fontSize: this.fontSize,
        textCase: this.selectedTextCase,
        textColor: hexToFFmpegColor(this.selectedColor, 0.8) // Alfa a 50%
      });
    }
  }
};
</script>
