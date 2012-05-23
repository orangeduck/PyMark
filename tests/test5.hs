import Text.Printf

import PyMark

main = do
  pets_two <- pyMarkUnpack "pets_two.pmk"
  
  printf "TypeID: %i\n" $ asInt (pets_two !-> "pets.catherine.type")
  printf "Name: %s\n" $ asString (pets_two !-> "pets.catherine.name")
  
  color <- return (pets_two !-> "pets.catherine.color")
  printf "Color: (%i, %i, %i)\n" (asInt $ color ! 0) (asInt $ color ! 1) (asInt $ color ! 2)
  
  