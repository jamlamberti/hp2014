class HomepageController < ApplicationController
  def index
  	fetch_data
  end

  def fetch_data
  	@hash_of_teachers = {}

  	File.open("public/data.json", "r") do |file|
  		i = 0
  		file.each do |line|
  			tempHash = JSON.parse(line)
  			courseNumber = tempHash.delete("courseNumber")
  			@hash_of_teachers[courseNumber] = tempHash
  		end
  	end
  end
end
