Rails.application.routes.draw do
  resources :search_suggestions
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  root "house#index"
  get '/index', to: 'house#index'
  get '/contact', to: 'house#contact'
  get '/about', to: 'house#about'
  get '/property-grid', to: 'house#property_grid', as: 'search_houses'
  get '/property_single', to: 'house#property_single'
  post '/pages/test', to: 'pages#test'

  resources :houses, controller: 'house' do
    member do
      get 'property_single/:id', to: 'house#property_single', as: 'property_single'
    end
  end

  
  get '/scrape', to: 'pages#scrape'

  resources :users, only: [:new, :create]
  get '/users/login', to: 'users#login', as: 'login'
  post '/users/login', to: 'users#login'
  delete '/logout', to: 'users#logout', as: 'logout'

  post '/property_single/:id/favorite', to: 'house#favorite', as: 'favorite_house'
  delete '/property_single/:id/unfavorite', to: 'house#unfavorite', as: 'unfavorite_house'
  
  get '/users/:id/favourites', to: 'users#favorites', as: 'user_favourites'
  
  get '/users/:id/searches', to: 'users#search', as: 'search'

  post '/property-grid/:id/save_search', to: 'house#save_search', as: 'save_search'
  delete '/property-grid/:id/delete_search', to: 'house#delete_search', as: 'delete_search'

  get '/map_districts', to: 'house#map_districts', as: 'map_districts'

  get '/scripts', to: 'scripts#index'
  post '/scripts/run', to: 'scripts#run_script', as: :run_script
  

  get '/users/index', to: 'users#index', as: 'users_index' 
  patch '/users/update_selected_roles', to: 'users#update_selected_roles', as: 'update_selected_roles_users'




end
