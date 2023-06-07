namespace :search_suggestions do
    desc "Generate search suggestions for existing Houses"
    task index: :environment do
      House.find_each do |house|
        SearchSuggestion.create(term: house.Localizacao, popularity: 1)
      end
    end
  end