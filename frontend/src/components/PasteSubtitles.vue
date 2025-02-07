// frontend/src/components/PasteSubtitles.vue

<template>
  <div>
    <!-- Button trigger modal -->
    <button type="button" title="Paste Subtitles" class="custom-btn" @click="showModal = true">
      <div v-html="icons.pasteIcon"></div></button>

    <!-- Modal -->
    <div class="modal fade" :class="{ show: showModal }" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" style="display: block;" v-if="showModal">
      <div class="modal-dialog">
        <div class="modal-content">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Paste Subtitles</h1>            
          <div class="modal-body">
            <textarea v-model="subtitles" rows="10" placeholder="Paste subtitles here..."></textarea>
          </div>
          <div class="d-flex align-items-center justify-content-end p-3 gap-3">
            <button type="button" class="btn btn-primary" @click="saveSubtitles">Guardar cambios</button>
            <button type="button" class="btn btn-danger" @click="showModal = false">Cerrar</button>
          </div>
            
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {icons} from '../assets/icons.js';
export default {
  name: 'PasteSubtitles',
  data() {
    return {
      showModal: false,
      subtitles: '',
      icons
    };
  },
  methods: {
    saveSubtitles() {
      if (!this.subtitles.trim()) {
        alert("Please enter subtitles content");
        return;
      }
      const blob = new Blob([this.subtitles], { type: 'text/plain' });
      const file = new File([blob], 'pasted-subtitles.lrc', { type: 'text/plain' });
      this.$emit('subtitles-pasted', file);
      this.showModal = false;
      this.subtitles = ''; // Limpiar el área de texto
    }
  }
};
</script>

<style scoped>
</style>