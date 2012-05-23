{-# LANGUAGE GADTs, TypeSynonymInstances, FlexibleInstances #-}

module PyMark where

import Data.Binary.Get
import Data.Binary.Put
import Data.Binary.IEEE754
import Data.ByteString.Lazy (ByteString, hGetContents)
import Data.Word
import Data.Char
import Data.List.Split

import Text.Printf
import System.IO hiding (hGetContents)
import Control.Monad

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

data NoneType = None deriving (Show, Eq)

class PyMarkAble a where
  
  pyMarkType :: a -> Int
  pyMarkTypeError :: a -> String -> b
  pyMarkTypeError x t = error $ "PyMark Object of TypeID " ++ show (pyMarkType x) ++ " is not a " ++ t
  
  pyMarkAt :: a -> Int -> PyMarkObject
  pyMarkGet :: a -> String -> PyMarkObject
  pyMarkGet' :: a -> [String] -> PyMarkObject
  
  pyMarkAt x i = pyMarkTypeError x "List"
  pyMarkGet x s = pyMarkTypeError x "Dict"
  pyMarkGet' x s = pyMarkTypeError x "Dict"
  
  pyMarkAsInt :: a -> Int
  pyMarkAsLong :: a -> Integer
  pyMarkAsFloat :: a -> Float
  pyMarkAsDouble :: a -> Double
  pyMarkAsBool :: a -> Bool
  pyMarkAsNone :: a -> NoneType
  pyMarkAsString :: a -> String
  
  pyMarkAsInt x = pyMarkTypeError x "Int"
  pyMarkAsLong x = pyMarkTypeError x "Long"
  pyMarkAsFloat x = pyMarkTypeError x "Float"
  pyMarkAsDouble x = pyMarkTypeError x "Double"
  pyMarkAsBool x = pyMarkTypeError x "Bool"
  pyMarkAsNone x = pyMarkTypeError x "None"
  pyMarkAsString x = pyMarkTypeError x "String"

instance PyMarkAble Int where { pyMarkType x = pyMarkIntType; pyMarkAsInt = id }
instance PyMarkAble Integer  where { pyMarkType x = pyMarkLongType; pyMarkAsLong = id }
instance PyMarkAble Float where { pyMarkType x = pyMarkFloatType; pyMarkAsFloat = id }
instance PyMarkAble Double where { pyMarkType x = pyMarkDoubleType; pyMarkAsDouble = id }
instance PyMarkAble Bool where { pyMarkType x = pyMarkBoolType; pyMarkAsBool = id }
instance PyMarkAble NoneType where { pyMarkType x = pyMarkNoneType; pyMarkAsNone = id }
instance PyMarkAble String where { pyMarkType x = pyMarkStringType; pyMarkAsString = id }
instance PyMarkAble [PyMarkObject] where
  pyMarkType x = pyMarkListType
  pyMarkAt x i = x !! i
  
  pyMarkGet x s = pyMarkGet' x (splitOn "." s)
  
  pyMarkGet' x [] = PyMarkObject x
  pyMarkGet' x [s] = (head [ps ! 1 | ps <- x, (asString (ps ! 0)) == s ])
  pyMarkGet' x (s:ss) = (head [ps ! 1 | ps <- x, (asString (ps ! 0)) == s ]) !!-> ss
  
  
data PyMarkObject where PyMarkObject :: (PyMarkAble a, Show a) => a -> PyMarkObject

(!) :: PyMarkObject -> Int -> PyMarkObject
(!) (PyMarkObject p) i = pyMarkAt p i

(!->) :: PyMarkObject -> String -> PyMarkObject
(!->) (PyMarkObject p) s = pyMarkGet p s

(!!->) :: PyMarkObject -> [String] -> PyMarkObject
(!!->) (PyMarkObject p) s = pyMarkGet' p s

asInt (PyMarkObject p) = pyMarkAsInt p
asLong (PyMarkObject p) = pyMarkAsLong p
asFloat (PyMarkObject p) = pyMarkAsFloat p
asDouble (PyMarkObject p) = pyMarkAsDouble p
asBool (PyMarkObject p) = pyMarkAsBool p
asNone (PyMarkObject p) = pyMarkAsNone p
asString (PyMarkObject p) = pyMarkAsString p

instance Show PyMarkObject where show (PyMarkObject p) = show p

pyMarkUnpackList :: Get PyMarkObject
pyMarkUnpackList = do
  len <- getWord64le
  objs <- replicateM (fromIntegral len) pyMarkUnpackObject
  return $ PyMarkObject objs

pyMarkUnpackType :: Int -> Get PyMarkObject
pyMarkUnpackType t
  |t == pyMarkIntType = do { x <- getWord32le; return $ PyMarkObject (fromIntegral x :: Int) }
  |t == pyMarkLongType = do { x <- getWord64le; return $ PyMarkObject (fromIntegral x :: Integer) }
  |t == pyMarkFloatType = do { x <- getFloat32le; return $ PyMarkObject x }
  |t == pyMarkDoubleType = do { x <- getFloat64le; return $ PyMarkObject x }
  |t == pyMarkBoolType = do
    x <- getWord8; if (fromIntegral x :: Int) == 0 
                   then return (PyMarkObject True)
                   else return (PyMarkObject False)
  |t == pyMarkNoneType = return $ PyMarkObject None
  |t == pyMarkStringType = do
    len <- getWord64le
    words <- replicateM (fromIntegral len) getWord8
    return $ PyMarkObject (map (\x -> chr (fromIntegral x)) words)
  |t == pyMarkTupleType = pyMarkUnpackList
  |t == pyMarkListType = pyMarkUnpackList
  |t == pyMarkDictType = pyMarkUnpackList
  |otherwise = error $ "Unknown PyMark TypeID" ++ show t
  
pyMarkUnpackObject :: Get PyMarkObject
pyMarkUnpackObject = do
  t <- getWord8
  pyMarkUnpackType ((fromIntegral t) :: Int)
  
pyMarkUnpack :: FilePath -> IO PyMarkObject
pyMarkUnpack file = do
  hndl <- openBinaryFile file ReadMode
  magic <- replicateM 6 (hGetChar hndl)
  if magic /= "PYMARK" then return $ error "Bad magic number for file" else return ()
  version <- hGetChar hndl
  if version /= (chr 1) then return $ error "Bad version number for file" else return ()
  bs <- hGetContents hndl
  obj <- return $ runGet pyMarkUnpackObject bs
  return obj

pyMarkPackObject :: Put
pyMarkPackObject = undefined

pyMarkPack :: FilePath -> PyMarkObject -> IO ()
pyMarkPack file obj = undefined
