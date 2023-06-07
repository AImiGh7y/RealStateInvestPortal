class SearchSuggestionsController < ApplicationController
  def index
    term = params[:term].downcase
    suggestions = SearchSuggestion.where('term LIKE ?', "#{term}%").select('DISTINCT term').order('popularity DESC').limit(10)
    render json: suggestions.map(&:term)
  end
  end