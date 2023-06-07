function populateSelectedMarkersTable(selectedHouses, numColumns, sortOrder, minPrice, maxPrice, showNullPrices) {

console.log(minPrice, maxPrice, showNullPrices, sortOrder);


if ((minPrice !== null && maxPrice !== null) || showNullPrices) {
  selectedHouses = selectedHouses.filter(function (house) {
    const price = parseFloat(house.Price);
    console.log(price);
    if (showNullPrices) { 
      return (isNaN(price) || price >= minPrice && price <= maxPrice);
    } else {
      return (price >= minPrice && price <= maxPrice);
    }
  });
}

  if (sortOrder) {
    switch (sortOrder) {
      case "price-low-to-high":
        selectedHouses.sort(function (a, b) {
          return a.Price - b.Price;
        });
        break;
      case "price-high-to-low":
        selectedHouses.sort(function (a, b) {
          return b.Price - a.Price;
        });
        break;
      case "area-small-to-large":
        selectedHouses.sort(function (a, b) {
          return a.Ano_de_Construcao - b.Ano_de_Construcao;
        });
        break;
      case "area-large-to-small":
        selectedHouses.sort(function (a, b) {
          return b.Ano_de_Construcao - a.Ano_de_Construcao;
        });
        break;
      default:
        break;
    }
  }


  var tableBody = document.getElementById("selected-markers-table").getElementsByTagName("tbody")[0];
  tableBody.innerHTML = ''; // Clear the table body
  var template = `
    <div>
      <div class="card-box-a card-shadow">
        <div class="img-box-a">
          <img src="{{imageUrl}}" width="350" height="350" alt="" class="img-a img-fluid" style="width: 350px !important; height: 350px !important;">
        </div>
        <div class="card-overlay">
          <div class="card-overlay-a-content">
            <div class="card-header-a">
              <h2 class="card-title-a">
                <a href="#">{{location}}</a>
              </h2>
            </div>
            <div class="card-body-a">
              <div class="price-box d-flex">
                <span class="price-a">{{status}} | {{price}}€</span>
              </div>
              <a href="/property_single.{{id}}" class="link-a">Details</a>
              <span class="ion-ios-arrow-forward"></span>
            </div>
            <div class="card-footer-a">
              <ul class="card-info d-flex justify-content-around">
                <li>
                  <h4 class="card-info-title">Area</h4>
                  <span>{{area}}m<sup>2</sup></span>
                </li>
                <li>
                  <h4 class="card-info-title">Bedrooms</h4>
                  <span>{{bedrooms}}</span>
                </li>
                <li>
                  <h4 class="card-info-title">Condition</h4>
                  <span>{{condition}}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>  
      </div>
    </div>
  `;
  var row, cell, html, houseIndex;
  for (var i = 0; i < selectedHouses.length; i++) {
    houseIndex = i % numColumns;
    if (houseIndex == 0) {
      row = tableBody.insertRow();
    }
    cell = row.insertCell(houseIndex);
    html = template.replace('{{imageUrl}}', selectedHouses[i].ImageUrl || 'img/house-default.jpg')
      .replace('{{location}}', selectedHouses[i].Localizacao)
      .replace('{{status}}', selectedHouses[i].Situacao)
      .replace('{{price}}', selectedHouses[i].Price || '')
      .replace('{{id}}', selectedHouses[i].Id)
      .replace('{{area}}', selectedHouses[i].Area_Util || '')
      .replace('{{bedrooms}}', selectedHouses[i].Total_quartos || '')
      .replace('{{condition}}', selectedHouses[i].Condicao || '');
    cell.innerHTML = html;
  }
}