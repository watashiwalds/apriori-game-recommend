import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8888',
  timeout: 3000,
})

const database = ['Blood Strike', 'Apex Legends', 'Crab Game', 'Blood Hunt', 'Vampire Survivors']
const getGames = (text, excludedGames) => {
  return database
    .filter((game) => !excludedGames.includes(game))
    .filter((game) => game.toLowerCase().includes(text.toLowerCase()))
}

const findGames = async (keyword) => {
  const res = await api.get('/all_games', { params: { keyword } })
  return res.data
}

const getSimilarGames = async (game) => {
  const res = await api.get('/all_games', { params: { game } })
  return res.data
}

export { findGames, getGames, getSimilarGames, database }
