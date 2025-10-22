/**
 * Export Service
 * Handles export functionality for Word and PDF documents
 */

import { PatientForm } from '@/models/PatientForm.js'

class ExportService {
  constructor() {
    this.supportedFormats = ['docx', 'pdf']
    this.defaultFormat = 'docx'
  }

  /**
   * Export patient data to Word document
   */
  async exportPatientToWord(patient, recordings = []) {
    try {
      // For MVP, create a simple HTML document that can be saved as Word
      const htmlContent = this.generatePatientDocumentHTML(patient, recordings)
      
      // Create and download the document
      const blob = new Blob([htmlContent], { type: 'application/msword' })
      const url = URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `Pacient_${patient.name.replace(/\s+/g, '_')}_${this.formatDate(new Date())}.doc`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      URL.revokeObjectURL(url)
      
      return { success: true, filename: link.download }
    } catch (error) {
      console.error('Failed to export patient to Word:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * Export patient data to PDF
   */
  async exportPatientToPDF(patient, recordings = []) {
    try {
      // For MVP, create HTML content that can be printed as PDF
      const htmlContent = this.generatePatientDocumentHTML(patient, recordings)
      
      // Open in new window for printing
      const printWindow = window.open('', '_blank')
      printWindow.document.write(htmlContent)
      printWindow.document.close()
      
      // Add print styles
      const style = printWindow.document.createElement('style')
      style.textContent = `
        @media print {
          body { font-family: Arial, sans-serif; margin: 20px; }
          .header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
          .section { margin-bottom: 20px; }
          .section h3 { color: #333; border-bottom: 1px solid #ccc; }
          .observation { background: #f5f5f5; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
        }
      `
      printWindow.document.head.appendChild(style)
      
      // Trigger print dialog
      printWindow.focus()
      printWindow.print()
      
      return { success: true }
    } catch (error) {
      console.error('Failed to export patient to PDF:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * Generate HTML content for patient document
   */
  generatePatientDocumentHTML(patient, recordings = []) {
    const currentDate = this.formatDate(new Date())
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Fisa Pacientului - ${patient.name}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
          .header { border-bottom: 2px solid #333; padding-bottom: 15px; margin-bottom: 30px; }
          .header h1 { color: #333; margin: 0; }
          .header .date { color: #666; font-size: 14px; }
          .section { margin-bottom: 25px; }
          .section h3 { color: #333; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
          .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
          .info-item { margin-bottom: 10px; }
          .info-label { font-weight: bold; color: #555; }
          .observation { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; border-radius: 4px; }
          .observation .timestamp { font-size: 12px; color: #666; margin-bottom: 5px; }
          .transcription { background: #e8f4fd; border-left-color: #28a745; }
          .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 12px; color: #666; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>FISA PACIENTULUI</h1>
          <div class="date">Generat la: ${currentDate}</div>
        </div>

        <div class="section">
          <h3>PERSONAL INFORMATION</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Nume:</span> ${patient.name}
            </div>
            <div class="info-item">
              <span class="info-label">Age:</span> ${patient.age} years old
            </div>
            <div class="info-item">
              <span class="info-label">Sex:</span> ${patient.gender}
            </div>
            <div class="info-item">
              <span class="info-label">Date of Birth:</span> ${patient.dateOfBirth || 'N/A'}
            </div>
            <div class="info-item">
              <span class="info-label">Telefon:</span> ${patient.phone || 'N/A'}
            </div>
            <div class="info-item">
              <span class="info-label">Email:</span> ${patient.email || 'N/A'}
            </div>
          </div>
          <div class="info-item">
            <span class="info-label">Address:</span> ${patient.address || 'N/A'}
          </div>
        </div>

        <div class="section">
          <h3>MEDICAL INFORMATION</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Grup sanguin:</span> ${patient.bloodType || 'N/A'}
            </div>
            <div class="info-item">
              <span class="info-label">Insurance Number:</span> ${patient.insuranceNumber || 'N/A'}
            </div>
          </div>
          <div class="info-item">
            <span class="info-label">Medical History:</span><br>
            ${patient.medicalHistory || 'No information available'}
          </div>
          <div class="info-item">
            <span class="info-label">Allergies:</span><br>
            ${patient.allergies || 'No known allergies'}
          </div>
          <div class="info-item">
            <span class="info-label">Current Medications:</span><br>
            ${patient.currentMedications || 'No medications'}
          </div>
          <div class="info-item">
            <span class="info-label">Emergency Contact:</span><br>
            ${patient.emergencyContact || 'No information available'}
          </div>
        </div>

        ${recordings.length > 0 ? `
        <div class="section">
          <h3>OBSERVATIONS AND TRANSCRIPTIONS</h3>
          ${recordings.map(recording => `
            <div class="observation ${recording.transcription ? 'transcription' : ''}">
              <div class="timestamp">
                ${this.formatDate(recording.timestamp)} - 
                ${recording.transcription ? 'Audio transcription' : 'Manual observation'}
              </div>
              <div class="content">
                ${recording.transcription || recording.text}
              </div>
            </div>
          `).join('')}
        </div>
        ` : ''}

        <div class="footer">
          <p>Document generat automat de sistemul Speech-to-Text Medical</p>
          <p>Generation date: ${currentDate}</p>
        </div>
      </body>
      </html>
    `
  }

  /**
   * Export multiple patients to batch document
   */
  async exportBatchPatients(patients, format = 'docx') {
    try {
      const htmlContent = this.generateBatchDocumentHTML(patients)
      
      const blob = new Blob([htmlContent], { 
        type: format === 'pdf' ? 'text/html' : 'application/msword' 
      })
      const url = URL.createObjectURL(blob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `Pacienti_${this.formatDate(new Date())}.${format === 'pdf' ? 'html' : 'doc'}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      URL.revokeObjectURL(url)
      
      return { success: true, filename: link.download }
    } catch (error) {
      console.error('Failed to export batch patients:', error)
      return { success: false, error: error.message }
    }
  }

  /**
   * Generate batch document HTML
   */
  generateBatchDocumentHTML(patients) {
    const currentDate = this.formatDate(new Date())
    
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Patient List - ${currentDate}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 15px; }
          .patient-summary { border: 1px solid #ccc; margin-bottom: 20px; padding: 15px; border-radius: 5px; }
          .patient-summary h3 { margin-top: 0; color: #333; }
          .info-row { margin-bottom: 5px; }
          .info-label { font-weight: bold; display: inline-block; width: 150px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>LISTA PACIENTI</h1>
          <p>Generat la: ${currentDate}</p>
        </div>
        
        ${patients.map(patient => `
          <div class="patient-summary">
            <h3>${patient.name}</h3>
            <div class="info-row">
              <span class="info-label">Age:</span> ${patient.age} years old
            </div>
            <div class="info-row">
              <span class="info-label">Sex:</span> ${patient.gender}
            </div>
            <div class="info-row">
              <span class="info-label">Telefon:</span> ${patient.phone || 'N/A'}
            </div>
            <div class="info-row">
              <span class="info-label">Last visit:</span> ${this.formatDate(patient.updatedAt)}
            </div>
          </div>
        `).join('')}
      </body>
      </html>
    `
  }

  /**
   * Format date for display
   */
  formatDate(date) {
    const d = new Date(date)
    return d.toLocaleDateString('ro-RO', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  /**
   * Get supported export formats
   */
  getSupportedFormats() {
    return this.supportedFormats
  }

  /**
   * Validate export data
   */
  validateExportData(patient, recordings = []) {
    const errors = []
    
    if (!patient || !patient.name) {
      errors.push('Patient data is required')
    }
    
    if (!patient.age || patient.age < 0) {
      errors.push('Valid patient age is required')
    }
    
    return {
      isValid: errors.length === 0,
      errors
    }
  }
}

// Create and export singleton instance
export const exportService = new ExportService()
export default exportService

