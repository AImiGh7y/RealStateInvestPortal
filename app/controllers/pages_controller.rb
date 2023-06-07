require 'nokogiri'
require 'open-uri'

class PagesController < ApplicationController
    def scrape(houses)
      urls = []
      houses.each do |house|
        urls.append(house.Url)
      end
      @results = scrape_webpage(urls)
    end

  def scrape_webpage(urls)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    images = []
  
    urls.each do |url|
      begin
        response = URI.open(url, 'User-Agent' => user_agent)
        if response.status[0] == '200'
          html = response.read
          doc = Nokogiri::HTML(html)
  
          # Extract the URL of the first image from the HTML using CSS selectors
          source = doc.css('picture.property-photos source').first
          if source && source['srcset']
            image_url = source['srcset'].split(' ').first
            images << image_url
          end
        else
          images << nil
        end
      rescue StandardError => e
        puts "Error scraping #{url}: #{e.message}"
        images << nil
        next
      end
    end
  
    # Return the list of image URLs as an array or an empty array if not found
    images
  end

  def scrape_single(house)
    urls = (house.Url)
    
    @results = scrape_webpage_single(urls)
  end

  def scrape_webpage_single(url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    images = []
  
    begin
      response = URI.open(url, 'User-Agent' => user_agent)
      if response.status[0] == '200'
        html = response.read
        doc = Nokogiri::HTML(html)
  
        # Extract the URL of the first image from the HTML using CSS selectors
        source = doc.css('picture.property-photos source').first
        if source && source['srcset']
          image_url = source['srcset'].split(' ').first
          images << image_url
        end
        
        # Extract the URL of the first image from the HTML using CSS selectors
        property_photos = doc.css('.property-photos')
        property_photos.each do |elem|
          img_src = elem.css('source').first['data-srcset']
          images << img_src
        end
      else
        puts "null"
      end
    rescue StandardError => e
      puts "Error scraping #{url}: #{e.message}"
    end
    # Return the list of image URLs as an array or an empty array if not found
    images
  end
  
  protect_from_forgery unless: -> { request.format.json? }
  
  def test
    my_array = params[:urls]
    # Call scrape_webpage passing my_array
    images = scrape_webpage(my_array)
    # Return the list of image URLs as an array or an empty array if not found
    render json: {message: "Success", value: images}
  end
  
  
end
