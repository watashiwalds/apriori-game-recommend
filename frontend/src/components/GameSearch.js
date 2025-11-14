import {
  CButton,
  CCard,
  CCol,
  CForm,
  CFormInput,
  CListGroup,
  CListGroupItem,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'
import { useCallback, useState } from 'react'
import { findGames } from '../api/api'
import debounce from 'lodash.debounce'

const similarGamesPlaceholder = [
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Apex Legends', time: 123 },
  { name: 'Crab Game', time: 123 },
  { name: 'Blood Hunt', time: 12.3 },
  { name: 'Vampire Survivors', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
  { name: 'Blood Strike', time: 12.3 },
]

const GameSearch = () => {
  const [game, setGame] = useState('')
  const [duration, setDuration] = useState('')
  const [showDropdown, setShowDropdown] = useState(false)
  const [filteredGames, setFilteredGames] = useState([])
  const [similarGames, setSimilarGames] = useState([])

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debounceSearch = useCallback(
    debounce(async (value) => {
      console.log('Searching for: ', value)
      // call api
      try {
        const data = await findGames(value)
        setFilteredGames(data)
      } catch (error) {
        console.error(error)
      }
    }, 500),
    [],
  )

  const handleChangeGame = (text) => {
    setGame(text)
    debounceSearch(text)
  }

  const handleFindSimilarGames = () => { }

  return (
    <>
      <h1 className="text-center font-bold mb-4">Apriori Game Recommended</h1>

      <CCard className="p-4 mb-4 shadow-sm rounded-lg">
        <CForm className="row g-3 align-items-end">
          <CCol md={7} className="position-relative">
            <div style={{ position: 'relative' }}>
              <CFormInput
                label="Tìm kiếm game"
                placeholder="Nhập game cần tìm kiếm..."
                value={game}
                onChange={(e) => handleChangeGame(e.target.value)}
                onFocus={() => setShowDropdown(game.length > 0)}
                onBlur={() => setTimeout(() => setShowDropdown(game.length > 0), 150)}
              />

              {showDropdown && filteredGames.length > 0 && (
                <CListGroup
                  style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    zIndex: 1000,
                    maxHeight: 150,
                    overflowY: 'auto',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                  }}
                >
                  {filteredGames.map((game) => (
                    <CListGroupItem
                      key={game}
                      onClick={() => {
                        setGame(game)
                        setShowDropdown(false)
                      }}
                      style={{ cursor: 'pointer' }}
                      className="hover:bg-blue-50"
                    >
                      {game}
                    </CListGroupItem>
                  ))}
                </CListGroup>
              )}
            </div>
          </CCol>

          <CCol md={3}>
            <CFormInput
              type="number"
              step="0.01"
              min="0"
              label="Thời lượng chơi (VD: 123.40 giờ)"
              placeholder="Nhập thời lượng chơi mong muốn..."
              value={duration}
              onChange={(e) => {
                const val = parseFloat(e.target.value)
                if (val >= 0) setDuration(e.target.value)
              }}
            />
          </CCol>

          <CCol md={2} className="d-flex align-items-end">
            <CButton
              color="info"
              className="text-white w-100"
              onClick={() => handleFindSimilarGames()}
            >
              Tìm trò chơi tương tự
            </CButton>
          </CCol>
        </CForm>
      </CCard>

      <CCard className="p-3" style={{ maxHeight: '500px', overflowY: 'auto' }}>
        <CTable striped hover responsive>
          <CTableHead className="sticky-top bg-white shadow-sm">
            <CTableRow>
              <CTableHeaderCell scope="col">Tên trò chơi</CTableHeaderCell>
              <CTableHeaderCell scope="col">Thời lượng chơi</CTableHeaderCell>
              <CTableHeaderCell scope="col">Steam?</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {similarGamesPlaceholder.map((game, index) => (
              <CTableRow key={index} className="hover:bg-gray-50 transition-colors">
                <CTableDataCell className="font-medium">{game.name}</CTableDataCell>
                <CTableDataCell>{game.time}</CTableDataCell>
                <CTableDataCell>
                  <a
                    href={`https://store.steampowered.com/search/?term=${encodeURIComponent(
                      game.name,
                    )}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-medium"
                  >
                    Steam
                  </a>
                </CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      </CCard>
    </>
  )
}

export default GameSearch
