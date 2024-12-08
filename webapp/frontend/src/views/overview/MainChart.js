import React, { useEffect, useRef } from 'react'

import PropTypes from 'prop-types'

import { CChartBar } from '@coreui/react-chartjs'
import { getStyle } from '@coreui/utils'

const MainChart = ({ data }) => {
  const chartRef = useRef(null)

  useEffect(() => {
    document.documentElement.addEventListener('ColorSchemeChange', () => {
      if (chartRef.current) {
        setTimeout(() => {
          chartRef.current.options.scales.x.grid.borderColor = getStyle(
            '--cui-border-color-translucent',
          )
          chartRef.current.options.scales.x.grid.color = getStyle('--cui-border-color-translucent')
          chartRef.current.options.scales.x.ticks.color = getStyle('--cui-body-color')
          chartRef.current.options.scales.y.grid.borderColor = getStyle(
            '--cui-border-color-translucent',
          )
          chartRef.current.options.scales.y.grid.color = getStyle('--cui-border-color-translucent')
          chartRef.current.options.scales.y.ticks.color = getStyle('--cui-body-color')
          chartRef.current.update()
        })
      }
    })
  }, [chartRef])

  const nicknames = data.map((item) => item.nickname)
  const followerCounts = data.map((item) => item.follower_count)

  return (
    <>
      <CChartBar
        data={{
          labels: nicknames,
          datasets: [
            {
              label: 'Follower Count',
              backgroundColor: '#f87979',
              data: followerCounts,
            },
          ],
        }}
        labels="authors"
      />
    </>
  )
}

MainChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      nickname: PropTypes.string.isRequired,
      follower_count: PropTypes.number.isRequired,
    }),
  ).isRequired,
}

export default MainChart
