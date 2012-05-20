import java.util.Hashtable;
import java.util.Arrays;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

import java.lang.Integer;

public class PyMarkObject {
  
	public static final byte PyMarkIntType    = 1;
	public static final byte PyMarkLongType   = 2;
	public static final byte PyMarkFloatType  = 3;
	public static final byte PyMarkDoubleType = 4;
	public static final byte PyMarkBoolType   = 5;
	public static final byte PyMarkNoneType   = 6;
	public static final byte PyMarkStringType = 7;
	public static final byte PyMarkTupleType  = 8;
	public static final byte PyMarkListType   = 9;
	public static final byte PyMarkDictType   = 10;
  
  private byte mType = 0;
  private Object mData = null;
  
  public Integer asInt() { return (Integer)mData; }
  public Long asLong() { return (Long)mData; }
  public Float asFloat() { return (Float)mData; }
  public Double asDouble() { return (Double)mData; }
  public Boolean asBool() { return (Boolean)mData; }
  public Object asNone() { return null; }
  public String asString() { return (String)mData; }
  
  public boolean isCollection() {
    if ((mType == PyMarkTupleType) ||
        (mType == PyMarkListType)) {
      return true;    
    } else {
      return false;
    }
  }
  
  public PyMarkObject get(String key) {
    if (mType != PyMarkDictType) {
      return null;
    }
    
    String[] tokens = key.split("\\.");
    
    if (tokens.length == 1) { 
      return ((Hashtable<String, PyMarkObject>)mData).get(key);
    } else {
      PyMarkObject val = ((Hashtable<String, PyMarkObject>)mData).get(tokens[0]);
      String rest = "";
      for (int i = 1; i < tokens.length; i++) {
        rest = rest.concat(tokens[i]);
        rest = rest.concat(".");
      }
      rest = rest.substring(0, rest.length()-1);
      return val.get(rest);
    }
    
  }
  
  public PyMarkObject at(int index) {
    
    if (!isCollection()) {
      return null;
    }
    
    if ((mType == PyMarkTupleType) ||
        (mType == PyMarkListType)) {
      return ((PyMarkObject[])mData)[index];
    }
    
    return null;
  }
  
  public PyMarkObject(InputStream stream) throws IOException {
    
    mType = (byte)stream.read();
    
    byte[] data;
    byte[] len;
    long length;
    
    ByteBuffer bb;
    
    switch (mType) {
      case PyMarkIntType:
        data = new byte[4]; stream.read(data, 0, 4);
        bb = ByteBuffer.wrap(data); bb.order(ByteOrder.LITTLE_ENDIAN);
        mData = (Integer)bb.getInt();
      break;
      case PyMarkLongType:
        data = new byte[8]; stream.read(data, 0, 8);
        bb = ByteBuffer.wrap(data); bb.order(ByteOrder.LITTLE_ENDIAN);
        mData = (Long)bb.getLong();
      break;
      case PyMarkFloatType:
        data = new byte[4]; stream.read(data, 0, 4);
        bb = ByteBuffer.wrap(data); bb.order(ByteOrder.LITTLE_ENDIAN);
        mData = (Float)bb.getFloat();
      break;
      case PyMarkDoubleType:
        data = new byte[8]; stream.read(data, 0, 8);
        bb = ByteBuffer.wrap(data); bb.order(ByteOrder.LITTLE_ENDIAN);
        mData = (Double)bb.getDouble();
      break;
      case PyMarkBoolType:
        int val = stream.read();
        if (val == 1) { mData = (Boolean)true; }
        else if (val == 0) { mData = (Boolean)false; }
      break;
      case PyMarkNoneType:
        mData = null;
      break;
      case PyMarkStringType:
        len = new byte[8]; stream.read(len, 0, 8);
        bb = ByteBuffer.wrap(len); bb.order(ByteOrder.LITTLE_ENDIAN);
        length = bb.getLong();
        data = new byte[(int)length];
        stream.read(data, 0, (int)length);
        mData = new String(data);
      break;
      case PyMarkTupleType:
      case PyMarkListType:
        len = new byte[8]; stream.read(len, 0, 8);
        bb = ByteBuffer.wrap(len); bb.order(ByteOrder.LITTLE_ENDIAN);
        length = bb.getLong();
        mData = new PyMarkObject[(int)length];
        for (int i = 0; i < length; i++) {
          ((PyMarkObject[])mData)[i] = new PyMarkObject(stream);
        }
      break;
      case PyMarkDictType:
        len = new byte[8]; stream.read(len, 0, 8);
        bb = ByteBuffer.wrap(len); bb.order(ByteOrder.LITTLE_ENDIAN);
        length = bb.getLong();
        mData = new Hashtable<String, PyMarkObject>();
        for (int i = 0; i < length; i++) {
          PyMarkObject tuple = new PyMarkObject(stream);
          PyMarkObject key = tuple.at(0);
          PyMarkObject value = tuple.at(1);
          ((Hashtable<String, PyMarkObject>)mData).put(key.asString(), value);
        }
      break;
      default:
        mData = null;
      break;
    }
    
  }
  
  public static PyMarkObject UnpackObject(InputStream stream) throws IOException {
    return new PyMarkObject(stream);
  }
  
  public static PyMarkObject Unpack(String filename) throws IOException {
    FileInputStream f = new FileInputStream(filename);
    byte[] magictemp = new byte[]{'P','Y','M','A','R','K'};
    byte[] magic = new byte[6];
    f.read(magic);
    
    if (!Arrays.equals(magictemp, magic)) {
      return null;
    }
    
    byte version = (byte)f.read();
    
    if (version != 1) {
      return null;
    }
    
    PyMarkObject o = UnpackObject(f);
    
    f.close();
    
    return o;
  }
  
  public static void PackObject(OutputStream stream, PyMarkObject o) {
  
  }
  
  public static void Pack(String filename, PyMarkObject o) {
  
  }
  
}
