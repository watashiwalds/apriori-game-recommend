import {
  CButton,
  CCard,
  CCol,
  CForm,
  CFormInput,
  CListGroup,
  CListGroupItem,
  CSpinner,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
} from '@coreui/react'
import { useCallback, useState } from 'react'
import { getGameByIds, getRecommendGames, searchGame } from '../api/api'
import debounce from 'lodash.debounce'
import { SelectedItem } from './SelectedItem'

const GameSearch = () => {
  // =========VARIABLES=========
  const [game, setGame] = useState('')
  const [duration, setDuration] = useState('')
  const [showDropdown, setShowDropdown] = useState(false)
  const [filteredGames, setFilteredGames] = useState([])
  const [filteredGameIndex, setfilteredGameIndex] = useState(-1)
  const [recommendGames, setRecommendGames] = useState([])
  const [selectedGames, setSelectedGames] = useState([])
  const [loading, setLoading] = useState(false)

  // =========REACT HOOKS=========
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debounceSearch = useCallback(
    debounce(async (value) => {
      console.log('Searching for: ', value)
      try {
        const res = await searchGame(value)
        setFilteredGames(res.data.slice(0, 50))
      } catch (error) {
        console.error(error)
        setFilteredGames([])
      }
    }, 500),
    [],
  )

  const handleChangeGame = (text) => {
    setGame(text)
    setfilteredGameIndex(-1)
    if (text.length > 0) {
      setShowDropdown(true)
      debounceSearch(text)
    } else {
      setShowDropdown(false)
    }
  }

  const handleClickItemDropdown = (index) => {
    setShowDropdown(false)
    setGame(filteredGames[index].game_title)
    setfilteredGameIndex(index)
  }

  const handleAddGame = () => {
    if (filteredGameIndex === -1) {
      alert('Vui lòng nhập tên game hợp lệ!')
      return
    }
    const newValue = {
      gameId: filteredGames[filteredGameIndex].game_id,
      gameTitle: filteredGames[filteredGameIndex].game_title,
      duration: duration,
    }
    setSelectedGames((prev) => [...prev, newValue])
  }
  const handleFindRecommendGames = async () => {
    try {
      setLoading(true)
      const inputGameIds = selectedGames.map((g) => g.gameId)
      console.log(inputGameIds)
      const outputGameIds = await getRecommendGames(inputGameIds)
      const res = await getGameByIds(outputGameIds)
      const nomalizeData = res.data.map((g) => ({ gameId: g.game_id, gameTitle: g.game_title }))
      setRecommendGames(nomalizeData)
    } catch (err) {
      console.error(err)
      setRecommendGames([])
    } finally {
      setLoading(false)
    }
  }

  // =========UI=========
  return (
    <>
      <h1 className="text-center font-bold mb-4">Apriori Game Recommended</h1>

      <CCard className="p-4 mb-4 shadow-lg rounded-2xl">
        <CForm className="row g-3 align-items-end d-flex">
          {/* Search Game Input */}
          <CCol md={12} lg={5} className="flex-grow-1">
            <CFormInput
              label="Tìm kiếm game"
              placeholder="Nhập game cần tìm kiếm..."
              value={game}
              onChange={(e) => handleChangeGame(e.target.value)}
              onFocus={() => setShowDropdown(game.length > 0)}
              onBlur={() => setTimeout(() => setShowDropdown(false), 150)}
            />
            {showDropdown && filteredGames.length > 0 && (
              <CListGroup
                style={{
                  position: 'absolute',
                  top: '100%',
                  left: 0,
                  right: 0,
                  zIndex: 9999,
                  maxHeight: 300,
                  overflowY: 'auto',
                  boxShadow: '0 6px 12px rgba(0,0,0,0.15)',
                  borderRadius: '0 0 0.5rem 0.5rem',
                }}
              >
                {filteredGames.map((game, index) => (
                  <CListGroupItem
                    key={index}
                    onClick={() => handleClickItemDropdown(index)}
                    style={{ cursor: 'pointer' }}
                    className="hover:bg-blue-50"
                  >
                    {game.game_title}
                  </CListGroupItem>
                ))}
              </CListGroup>
            )}
          </CCol>

          {/* Duration Input */}
          <CCol md={12} lg={2} className="flex-grow-1">
            <CFormInput
              type="number"
              step="0.01"
              min="0"
              label="Thời lượng chơi"
              placeholder="123,45"
              value={duration}
              onChange={(e) => {
                const val = parseFloat(e.target.value)
                if (val >= 0) setDuration(e.target.value)
              }}
            />
          </CCol>

          {/* Add Game Button */}
          <CCol md={6} lg={2} className="d-flex justify-content-end">
            <CButton color="info" className="text-white w-100 shadow-sm" onClick={handleAddGame}>
              Thêm trò chơi
            </CButton>
          </CCol>

          {/* Find Recommend Button */}
          <CCol md={6} lg={3} className="d-flex justify-content-end">
            <CButton
              color="success"
              className="text-white w-100 d-flex justify-content-center align-items-center gap-2 shadow-sm"
              style={{ whiteSpace: 'nowrap' }}
              onClick={handleFindRecommendGames}
              disabled={loading}
            >
              {loading && <CSpinner color="light" size="sm" />}
              Tìm trò chơi tương tự
            </CButton>
          </CCol>
        </CForm>

        {/* Selected Games List */}
        <div className="mt-4 flex flex-col gap-2">
          {selectedGames.map((game, index) => (
            <SelectedItem
              key={index}
              index={index}
              gameName={game.gameTitle}
              duration={game.duration}
              onDelete={() => setSelectedGames((prev) => prev.filter((_, i) => i !== index))}
            />
          ))}
        </div>
      </CCard>

      <CCard
        className="p-4 mb-4 shadow-lg rounded-xl"
        style={{ maxHeight: '500px', overflowY: 'auto' }}
      >
        <CTable striped hover responsive>
          <CTableHead className="sticky top-0 bg-white shadow-sm">
            <CTableRow>
              <CTableHeaderCell scope="col">Tên trò chơi</CTableHeaderCell>
              <CTableHeaderCell scope="col">Thời lượng chơi</CTableHeaderCell>
              <CTableHeaderCell scope="col">Tìm trên Steam?</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {recommendGames.length > 0 ? (
              recommendGames.map((game, index) => (
                <CTableRow key={index} className="hover:bg-gray-50 transition-colors duration-200">
                  <CTableDataCell className="font-medium">{game.gameTitle}</CTableDataCell>
                  <CTableDataCell className="text-gray-600">_</CTableDataCell>
                  <CTableDataCell>
                    <a
                      href={`https://store.steampowered.com/search/?term=${encodeURIComponent(
                        game.gameTitle,
                      )}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline font-medium"
                    >
                      Steam
                    </a>
                  </CTableDataCell>
                </CTableRow>
              ))
            ) : (
              <CTableRow>
                <CTableDataCell colSpan={3} className="text-center text-gray-500 py-4">
                  Không tìm thấy trò chơi phù hợp
                </CTableDataCell>
              </CTableRow>
            )}
          </CTableBody>
        </CTable>
      </CCard>
    </>
  )
}

export default GameSearch
