class AddUrlToSearches < ActiveRecord::Migration[7.0]
  def change
    add_column :searches, :url, :string
  end
end
