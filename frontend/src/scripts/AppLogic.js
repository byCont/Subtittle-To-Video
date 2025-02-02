// src/scripts/AppLogic.js

import axios from 'axios';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import '../App.css';
const apiBaseUrl = "http://localhost:5000";

export default {
  data() {
    return {
      loading: false,
      videoToRender: null,
      uploadprogress: 0,
    };
  },
  methods: {
    
    generateVideo(params) {
      this.loading = true;
      const audioFile = document.getElementById("audioinput").files[0];
      const imageFile = document.getElementById("imageinput").files[0];
    
      // Validación CORREGIDA (usar params.subtitles en lugar de params.subtitleFile)
      if (!audioFile || !params.subtitles) {
        this.loading = false;
        return toast.warning("¡Se requieren el archivo de audio y los subtítulos editados!");
      }
    
      const data = new FormData();
      data.append("audiofile", audioFile);
      
      // Crear Blob con el contenido editado CORRECTO
      const subtitleBlob = new Blob([params.subtitles], { type: 'text/plain' });
      data.append("subtitlefile", subtitleBlob, 'subtitles.lrc'); // Nombre requerido por el backend
    
      if (imageFile) data.append("imagefile", imageFile);
      
      data.append("font_name", params.font);
      data.append("font_size", params.fontSize);
      data.append("text_case", params.textCase);
      
      if (params.enableBackgroundColor && params.textColor) {
        data.append("text_color", params.textColor);
      }
    
      axios.post(`${apiBaseUrl}/generate_video`, data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(res => {
        if (res.data.status === "success") {
            toast.success("Video generated!");
          this.videoToRender = res.data.generated_videopath;
        } else {
            toast.error(`Error generating video: ${res.data.message}`);
        }
        this.loading = false;
      })         
      .catch((error) => {
        toast.error("Error de conexión con el servidor");
        console.error('Detalles del error:', error);
        this.loading = false;
      });    
    }
  },
};
