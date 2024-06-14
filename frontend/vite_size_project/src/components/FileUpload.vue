<template>
  <div>
    <input type="file" @change="onFileChange" />
    <button @click="uploadFile">Upload</button>
    <div v-if="uploadSuccess">File uploaded successfully!</div>
    <div v-if="uploadError">{{ uploadError }}</div>

    <div v-if="processedFileUrl">
      <button @click="downloadFile">Download Processed File</button>
    </div>
    <div v-if="downloadError">{{ downloadError }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      uploadSuccess: false,
      uploadError: '',
      processedFileUrl: '',
      downloadError: ''
    };
  },
  methods: {
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        this.uploadError = "No file selected.";
        return;
      }
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
          method: 'POST',
          body: formData
        });
        if (response.ok) {
          const data = await response.json();
          this.uploadSuccess = true;
          this.uploadError = '';
          this.processedFileUrl = `http://127.0.0.1:8000${data.processed_file_url}`;
          console.log(data);
        } else {
          const errorData = await response.json();
          this.uploadError = errorData.detail || 'Upload failed';
        }
      } catch (error) {
        this.uploadError = error.message || 'Upload failed';
      }
    },
    async downloadFile() {
      try {
        const response = await fetch(this.processedFileUrl);
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = this.processedFileUrl.split('/').pop();  // 从 URL 中提取文件名
          document.body.appendChild(a);
          a.click();
          a.remove();
          this.downloadError = '';
        } else {
          const errorData = await response.json();
          this.downloadError = errorData.detail || 'Download failed';
        }
      } catch (error) {
        this.downloadError = error.message || 'Download failed';
      }
    }
  }
};
</script>

<style scoped>
div {
  margin: 20px;
}
button {
  margin-top: 10px;
}
input {
  margin-top: 10px;
}
</style>