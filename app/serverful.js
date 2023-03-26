const express = require('express')
const app = express()

let count = 0 // initial state

app.get('/', (req, res) => {
  res.send(`Current count: ${count}`)
})

app.post('/increment', (req, res) => {
  count++
  res.send(`Count incremented to ${count}`)
})

app.post('/decrement', (req, res) => {
  count--
  res.send(`Count decremented to ${count}`)
})

app.listen(3000, () => {
  console.log('Server started on port 3000')
})
