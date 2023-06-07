class Favorite < ApplicationRecord
  belongs_to :user
  belongs_to :house
  validates :house_id, uniqueness: { scope: :user_id, message: "has already been favorited by this user" }
end
