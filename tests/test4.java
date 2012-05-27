import java.io.IOException;

class test4 {
  
  public static void main(String[] args) throws IOException {
    
    PyMarkObject pets_two = PyMarkObject.Unpack("pets_two.pmk");
    
    System.out.printf("TypeID: %d\n", pets_two.get("pets.catherine.type").asInt()); 
    System.out.printf("Name: %s\n", pets_two.get("pets.catherine.name").asString());
    
    PyMarkObject color = pets_two.get("pets.catherine.color");
    System.out.printf("Color: (%d, %d, %d)\n", color.at(0).asInt(),
                                               color.at(1).asInt(),
                                               color.at(2).asInt());
  
  }

}
