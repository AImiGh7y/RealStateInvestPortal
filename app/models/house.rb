class House < ApplicationRecord
    self.primary_key = 'Id'
    has_many :favorites, foreign_key: 'house_id'
    has_many :users_who_favorited, through: :favorites, source: :user
end
