class CreateHouses < ActiveRecord::Migration[7.0]
  def change
    create_table "houses", primary_key: "Id", force: :cascade do |t|
      t.string "Url", limit: 196
      t.string "Id_link", limit: 36
      t.string "Type", limit: 12
      t.string "Referencia", limit: 48
      t.string "Situacao", limit: 7
      t.string "Condicao", limit: 41
      t.string "Title", limit: 72
      t.integer "Price"
      t.string "Certifacao_Energética", limit: 18
      t.string "Localizacao", limit: 131
      t.decimal "Latitude"
      t.decimal "Longitude"
      t.decimal "Area_Util"
      t.decimal "Area_Bruta"
      t.decimal "Price_per_Area"
      t.integer "Ano_de_Construcao"
      t.string "Data_Publicacao", limit: 17
      t.integer "Alpendre"
      t.integer "Casa_de_Banho_Partilhada"
      t.integer "Casas_de_Banho"
      t.integer "Copas"
      t.integer "Cozinhas"
      t.integer "Escritórios"
      t.integer "Hall_de_Quartos"
      t.integer "Lavabo"
      t.integer "Marquise"
      t.integer "Open_Space"
      t.integer "Quarto_de_hóspedes"
      t.integer "Salas_de_Jantar"
      t.integer "Suites"
      t.integer "Total_quartos"
      t.integer "Varandas"
      t.integer "Casa_de_banho_de_serviço"
      t.integer "Casa_de_Banho_Privativa"
      t.integer "Closet"
      t.integer "Corredor"
      t.integer "Despensas"
      t.integer "Hall_de_Entrada"
      t.integer "Kitchenet"
      t.integer "Lavandaria"
      t.integer "Número_de_pisos"
      t.integer "Outras_Salas"
      t.integer "Salas"
      t.integer "Sotão"
      t.integer "Telhado_Verde"
      t.integer "Total_quartos_interiores"
      t.string "Acesso_Mobilidade_Reduzida", limit: 5
      t.string "Arrecadação", limit: 5
      t.string "Elevador", limit: 5
      t.string "Garagem", limit: 5
      t.string "Estacionamento", limit: 5
      t.string "Jardim", limit: 5
      t.string "Lareira", limit: 5
      t.string "Recuperador_de_calor", limit: 5
      t.string "Vidros_Duplos", limit: 5
      t.string "Varanda", limit: 5
      t.string "Terraço", limit: 5
      t.string "Suite", limit: 5
      t.string "Segurança", limit: 5
      t.string "Piscina", limit: 5
      t.string "Painéis_Solares", limit: 5
      t.string "Mobília", limit: 5
      t.string "Logradouro", limit: 5  
    end
  end
end
