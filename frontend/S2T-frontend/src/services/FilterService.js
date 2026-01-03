class FilterService {
  constructor() {
    this.filters = {
      patients: {
        name: '',
        ageRange: { min: null, max: null },
        gender: '',
        dateRange: { start: null, end: null },
        hasRecordings: null
      },
      recordings: {
        patientId: null,
        dateRange: { start: null, end: null },
        duration: { min: null, max: null },
        hasTranscription: null,
        confidence: { min: null, max: null }
      }
    }
  }

  filterPatients(patients, criteria = {}) {
    if (!Array.isArray(patients)) return []

    return patients.filter(patient => {
      if (criteria.name && !patient.name.toLowerCase().includes(criteria.name.toLowerCase())) {
        return false
      }

      if (criteria.ageRange) {
        if (criteria.ageRange.min !== null && patient.age < criteria.ageRange.min) {
          return false
        }
        if (criteria.ageRange.max !== null && patient.age > criteria.ageRange.max) {
          return false
        }
      }

      if (criteria.gender && criteria.gender.trim() !== '' && patient.gender !== criteria.gender) {
        return false
      }

      if (criteria.dateRange) {
        const patientDate = new Date(patient.updatedAt || patient.createdAt)
        if (criteria.dateRange.start && patientDate < new Date(criteria.dateRange.start)) {
          return false
        }
        if (criteria.dateRange.end && patientDate > new Date(criteria.dateRange.end)) {
          return false
        }
      }

      if (criteria.hasRecordings !== null) {
        const hasRecordings = patient.observations && patient.observations.length > 0
        if (criteria.hasRecordings && !hasRecordings) {
          return false
        }
        if (!criteria.hasRecordings && hasRecordings) {
          return false
        }
      }

      return true
    })
  }

  filterRecordings(recordings, criteria = {}) {
    if (!Array.isArray(recordings)) return []

    return recordings.filter(recording => {
      if (criteria.patientId && recording.patientId !== criteria.patientId) {
        return false
      }

      if (criteria.dateRange) {
        const recordingDate = new Date(recording.timestamp)
        if (criteria.dateRange.start && recordingDate < new Date(criteria.dateRange.start)) {
          return false
        }
        if (criteria.dateRange.end && recordingDate > new Date(criteria.dateRange.end)) {
          return false
        }
      }

      if (criteria.duration) {
        if (criteria.duration.min !== null && recording.duration < criteria.duration.min) {
          return false
        }
        if (criteria.duration.max !== null && recording.duration > criteria.duration.max) {
          return false
        }
      }

      if (criteria.hasTranscription !== null) {
        const hasTranscription = recording.transcription && recording.transcription.text
        if (criteria.hasTranscription && !hasTranscription) {
          return false
        }
        if (!criteria.hasTranscription && hasTranscription) {
          return false
        }
      }

      if (criteria.confidence) {
        if (criteria.confidence.min !== null && recording.transcription?.confidence < criteria.confidence.min) {
          return false
        }
        if (criteria.confidence.max !== null && recording.transcription?.confidence > criteria.confidence.max) {
          return false
        }
      }

      return true
    })
  }

  searchPatients(patients, query) {
    if (!query || !query.trim()) return patients

    const searchTerm = query.toLowerCase()
    
    return patients.filter(patient => {
      return (
        patient.name.toLowerCase().includes(searchTerm) ||
        patient.phone?.toLowerCase().includes(searchTerm) ||
        patient.email?.toLowerCase().includes(searchTerm) ||
        patient.medicalHistory?.toLowerCase().includes(searchTerm) ||
        patient.allergies?.toLowerCase().includes(searchTerm) ||
        patient.currentMedications?.toLowerCase().includes(searchTerm)
      )
    })
  }

  searchRecordings(recordings, query) {
    if (!query || !query.trim()) return recordings

    const searchTerm = query.toLowerCase()
    
    return recordings.filter(recording => {
      return (
        recording.transcription?.text.toLowerCase().includes(searchTerm) ||
        recording.patientName?.toLowerCase().includes(searchTerm)
      )
    })
  }

  sortPatients(patients, sortBy = 'name', sortOrder = 'asc') {
    return [...patients].sort((a, b) => {
      let aValue = a[sortBy]
      let bValue = b[sortBy]

      if (sortBy === 'createdAt' || sortBy === 'updatedAt') {
        aValue = new Date(aValue)
        bValue = new Date(bValue)
      }

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase()
        bValue = bValue.toLowerCase()
      }

      if (sortOrder === 'desc') {
        return bValue > aValue ? 1 : -1
      } else {
        return aValue > bValue ? 1 : -1
      }
    })
  }

  sortRecordings(recordings, sortBy = 'timestamp', sortOrder = 'desc') {
    return [...recordings].sort((a, b) => {
      let aValue = a[sortBy]
      let bValue = b[sortBy]

      if (sortBy === 'timestamp' || sortBy === 'startTime') {
        aValue = new Date(aValue)
        bValue = new Date(bValue)
      }

      if (sortBy === 'confidence') {
        aValue = a.transcription?.confidence || 0
        bValue = b.transcription?.confidence || 0
      }

      if (sortOrder === 'desc') {
        return bValue > aValue ? 1 : -1
      } else {
        return aValue > bValue ? 1 : -1
      }
    })
  }

  getPatientFilterOptions(patients) {
    const genders = [...new Set(patients.map(p => p.gender).filter(Boolean))]
    const ageGroups = this.getAgeGroups(patients)
    const hasRecordingsOptions = [
      { value: true, label: 'With recordings' },
      { value: false, label: 'Without recordings' }
    ]

    return {
      genders: genders.map(gender => ({ value: gender, label: gender })),
      ageGroups,
      hasRecordingsOptions
    }
  }

  getAgeGroups(patients) {
    const ages = patients.map(p => p.age).filter(age => age > 0)
    const minAge = Math.min(...ages)
    const maxAge = Math.max(...ages)

    const groups = []
    for (let i = Math.floor(minAge / 10) * 10; i <= Math.ceil(maxAge / 10) * 10; i += 10) {
      groups.push({
        value: { min: i, max: i + 9 },
        label: `${i}-${i + 9} ani`
      })
    }

    return groups
  }

  clearFilters() {
    this.filters = {
      patients: {
        name: '',
        ageRange: { min: null, max: null },
        gender: '',
        dateRange: { start: null, end: null },
        hasRecordings: null
      },
      recordings: {
        patientId: null,
        dateRange: { start: null, end: null },
        duration: { min: null, max: null },
        hasTranscription: null,
        confidence: { min: null, max: null }
      }
    }
  }

  getFilters() {
    return this.filters
  }

  setFilter(category, key, value) {
    if (this.filters[category]) {
      this.filters[category][key] = value
    }
  }
}

export const filterService = new FilterService()
export default filterService

