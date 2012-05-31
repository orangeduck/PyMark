(use 'pymark)

(let [pets-two (pymark-unpack "pets_two.pmk")]
  (do
    (printf "TypeID: %d\n" (get-in pets-two ["pets" "catherine" "type"]))
    (printf "Name: %s\n" (get-in pets-two ["pets" "catherine" "name"]))
    
    (let [color (get-in pets-two ["pets" "catherine" "color"])]
      (printf "Color: (%d, %d, %d)\n" (nth color 0) (nth color 1) (nth color 2))) ))