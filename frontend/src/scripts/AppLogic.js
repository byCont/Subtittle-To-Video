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
    
    generateVideo(params) {  // <- Recibir el objeto params
      this.loading= true;
      const audioFile = document.getElementById("audioinput").files[0];
      const subtitleFile = document.getElementById("subtitleinput").files[0];
    
      if (!audioFile || !subtitleFile) {
        this.loading= false;
        return toast.warning("Audio and subtitle files are required!");
      }
    
      const data = new FormData();
      data.append("audiofile", audioFile);
      data.append("subtitlefile", subtitleFile);
      // Añadir nuevos parámetros al FormData
      data.append("font_name", params.font);
      data.append("font_size", params.fontSize);
      data.append("text_case", params.textCase);
    
      axios.post(`${apiBaseUrl}/generate_video`, data)
        .then(res => {
          if (res.data.status === "success") {
            toast.success("Video generated!");
            this.videoToRender = res.data.generated_videopath;
          } else {
            toast.error(`Error generating video: ${res.data.message}`);
          }
          this.loading= false;
        })         
        .catch(() => {
          toast.error("Error connecting to the server.");
          this.loading= false;
        });    
    }
  },
};
