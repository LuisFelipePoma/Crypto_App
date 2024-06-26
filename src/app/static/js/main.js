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
    $centralized.innerHTML = '<p>No hay exchanges centralizados</p>'
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
    $decentralized.innerHTML = '<p>No hay exchanges descentralizados</p>'
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
const $metadataChartTemplate = $("#metadata-chart-template")

{/* <template id="metadata-chart-template">
		<p><span>Sharper ratio</span class="sharper">: <span></span></p>
		<p><span>Log Return</span class="log-return">: <span></span>%</p>
		<p><span>Mean RSI</span>: <span class="mean-rsi"></span></p>
		<p><span>Std RSI</span>: <span class="std-rsi"></span></p>
		<p><span>Volatility</span>: <span class="volatility"></span>%</p>
	</template> */}

function showMetadataChart(metadata){
	console.log(metadata.log_return)
	const template = $metadataChartTemplate.content.cloneNode(true)
	template.querySelector('.sharper span').textContent = metadata.sharper
	template.querySelector('.log-return span').textContent = metadata.log_return
	template.querySelector('.mean-rsi').textContent = metadata.mean_rsi
	template.querySelector('.std-rsi').textContent = metadata.std_rsi
	template.querySelector('.volatility').textContent = metadata.volatility
	// Clear existing content
	$metadataChart.innerHTML = ''
	$metadataChart.appendChild(template)
}

// <------------------------------ función showDialog ------------------------------>
function showDialog (event) {
  // Mostramos el modal con la predicción
  $predictionArticle.innerHTML = ''
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
				// show metadata
				showMetadataChart(data.metadata)
        // plot chart
        plot_series(data.data)
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
