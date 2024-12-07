<template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div class="w-full max-w-2xl bg-white rounded-lg shadow-xl overflow-hidden">
        <div class="p-8">
          <h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">File Upload</h1>
          
          <div 
            class="border-dashed border-2 border-gray-300 rounded-lg p-8 text-center cursor-pointer transition-colors duration-300 ease-in-out"
            :class="{ 'border-blue-500 bg-blue-50': isDragging }"
            @dragenter.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @dragover.prevent
            @drop.prevent="handleDrop"
            @click="$refs.fileInput.click()"
          >
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileInput" 
              multiple 
              class="hidden" 
            />
            <UploadCloudIcon class="w-16 h-16 mx-auto mb-4 text-gray-400" />
            <p class="text-lg text-gray-600 mb-2">
              Drag and drop your files here, or click to select files
            </p>
            <p class="text-sm text-gray-500">
              Supports multiple file uploads
            </p>
          </div>
  
          <div v-if="files.length > 0" class="mt-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Selected Files:</h2>
            <ul class="space-y-3">
              <li 
                v-for="(file, index) in files" 
                :key="index"
                class="flex items-center justify-between bg-gray-50 rounded-lg p-4 transition-colors duration-300 ease-in-out hover:bg-gray-100"
              >
                <div class="flex items-center">
                  <FileIcon class="w-6 h-6 text-blue-500 mr-3" />
                  <span class="text-gray-800 font-medium">{{ file.name }}</span>
                </div>
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 mr-4">{{ formatFileSize(file.size) }}</span>
                  <button 
                    @click="removeFile(index)" 
                    class="text-red-500 hover:text-red-700 focus:outline-none"
                  >
                    <XIcon class="w-5 h-5" />
                  </button>
                </div>
              </li>
            </ul>
          </div>
  
          <div class="mt-8 flex justify-end">
            <button 
              @click="uploadFiles" 
              class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-300 ease-in-out"
              :disabled="files.length === 0 || isUploading"
              :class="{ 'opacity-50 cursor-not-allowed': files.length === 0 || isUploading }"
            >
              {{ isUploading ? 'Uploading...' : 'Upload Files' }}
            </button>
          </div>
  
          <div v-if="downloadUrl" class="mt-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Download Link:</h2>
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
              <p class="font-bold">Success!</p>
              <p class="block sm:inline">Your files have been uploaded and zipped.</p>
              <p class="mt-2">
                <a :href="downloadUrl" target="_blank" class="text-blue-500 hover:underline">Click here to view the download page</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { UploadCloudIcon, FileIcon, XIcon } from 'lucide-vue-next'
  import axios from 'axios'
  
  export default {
    name: 'MultiFileUpload',
    components: {
      UploadCloudIcon,
      FileIcon,
      XIcon
    },
    data() {
      return {
        files: [],
        isDragging: false,
        isUploading: false,
        downloadUrl: null
      }
    },
    methods: {
      handleDrop(e) {
        this.isDragging = false
        const droppedFiles = Array.from(e.dataTransfer.files)
        this.addFiles(droppedFiles)
      },
      handleFileInput(e) {
        const selectedFiles = Array.from(e.target.files)
        this.addFiles(selectedFiles)
      },
      addFiles(newFiles) {
        const updatedFiles = [...this.files]
        newFiles.forEach(file => {
          if (!this.files.some(f => f.name === file.name)) {
            updatedFiles.push(file)
          }
        })
        this.files = updatedFiles
      },
      removeFile(index) {
        this.files.splice(index, 1)
      },
      formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
      },
      async uploadFiles() {
        if (this.files.length === 0) return
  
        this.isUploading = true
        const formData = new FormData()
        this.files.forEach((file, index) => {
          formData.append(`file${index}`, file)
        })
  
        try {
          const response = await axios.post('http://localhost:8000/api/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          this.downloadUrl = response.data.download_url
        } catch (error) {
          console.error('Error uploading files:', error)
          // Handle error (e.g., show an error message to the user)
        } finally {
          this.isUploading = false
        }
      }
    }
  }
  </script>