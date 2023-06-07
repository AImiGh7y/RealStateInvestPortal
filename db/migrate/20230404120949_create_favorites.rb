class CreateFavorites < ActiveRecord::Migration[7.0]
  def change
    create_table :favorites do |t|
      t.belongs_to :user, null: false, foreign_key: true
      t.belongs_to :house, null: false, foreign_key: { to_table: :houses, primary_key: 'Id', on_delete: :cascade }

      t.timestamps
    end
  end
end
