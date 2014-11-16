class HomepageController < ApplicationController
  def index
  	fetch_data
  end

  def fetch_data
  	@hash_of_professors = {}
    @average_difficulty = 0;

    File.open("public/data.json", "r") do |file|
      i = 0
      total = 0;
      file.each do |line|
        i+=1;
        tempHash = JSON.parse(line)
        id = tempHash.delete("id")
        total+= Integer(tempHash["difficulty"])
        if(@hash_of_professors[id] != nil) ##It's already been put in there
          @hash_of_professors[id] << tempHash
        else
         @hash_of_professors[id] = [tempHash]
       end
     end
     @average_difficulty = total.to_f / i.to_f
   end
 end
end
