# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_05_11_035029) do
  create_table "delayed_jobs", force: :cascade do |t|
    t.integer "priority", default: 0, null: false
    t.integer "attempts", default: 0, null: false
    t.text "handler", null: false
    t.text "last_error"
    t.datetime "run_at"
    t.datetime "locked_at"
    t.datetime "failed_at"
    t.string "locked_by"
    t.string "queue"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.index ["priority", "run_at"], name: "delayed_jobs_priority"
  end

  create_table "favorites", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "house_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["house_id"], name: "index_favorites_on_house_id"
    t.index ["user_id"], name: "index_favorites_on_user_id"
  end

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

  create_table "search_suggestions", force: :cascade do |t|
    t.string "term"
    t.integer "popularity"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "searches", force: :cascade do |t|
    t.integer "user_id"
    t.text "search_criteria"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "url"
  end

  create_table "users", force: :cascade do |t|
    t.string "name"
    t.string "email"
    t.string "password_digest"
    t.string "role"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_foreign_key "favorites", "houses", primary_key: "Id", on_delete: :cascade
  add_foreign_key "favorites", "users"
end
