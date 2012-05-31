(ns pymark
  "PyMark binary parser"
  (:import (java.io InputStream OutputStream 
                    FileInputStream FileOutputStream
                    IOException))
  (:import (java.nio ByteBuffer ByteOrder))
  (:import (java.nio.channels FileChannel)))


(def pymark-int-type    (byte 1 ))
(def pymark-long-type   (byte 2 ))
(def pymark-float-type  (byte 3 ))
(def pymark-double-type (byte 4 ))
(def pymark-bool-type   (byte 5 ))
(def pymark-none-type   (byte 6 ))
(def pymark-string-type (byte 7 ))
(def pymark-tuple-type  (byte 8 ))
(def pymark-list-type   (byte 9 ))
(def pymark-dict-type   (byte 10))

(def pymark-magic "PYMARK")
(def pymark-version (byte 1))


(defn unfold [pairs]
  "Unfolds a list of pairs into a single list"
  (if (= pairs []) []
  (cons (nth (first pairs) 0) (cons (nth (first pairs) 1) (unfold (rest pairs))))))

  
(defn pymark-unpack-object [bb]
  "Unpacks a PyMark object from a ByteBuffer"
  (let [t (.get bb)]
  (cond
    (= t pymark-int-type) (.getInt bb)
    (= t pymark-long-type) (.getLong bb)
    (= t pymark-float-type) (.getFloat bb)
    (= t pymark-double-type) (.getDouble bb)
    (= t pymark-bool-type) (if (= (.get bb) 1) true false)
    (= t pymark-none-type) nil
    (= t pymark-string-type)
      (let [bytestr (byte-array (.getLong bb))] do
        (.get bb bytestr) (new String bytestr) )
    (= t pymark-tuple-type) (doall (repeatedly (.getLong bb) #(pymark-unpack-object bb)))
    (= t pymark-list-type)  (doall (repeatedly (.getLong bb) #(pymark-unpack-object bb)))
    (= t pymark-dict-type) (apply hash-map (unfold (doall (repeatedly (.getLong bb) #(pymark-unpack-object bb)))))
  :default (throw (new IOException (str "PyMark: Unknown TypeID " t))) )))

  
(defn bytes-to-string [bytes]
  "Converts a byte array to a string"
  (apply str (map char bytes)))

  
(defn pymark-unpack [filename]
  "Unpacks a PyMark Object from a file"
  (with-open [chan (.getChannel (FileInputStream. filename))]
    (let [magic (byte-array 6)
          bb (ByteBuffer/allocateDirect (.size chan))]
      (do
        (.order bb ByteOrder/LITTLE_ENDIAN)
        (.read chan bb)
        (.rewind bb)
        (.get bb magic)
        (if (not= (bytes-to-string magic) pymark-magic) (throw (new IOException "Badly Formed PyMark file magic number")))
        (if (not= (.get bb) pymark-version) (throw (new IOException "Badly Formed PyMark file version number")))
        (pymark-unpack-object bb) ))))
 

(defn object-size [obj]
  "Works out the needed allocation size for a ByteBuffer"
  (cond
    (= (type obj) Integer) (+ 1 4)
    (= (type obj) Long) (+ 1 8)
    (= (type obj) Float) (+ 1 4)
    (= (type obj) Double) (+ 1 8)
    (= (type obj) Boolean) (+ 1 1)
    (= (type obj) nil) 1
    (= (type obj) String) (+ 1 8 (.length obj))
    (or (= (type obj) clojure.lang.PersistentVector)
        (= (type obj) clojure.lang.MapEntry)
        (= (type obj) clojure.lang.LazySeq)) (+ 1 8 (apply + (doall (map object-size obj))))
    (= (type obj) clojure.lang.PersistentHashMap) (+ 1 8 (apply + (doall (map object-size (seq obj)))))
  :default (throw (new IOException (str "Unknown PyMark Type " (type obj)))) ))
  
  
(defn pymark-pack-object [bb obj]
  "Packs a PyMark object into a ByteBuffer"
  (cond
    (= (type obj) Integer) (do (.put bb pymark-int-type) (.putInt bb obj))
    (= (type obj) Long) (do (.put bb pymark-long-type) (.putInt bb obj))
    (= (type obj) Float) (do (.put bb pymark-float-type) (.putInt bb obj))
    (= (type obj) Double) (do (.put bb pymark-double-type) (.putInt bb obj))
    (= (type obj) Boolean) (do (.put bb pymark-bool-type) (if (= obj true) (.put bb 1) (.put bb 0)))
    (= (type obj) nil) (.put bb pymark-none-type)
    (= (type obj) String) (do
      (.put bb pymark-string-type)
      (.putLong bb (count obj))
      (.put bb (.getBytes obj)) )
    (or (= (type obj) clojure.lang.PersistentVector)
        (= (type obj) clojure.lang.MapEntry)
        (= (type obj) clojure.lang.LazySeq)) (do 
      (.put bb pymark-list-type)
      (.putLong bb (count obj)) 
      (doall (map (fn [x] (pymark-pack-object bb x)) obj)) )
    (= (type obj) clojure.lang.PersistentHashMap) (do 
      (.put bb pymark-dict-type)
      (.putLong bb (count obj)) 
      (doall (map (fn [x] (pymark-pack-object bb x)) (seq obj))) )
  :default (throw (new IOException (str "Unknown PyMark Type " (type obj)))) ))
 

(defn pymark-pack [filename obj]
  "Packs a PyMark Object into a file"
  (with-open [chan (.getChannel (FileOutputStream. filename))]
    (let [bb (ByteBuffer/allocateDirect (+ 6 1 (object-size obj)))]
      (do
        (.order bb ByteOrder/LITTLE_ENDIAN)
        (.put bb (.getBytes pymark-magic))
        (.put bb pymark-version)
        (pymark-pack-object bb obj)
        (.rewind bb)
        (.write chan bb) ))))
        