{-# LANGUAGE GADTs, TypeSynonymInstances, FlexibleInstances #-}

module PyMark where

import Data.Binary.Get
import Data.Binary.Put
import Data.Binary.IEEE754
import Data.ByteString.Lazy (ByteString, hGetContents, hPut)
import Data.Word
import Data.Char
import Data.List
import Data.List.Split

import Text.Printf
import System.IO hiding (hGetContents)
import Control.Monad


-- Type indicies
pyMarkIntType    = 1
pyMarkLongType   = 2
pyMarkFloatType  = 3
pyMarkDoubleType = 4
pyMarkBoolType   = 5
pyMarkNoneType   = 6
pyMarkStringType = 7
pyMarkTupleType  = 8
pyMarkListType   = 9
pyMarkDictType   = 10


-- Could have used 'Nothing' but defining a new type seemed easier
data NoneType = None deriving (Show, Eq)


-- Represents a type which can be serialized or deserialized
class PyMarkAble a where
  
  -- Class functions
  typeId :: a -> Int
  typeLength :: a -> Int
  typeCastError :: String -> a -> b
  
  (!) :: a -> Int -> PyMarkObject
  (!#) :: a -> String -> PyMarkObject
  
  asInt :: a -> Int
  asLong :: a -> Integer
  asFloat :: a -> Float
  asDouble :: a -> Double
  asBool :: a -> Bool
  asNone :: a -> NoneType
  asString :: a -> String
  asList :: a -> [PyMarkObject]
  
  -- Defaults
  typeLength = typeCastError "List"
  typeCastError t x = error $ "PyMark Object of TypeID " ++ show (typeId x) ++ " is not a " ++ t
  
  (!) x i = typeCastError "List" x
  (!#) x k = typeCastError "Dict" x
  
  asInt = typeCastError "Int"
  asLong = typeCastError "Long"
  asFloat = typeCastError "Float"
  asDouble = typeCastError "Double"
  asBool = typeCastError "Bool"
  asNone = typeCastError "None"
  asString = typeCastError "String"
  asList = typeCastError "List"

  
-- Existential Type for PyMarkAble Objects
data PyMarkObject where PyMarkObject :: (PyMarkAble a, Show a) => a -> PyMarkObject
instance Show PyMarkObject where show (PyMarkObject p) = show p
instance PyMarkAble PyMarkObject where
  typeId (PyMarkObject p) = typeId p
  typeLength (PyMarkObject p) = typeLength p
  (!) (PyMarkObject p) i = p ! i
  (!#) (PyMarkObject p) k = p !# k
  asInt (PyMarkObject p) = asInt p
  asLong (PyMarkObject p) = asLong p
  asFloat (PyMarkObject p) = asFloat p
  asDouble (PyMarkObject p) = asDouble p
  asBool (PyMarkObject p) = asBool p
  asNone (PyMarkObject p) = asNone p
  asString (PyMarkObject p) = asString p
  asList (PyMarkObject p) = asList p
  
  
-- Instances for basic types
instance PyMarkAble Int where { typeId = const pyMarkIntType; asInt = id }
instance PyMarkAble Integer  where { typeId = const pyMarkLongType; asLong = id }
instance PyMarkAble Float where { typeId = const pyMarkFloatType; asFloat = id }
instance PyMarkAble Double where { typeId = const pyMarkDoubleType; asDouble = id }
instance PyMarkAble Bool where { typeId = const pyMarkBoolType; asBool = id }
instance PyMarkAble NoneType where { typeId = const pyMarkNoneType; asNone = id }

instance PyMarkAble String where 
  typeId = const pyMarkStringType
  typeLength = length
  asString = id
  
instance PyMarkAble [PyMarkObject] where
  typeId = const pyMarkListType
  typeLength = length
  asList = id
  (!) x i = x !! i
  (!#) x s = if length (rest s) == 0 then (lookup x (first s))
             else (lookup x (first s)) !# (intercalate "." (rest s)) 
    where first s = head (splitOn "." s)
          rest s = tail (splitOn "." s)
          lookup x s = head [ps!1 | ps <- x, asString (ps!0) == s ]
  
  
-- Unpacks a collection object
pyMarkUnpackList :: Get PyMarkObject
pyMarkUnpackList = do
  len <- getWord64le
  objs <- replicateM (fromIntegral len) pyMarkUnpackObject
  return $ PyMarkObject objs

  
-- Unpacks an object of a specified type index
pyMarkUnpackType :: Int -> Get PyMarkObject
pyMarkUnpackType t
  | pyMarkIntType    == t = do { x <- getWord32le; return $ PyMarkObject (fromIntegral x :: Int) }
  | pyMarkLongType   == t = do { x <- getWord64le; return $ PyMarkObject (fromIntegral x :: Integer) }
  | pyMarkFloatType  == t = do { x <- getFloat32le; return $ PyMarkObject x }
  | pyMarkDoubleType == t = do { x <- getFloat64le; return $ PyMarkObject x }
  | pyMarkBoolType   == t = do
      x <- getWord8
      if (fromIntegral x) == 0 
      then return (PyMarkObject True)
      else return (PyMarkObject False)
  
  | pyMarkNoneType   == t = return $ PyMarkObject None
  | pyMarkStringType == t = do
      len <- getWord64le
      words <- replicateM (fromIntegral len) getWord8
      return $ PyMarkObject (map (chr . fromIntegral) words)
  
  | pyMarkTupleType == t = pyMarkUnpackList
  | pyMarkListType  == t = pyMarkUnpackList
  | pyMarkDictType  == t = pyMarkUnpackList
  
  | otherwise = error $ "Unknown PyMark TypeID" ++ show t
  
  
-- Reads type information and unpacks specified type
pyMarkUnpackObject :: Get PyMarkObject
pyMarkUnpackObject = getWord8 >>= pyMarkUnpackType . fromIntegral


-- Unpacks Object from filename
pyMarkUnpack :: FilePath -> IO PyMarkObject
pyMarkUnpack file = do
  hndl <- openBinaryFile file ReadMode
  
  magic <- replicateM 6 (hGetChar hndl)
  if magic /= "PYMARK" 
  then ioError (userError "Bad magic number for file")
  else return ()
  
  version <- hGetChar hndl
  if version /= (chr 1)
  then ioError (userError "Bad version number for file")
  else return ()
  
  bs <- hGetContents hndl
  return $ runGet pyMarkUnpackObject bs

  
-- Packs a list type
pyMarkPackList :: PyMarkObject -> Put
pyMarkPackList obj = do
  putWord64le $ (fromIntegral . typeLength) obj
  mapM_ pyMarkPackObject $ asList obj
  
-- Given a type index packs that type object
pyMarkPackType :: Int -> PyMarkObject -> Put
pyMarkPackType t obj
  | pyMarkIntType    == t = putWord32le $ (fromIntegral . asInt) obj
  | pyMarkLongType   == t = putWord64le $ (fromIntegral . asLong) obj
  | pyMarkFloatType  == t = putFloat32le $ (asFloat obj)
  | pyMarkDoubleType == t = putFloat64le $ (asDouble obj)
  | pyMarkBoolType   == t = if (asBool obj) then putWord8 1 else putWord8 0
  | pyMarkNoneType   == t = return ()
  | pyMarkStringType == t = do
      putWord64le $ (fromIntegral . typeLength) obj
      mapM_ (\x -> putWord8 $ (fromIntegral . ord) x) (asString obj)
  | pyMarkTupleType == t = pyMarkPackList obj
  | pyMarkListType  == t = pyMarkPackList obj
  | pyMarkDictType  == t = pyMarkPackList obj
  | otherwise = error $ "Unknown PyMark TypeID" ++ show t
  
  
-- Packs a PyMarkObject
pyMarkPackObject :: PyMarkObject -> Put
pyMarkPackObject obj = do
  putWord8 $ fromIntegral (typeId obj)
  pyMarkPackType (typeId obj) obj
  
  
-- Packs a PyMarkObject into a file
pyMarkPack :: FilePath -> PyMarkObject -> IO ()
pyMarkPack file obj = do
  hndl <- openBinaryFile file WriteMode
  hPutStr hndl "PYMARK"
  hPutChar hndl (chr 1)
  hPut hndl $ runPut (pyMarkPackObject obj)
  hClose hndl