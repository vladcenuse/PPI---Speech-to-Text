export const appConfig = {
  app: {
    name: 'Speech-to-Text Medical System',
    version: '1.0.0',
    description: 'Automate patient file creation with intelligent speech recognition',
    author: 'Vladutz Simion, Buhaitu Andrei, Chisu Grasu',
  },

  api: {
    baseUrl: process.env.NODE_ENV === 'production' 
      ? 'https://your-production-api.com' 
      : 'http://127.0.0.1:8000',
    timeout: 30000,
    endpoints: {
      patients: '/api/patients',
      recordings: '/api/recordings',
      transcriptions: '/api/transcriptions',
      exports: '/api/exports'
    }
  },

  recording: {
    maxDuration: 300000,
    audioFormat: 'audio/webm;codecs=opus' ,
    sampleRate: 44100,
    channels: 1,
    bitRate: 128000
  },

  speechToText: {
    language: 'ro-RO',
    maxAlternatives: 1,
    confidenceThreshold: 0.8,
    enablePunctuation: true,
    enableWordTimeOffsets: true
  },

  ui: {
    theme: {
      primaryColor: '#667eea',
      secondaryColor: '#764ba2',
      successColor: '#28a745',
      warningColor: '#ffc107',
      errorColor: '#dc3545',
      infoColor: '#17a2b8'
    },
    layout: {
      headerHeight: '80px',
      sidebarWidth: '250px',
      maxContentWidth: '1200px'
    },
    animations: {
      transitionDuration: '0.3s',
      enableAnimations: true
    }
  },

  export: {
    supportedFormats: ['docx', 'pdf'],
    defaultFormat: 'docx',
    templatePath: '/templates/patient-form-template.docx'
  },

  storage: {
    localStorageKey: 's2t-medical-app',
    sessionStorageKey: 's2t-medical-session',
    maxCacheSize: 50 * 1024 * 1024,
    cacheExpiration: 24 * 60 * 60 * 1000
  },

  development: {
    enableDevTools: process.env.NODE_ENV === 'development',
    mockApiResponses: true,
    logLevel: 'debug'
  }
}
