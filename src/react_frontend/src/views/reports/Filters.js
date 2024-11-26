import React, { useState } from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import PropTypes from 'prop-types'
import { cilCalendar, cilTag } from '@coreui/icons'
import CIcon from '@coreui/icons-react'

import { CRow, CCol, CFormSelect } from '@coreui/react'

const Filters = ({ onDateRangeChange, hashtags, selectedHashtag, setSelectedHashtag }) => {
  const [dateRange, setDateRange] = useState([null, null]) // State for date range
  const [startDate, endDate] = dateRange

  return (
    <CRow className="mb-4 align-items-center">
      {/* Date Range Picker */}
      <CCol xs="12" md="6">
        <div className="d-flex flex-column">
          <label className="form-label fw-bold mb-1">
            <CIcon icon={cilCalendar} className="me-2" />
            Select Date Range
          </label>
          <DatePicker
            selected={startDate}
            onChange={(dates) => {
              setDateRange(dates)
              if (dates && dates[0] && dates[1]) {
                onDateRangeChange(dates)
              } else {
                onDateRangeChange([null, null])
              }
            }}
            startDate={startDate}
            endDate={endDate}
            selectsRange
            isClearable
            placeholderText="Choose a date range"
            className="form-control shadow-sm wider-picker"
            calendarClassName="w-100" // Ensures calendar scales with wider picker
            style={{ width: '100%' }} // Inline width adjustment for the picker
          />
        </div>
      </CCol>

      {/* Hashtag Filter */}
      <CCol xs="12" md="6">
        <div className="d-flex flex-column">
          <label className="form-label fw-bold mb-1">
            <CIcon icon={cilTag} className="me-2" />
            Filter by Hashtag
          </label>
          <CFormSelect
            value={selectedHashtag}
            onChange={(e) => setSelectedHashtag(e.target.value)}
            className="shadow-sm"
          >
            <option value="all">All Hashtags</option>
            {hashtags.map((hashtag) => (
              <option key={hashtag.id} value={hashtag.title}>
                {hashtag.title}
              </option>
            ))}
          </CFormSelect>
        </div>
      </CCol>
    </CRow>
  )
}

Filters.propTypes = {
  onDateRangeChange: PropTypes.func.isRequired,
  hashtags: PropTypes.array.isRequired,
  selectedHashtag: PropTypes.string.isRequired,
  setSelectedHashtag: PropTypes.func.isRequired,
}

export default Filters
