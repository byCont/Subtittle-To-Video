// frontend/src/components/VideoUpload.vue

<template>
    <div class="col-lg-3 video-upload-container">
      <div class="form-group d-flex align-items-center justify-content-start gap-3">
             
        <div class="form-control-group">
          <label class="d-flex align-items-center justify-content-start gap-2" for="audioinput"><div v-html="icons.fileAudio"></div>Add Audio:</label>
          <input 
            type="file" 
            id="audioinput" 
            accept="audio/*" 
            @change="handleAudioSelect"
          />
        </div>

        <div class="form-control-group">
          <label class="d-flex align-items-center justify-content-start gap-2" for="subtitleinput"><div v-html="icons.addSubt"></div>Add Subtitles:</label>
          <div class="subtitle-input-container">
            <input type="file" id="subtitleinput" accept=".srt,.ass,.lrc" @change="handleFileSelect" />
            <!-- Botón para editar subtítulos -->
            <button v-if="subtitlesContent" class="btn btn-edit-small d-flex align-items-center justify-content-start gap-2" @click="openSubtitleEditor"><div v-html="icons.editIcon"></div>Edit</button>
          </div>
        </div>
        <!-- Modal para editar subtítulos -->
        <SubtitleEditorModal
          :subtitles="subtitlesContent"
          :showModal="showSubtitleEditor"
          @save-changes="saveEditedSubtitles"
          @close-modal="closeSubtitleEditor"
        />

        <div class="form-control-group">
          <label class="d-flex align-items-center justify-content-start gap-2" for="imageinput"><div v-html="icons.addImage"></div>Add Image:</label>
          <input 
            type="file" 
            id="imageinput" 
            accept="image/*"
            @change="handleImageSelect"
          />
        </div>

      <!-- Nuevos campos para fuente y tamaño -->
        <div class="form-control-group-text">
          <label class="d-flex align-items-center justify-content-start gap-1"><div v-html="icons.styleIcon"></div>Font Style:</label>
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
          <label class="d-flex align-items-center justify-content-start gap-1"><div v-html="icons.caseIcon"></div>Text Case:</label>
          <select v-model="selectedTextCase" class="form-control">            
            <option class="option" value="upper">AA</option>
            <option class="option" value="capitalize">Aa</option>
          </select>
        </div>

        <div class="form-control-group-text">
          <label class="d-flex align-items-center justify-content-start gap-1"><div v-html="icons.fontColorIcon"></div>Text Color:</label>
          <select v-model="selectedTextColor" class="form-control">            
            <option class="option" value="light">Light</option>
            <option class="option" value="dark">Dark</option>
          </select>
        </div>

        <div class="form-control-group-text">
          <label class="d-flex align-items-center justify-content-start gap-1"><div v-html="icons.fontIcon"></div>Text Size:</label>
          <select v-model="fontSize" class="form-control">
            <option value="25">25</option>
            <option value="30">30</option>
            <option value="90">90</option>
            <option value="95">95</option>
            <option value="110">110</option>
            <option value="120">120</option>
            <option value="130">130</option>
            <option value="130">150</option>            
            <option value="130">165</option>
          </select>
        </div>

        <!-- Cambiar el input a tipo text para permitir vacío -->
        <div class="form-control-group-text">
          <label class="d-flex align-items-center justify-content-start gap-1"> <div v-html="icons.colorIcon"></div>Background:</label>
          <div class="d-flex gap-2">
            <input 
            type="color" 
            v-model="selectedColor" 
            class="form-control"
            :style="{ backgroundColor: selectedColor || 'transparent' }"
          >
          <input 
            type="checkbox" 
            v-model="enableBackgroundColor" 
            class="form-checkbox"
          >Enable</div>
          
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
  import {icons} from '../assets/icons.js';
  import SubtitleEditorModal from './SubtitleEditorModal.vue';

  export default {
    name: 'VideoUpload',
    components: {
      SubtitleEditorModal,
    },
    props: {
      uploadProgress: Number,
    },
    data() {
      return {
        selectedFont: 'Product Sans Bold',
        fontSize: 95,
        selectedTextCase: 'capitalize',
        selectedTextColor: 'light',
        selectedColor: '#d6d6d6cc',  // Valor por defecto (gris translúcido)
        enableBackgroundColor: false,
        subtitlesContent: '',
        icons,
        showSubtitleEditor: false,
        fontOptions: [
          { name: 'Product Sans Bold', value: 'Product Sans Bold' }, // default font
          { name: 'Arial', value: 'Arial' },
          { name: 'Poppins Regular', value: 'Poppins Regular' },
          { name: 'Poppins Bold', value: 'Poppins Bold'},
          { name: 'Impact', value: 'Impact' },
          { name: 'Times New Roman', value: 'Times New Roman' },
          { name: 'Verdana', value: 'Verdana' },
          { name: 'Comic Sans MS', value: 'Comic Sans MS' },
          { name: 'Dancing Script Regular', value: 'Dancing Script Regular' },
          { name: 'Barrio Upper', value: 'Barrio Regular' },
          { name: 'Barriecito', value: 'Barriecito Regular'},          
          { name: 'Gread Vibes', value: 'Great Vibes Regular'},
          { name: 'Lobster', value: 'Lobster Regular'},
          { name: 'Permanent Marker',value: 'Permanent Marker Regular'},
          { name: 'Satisfy', value: 'Satisfy Regular'},
          { name: 'Alfa Slab One Regular', value: 'Alfa Slab One Regular' }, 
          { name: 'Special Elite Regular', value: 'Special Elite Regular'},
          { name: 'Bebas Neue', value: 'Bebas Neue Regular'},
          { name: 'Sancreek', value: 'Sancreek Regular'},
          { name: 'Garrison BOLD', value: 'Garrison ExtraBold Sans BOLD'},
          { name: 'Akira', value: 'AkiraExpanded-SuperBold'}

        ]
      };
    },
    methods: {
      handleDrop(event) {
        const files = event.dataTransfer.files;
        this.processFiles(files);
      },
      handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.subtitlesContent = e.target.result; // Guardar contenido del archivo
            // No abrir el modal automáticamente
          };
          reader.readAsText(file);
        }
      }, 
      openSubtitleEditor() {
        this.showSubtitleEditor = true; // Abrir el modal manualmente
      },  
      processFiles(files) {
        // Pasar los subtítulos editados junto con otros archivos
        this.$emit('files-selected', { subtitles: this.subtitlesContent, files });
      },
      handleAudioSelect(event) {
        this.$emit('audio-selected', event.target.files[0]);
      },
      handleImageSelect(event) {
        this.$emit('image-selected', event.target.files[0]);
      },
      saveEditedSubtitles(editedContent) {
        this.subtitlesContent = editedContent; // Guardar cambios realizados
        this.closeSubtitleEditor(); // Cerrar el modal
      },
      closeSubtitleEditor() {
        this.showSubtitleEditor = false; // Ocultar el modal
      },

      handleGenerate() {
        if (!this.subtitlesContent) {
          alert("Debes cargar o editar los subtítulos primero");
          return;
        }

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
          textColor: this.selectedTextColor,
          bgColor: hexToFFmpegColor(this.selectedColor, 0.7),
          enableBackgroundColor: this.enableBackgroundColor,
          subtitles: this.subtitlesContent // Añadir los subtítulos al payload
        });
      }
    }
  };
</script>
