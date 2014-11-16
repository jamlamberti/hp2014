class HomepageController < ApplicationController
  def index
  	fetch_data
  end

  def fetch_data
  	@hash_of_professors = {}

  	File.open("public/data.json", "r") do |file|
  		i = 0
  		file.each do |line|
  			tempHash = JSON.parse(line)
  			id = tempHash.delete("id")
  			@hash_of_professors[id] = tempHash
  		end
  	end
  end
end
