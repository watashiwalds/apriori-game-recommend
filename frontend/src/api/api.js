import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 3000,
})

const searchGame = async (name) => {
  const res = await api.get('/search_game', { params: { name } })
  console.log(res)
  return res.data
}

const getRecommendGames = async (gameIds) => {
  const res = await api.post('/recomment', { id_game: gameIds })
  return res.data
}

const getGameByIds = async (ids) => {
  const res = await api.post('/get_games_by_ids', { ids: ids })
  return res.data
}

export { searchGame, getRecommendGames, getGameByIds }
