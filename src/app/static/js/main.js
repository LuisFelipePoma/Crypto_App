// chart.js
import { plot_series } from './charts.js'

// Query Selector
const $ = e => document.querySelector(e)
const $iconLoadingDialog = $('#loading-icon-dialog')
const $ctx = document.getElementById('chart')

// Agregamos eventos a los botones de la página
const $closeDialog = document.querySelector('dialog button')
const $dialog = document.querySelector('dialog')
$closeDialog.addEventListener('click', () => {
  $dialog.close()
})

//<-------------------------------  Agregamos la funcionalidad de abrir el dialog
// Muestra informacion de la moneda
const $coinInfo = $('#coin-info')

function showCoinInfo (coinData) {
  $coinInfo.innerHTML = `
        <h2>${coinData.name}</h2>
        <p><span>Market Cap</span>: $${coinData.market_cap.toLocaleString(
          undefined,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )}</p>
        <p><span>Price</span>: $${coinData.current_price.toLocaleString(
          undefined,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )}</p>
        <p><span>Volume</span>: $${coinData.total_volume.toLocaleString(
          undefined,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )}</p>
        <p><span>Total supply</span>: ${coinData.total_supply.toLocaleString(
          undefined,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )}</p>
        <p><span>Max. Supply</span>: ${coinData.max_supply.toLocaleString(
          undefined,
          { minimumFractionDigits: 2, maximumFractionDigits: 2 }
        )}</p>
        <p><span>Category</span>: ${coinData.category}</p>
`
}

// Exporta la función showDialog
function showDialog (event) {
  // Mostramos el modal con la predicción
  $dialog.showModal()
  // Obtenemos la info del elemento
  const coin = event.getAttribute('coin-data')
  const coinData = JSON.parse(coin.replace(/'/g, '"'))
  showCoinInfo(coinData)
  $iconLoadingDialog.style.display = 'flex'
  $ctx.style.display = 'none'
  // Realizamos la peticion al backend
  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ coinId: coinData.id })
  })
    .then(response => response.json())
    .then(data => {
      setTimeout(() => {
        plot_series(data.data)
        $iconLoadingDialog.style.display = 'none'
        $ctx.style.display = 'block'
      }, 1000)
    })
    .catch(error => {
      console.error('Error:', error)
    })
}
// Agregamos el evento

const coins = document.querySelectorAll('.coin-bubble')

coins.forEach(coin => {
  coin.addEventListener('click', () => {
    showDialog(coin)
  })
})

// Search
const $searchCoin = $('#search-coin')
const $iconLoadingSearch = $('#loading-icon-search')
const $generalCoinsList = $('#general-coins')
const $coinBubbleTemplate = $('#coin-bubble-template')

function searchCoin () {
  $iconLoadingSearch.style.display = 'flex'
  fetch('/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: $searchCoin.value })
  })
    .then(response => response.json())
    .then(data => {
      const coins = data.data
      if (coins.length === 0) {
        $generalCoinsList.innerHTML =
          '<h6><br>No tenemos monedas con ese nombre.</br><h6>'
        $iconLoadingSearch.style.display = 'none'
        return
      }

      $generalCoinsList.innerHTML = ''
      coins.forEach(coin => {
        const $coinBubble = $coinBubbleTemplate.content
          .cloneNode(true)
          .querySelector('.coin-bubble')
        console.log($coinBubble)
        $coinBubble.setAttribute('coin-data', JSON.stringify(coin))
        $coinBubble.querySelector('img').src = coin.image
        $coinBubble.querySelector('p').innerHTML = coin.symbol

        // add event
        $coinBubble.addEventListener('click', () => {
          showDialog($coinBubble)
        })
        $generalCoinsList.appendChild($coinBubble)
      })
      $iconLoadingSearch.style.display = 'none'
    })
    .catch(error => {
      console.error('Error fetching movies:', error)
      $iconLoadingSearch.style.display = 'none'
    })
}

$searchCoin.addEventListener('change', searchCoin)
