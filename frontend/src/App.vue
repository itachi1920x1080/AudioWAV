<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const statusMessage = ref('')
const isConverting = ref(false)

// ១. ពេលអ្នកប្រើប្រាស់រើសឯកសារ
function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    statusMessage.value = `ត្រៀមបម្លែង៖ ${file.name}`
  }
}

// ២. ពេលអ្នកប្រើប្រាស់ចុចប៊ូតុង "បម្លែងទៅជា WAV"
async function uploadForConversion() {
  if (!selectedFile.value) return
  
  isConverting.value = true
  statusMessage.value = 'កំពុងបញ្ជូន និងបម្លែងឯកសារ... ⏳'
  
  const formData = new FormData()
  formData.append('audio', selectedFile.value)

  try {
    // ភ្ជាប់ទៅកាន់ FastAPI ដែលកំពុង Run លើ Port 8000
    const response = await fetch('http://localhost:8000/convert', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error("មានបញ្ហានៅលើ Server")

    // ៣. ទទួលបានឯកសារ WAV ត្រឡប់មកវិញ
    const blob = await response.blob()
    
    // ៤. បង្កើតតំណទាញយក (Download Link) ដោយស្វ័យប្រវត្តិ
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    
    const oldName = selectedFile.value.name
    const newName = oldName.substring(0, oldName.lastIndexOf('.')) + '.wav'
    link.download = newName
    
    document.body.appendChild(link)
    link.click()
    link.remove()

    statusMessage.value = '✅ ការបម្លែងជោគជ័យ! ឯកសារកំពុងទាញយក...'
  } catch (error) {
    statusMessage.value = '❌ មានបញ្ហា! តើអ្នកបាន Run API Python (uvicorn) ហើយឬនៅ?'
    console.error(error)
  } finally {
    isConverting.value = false
  }
}
</script>

<template>
  <main class="converter-box">
    <div class="brand-mark" aria-hidden="true">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 60" width="220">
        <rect x="10" y="20" width="6" height="20" rx="3" fill="#94a3b8">
          <animate attributeName="height" values="20;40;20" dur="1s" repeatCount="indefinite" />
          <animate attributeName="y" values="20;10;20" dur="1s" repeatCount="indefinite" />
        </rect>
        <rect x="20" y="10" width="6" height="40" rx="3" fill="#94a3b8">
          <animate attributeName="height" values="40;20;40" dur="1.2s" repeatCount="indefinite" />
          <animate attributeName="y" values="10;20;10" dur="1.2s" repeatCount="indefinite" />
        </rect>

        <path d="M 35 30 L 42 24 L 42 28 L 50 28 L 50 32 L 42 32 L 42 36 Z" fill="#cbd5e1" />

        <rect x="58" y="10" width="6" height="40" rx="3" fill="#42b883">
          <animate attributeName="height" values="40;15;40" dur="0.9s" repeatCount="indefinite" />
          <animate attributeName="y" values="10;22.5;10" dur="0.9s" repeatCount="indefinite" />
        </rect>
        <rect x="68" y="20" width="6" height="20" rx="3" fill="#42b883">
          <animate attributeName="height" values="20;35;20" dur="1.1s" repeatCount="indefinite" />
          <animate attributeName="y" values="20;12.5;20" dur="1.1s" repeatCount="indefinite" />
        </rect>

        <text x="88" y="40" font-family="'Segoe UI', Tahoma, sans-serif" font-size="26" font-weight="900" fill="#2c3e50">
          Audio<tspan fill="#42b883">WAV</tspan>
        </text>
      </svg>
    </div>
    <h1>កម្មវិធីបម្លែងសំឡេង</h1>
    <p class="subtitle">បម្លែង MP3, OGG, M4A ទៅជាទម្រង់ WAV គុណភាពខ្ពស់</p>
    
    <div class="upload-section">
      <input 
        type="file" 
        accept="audio/*" 
        @change="handleFileUpload"
        class="file-input"
      >
      <button 
        :disabled="!selectedFile || isConverting" 
        @click="uploadForConversion"
        class="convert-btn"
      >
        {{ isConverting ? 'កំពុងបម្លែង...' : 'បម្លែងទៅជា WAV' }}
      </button>
    </div>

    <p :class="['status', { 'success': statusMessage.includes('ជោគជ័យ'), 'error': statusMessage.includes('បញ្ហា') }]">
      {{ statusMessage }}
    </p>
  </main>
</template>

<style scoped>
.converter-box {
  max-width: 520px;
  margin: 72px auto;
  padding: 36px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.96));
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 20px;
  box-shadow: 0 24px 70px rgba(15, 23, 42, 0.12);
}

.brand-mark {
  margin-bottom: 12px;
}

.brand-mark svg {
  max-width: 100%;
  height: auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 5px;
  font-size: 2rem;
}

.subtitle {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 28px;
}

.upload-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.file-input {
  padding: 12px;
  border: 1.5px dashed #cbd5e1;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.92);
  cursor: pointer;
}

.convert-btn {
  padding: 13px 16px;
  background-color: #42b883;
  color: white;
  font-size: 1.1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.convert-btn:hover:not(:disabled) {
  background-color: #33a06f;
}

.convert-btn:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.status {
  margin-top: 20px;
  font-weight: bold;
  color: #475569;
}

.success { color: #10b981; }
.error { color: #ef4444; }
</style>