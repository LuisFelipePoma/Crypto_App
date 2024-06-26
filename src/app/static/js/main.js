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
const $predictionArticle = $('#prediction')

function showCoinInfo (coinData) {
  const template = document
    .getElementById('coin-info-template')
    .content.cloneNode(true)

  template.querySelector('h2').textContent = coinData.name
  template.querySelector('.market-cap').textContent =
    coinData.market_cap.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  template.querySelector('.current-price').textContent =
    coinData.current_price.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  template.querySelector('.total-volume').textContent =
    coinData.total_volume.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  template.querySelector('.total-supply').textContent =
    coinData.total_supply.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  template.querySelector('.max-supply').textContent = coinData.max_supply
    ? coinData.max_supply.toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    : 'N/A'
  template.querySelector('.category').textContent = coinData.category

  // show exchanges
  const centralized = coinData.exchanges_centralized
  const decentralized = coinData.exchanges_decentralized

  const $centralized = template.querySelector('.centralized')
  const $decentralized = template.querySelector('.decentralized')

  $centralized.innerHTML = ''
  $decentralized.innerHTML = ''

  if (centralized.length === 0) {
    $centralized.innerHTML = ''
  } else {
    $centralized.appendChild(document.createElement('p')).textContent =
      'Centralizados'
    centralized.forEach(exchange => {
      const $exchange = document.createElement('small')
      $exchange.textContent = exchange
      $centralized.appendChild($exchange)
    })
  }

  if (decentralized.length === 0) {
    $decentralized.innerHTML = ''
  } else {
    $decentralized.appendChild(document.createElement('p')).textContent =
      'Descentralizados'
    decentralized.forEach(exchange => {
      const $exchange = document.createElement('small')
      $exchange.textContent = exchange
      $decentralized.appendChild($exchange)
    })
  }
  // Clear existing content
  $coinInfo.innerHTML = ''
  $coinInfo.appendChild(template)
}

// <------------------------------ función showMetadata ------------------------------>
const $metadataChart = $('#metadata-chart')
const $metadataChartTemplate = $('#metadata-chart-template')

// Un RSI por debajo de 30 indica sobreventa,
// mientras que por encima de 70 indica sobrecompra.
function showMetadataChart (metadata) {
  const template = $metadataChartTemplate.content.cloneNode(true)
  template.querySelector('.sharper').textContent = Number(
    metadata.sharper
  ).toFixed(6)
  template.querySelector('.log-return').textContent = Number(
    metadata.log_return
  ).toFixed(6)
  // RSI
  template.querySelector('.mean-rsi').textContent = `${Number(
    metadata.mean_rsi
  ).toFixed(2)}${
    metadata.mean_rsi < 30
      ? ' (Oversold)'
      : metadata.mean_rsi > 70
      ? ' (Overbought)'
      : ' ~'
  }`
  template.querySelector('.mean-rsi').style.color =
    metadata.mean_rsi < 30 ? 'green' : metadata.mean_rsi > 70 ? 'red' : 'black'
  //
  template.querySelector('.volatility').textContent = Number(
    metadata.volatility
  ).toFixed(4)
  // Clear existing content
  $metadataChart.innerHTML = ''
  $metadataChart.appendChild(template)
}

// <------------------------------ función showDialog ------------------------------>
function showDialog (event) {
  // Mostramos el modal con la predicción
  $predictionArticle.innerHTML = ''
  $metadataChart.innerHTML = ''
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
      console.log(data)
      setTimeout(() => {
        // add prediction
        const prediction = data.predict
        if (prediction === 1) {
          $predictionArticle.innerHTML = `<p>Esta moneda <span class="up">aumentara</span> su precio <span class="up">x2</span></p>`
        } else {
          $predictionArticle.innerHTML = `<p>Esta moneda <span class="low">no aumentara</span> su precio</p>`
        }
        // plot chart
        plot_series(data.data)
        // show metadata
        showMetadataChart(data.metadata)
        // set styles
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

// <------------------------------ Search------------------------------>
const $searchCoin = $('#search-coin')
const $generalCoinsList = $('#general-coins')
const $coinBubbleTemplate = $('#coin-bubble-template')

function searchCoin () {
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
        return
      }

      $generalCoinsList.innerHTML = ''
      coins.forEach(coin => {
        const $coinBubble = $coinBubbleTemplate.content
          .cloneNode(true)
          .querySelector('.coin-bubble')
        $coinBubble.setAttribute('coin-data', JSON.stringify(coin))
        $coinBubble.querySelector('img').src = coin.image
        $coinBubble.querySelector('p').innerHTML = coin.symbol

        // add event
        $coinBubble.addEventListener('click', () => {
          showDialog($coinBubble)
        })
        $generalCoinsList.appendChild($coinBubble)
      })
    })
    .catch(error => {
      console.error('Error fetching movies:', error)
    })
}

$searchCoin.addEventListener('change', searchCoin)

// <------------------------------ Coins  low market ------------------------------>

// <------------------------------ CHANGE BEHAVIOUR SCROLL ------------------------------>
const $listTags = document.querySelectorAll('.list-tag')
// Apply scroll behav
$listTags.forEach(list => {
  list.addEventListener('wheel', evt => {
    evt.preventDefault() // Avoid vertical scroll
    list.scrollBy({
      left: evt.deltaY * 2.5, // Adjust velocity
      behavior: 'smooth'
    })
  })
})
