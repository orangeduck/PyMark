import java.util.Arrays;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

import java.nio.channels.FileChannel;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

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
  
  public byte type() { return mType; }
  
  public boolean isCollection() {
    if ((mType == PyMarkTupleType) ||
        (mType == PyMarkListType) ||
        (mType == PyMarkDictType)) {
      return true;    
    } else {
      return false;
    }
  }
  
  public int length() {
    if (isCollection()) {
      return ((PyMarkObject[])mData).length;
    } else {
      return -1;
    }
  }
  
  public PyMarkObject get(String key) {
    if (mType != PyMarkDictType) {
      return null;
    }
    
    String[] tokens = key.split("\\.");
    
    PyMarkObject val = null;
    
    for(int i = 0; i < length(); i++) {
      
      PyMarkObject tuple_key = at(i).at(0);
      String tuple_str = tuple_key.asString();
      if (tuple_str.equals(tokens[0])) {
        val = at(i).at(1);
      }
      
    }
    
    if (tokens.length == 1) {
      return val;
    } else {
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
    
    return ((PyMarkObject[])mData)[index];
  }
  
  public PyMarkObject(ByteBuffer bb) throws IOException {
    
    mType = bb.get();
    
    switch (mType) {
      case PyMarkIntType: mData = (Integer)bb.getInt(); break;
      case PyMarkLongType: mData = (Long)bb.getLong(); break;
      case PyMarkFloatType: mData = (Float)bb.getFloat(); break;
      case PyMarkDoubleType: mData = (Double)bb.getDouble(); break;
      case PyMarkBoolType:
        byte val = (byte)bb.getChar();
        if (val == 1) { mData = (Boolean)true; }
        else if (val == 0) { mData = (Boolean)false; }
      break;
      case PyMarkNoneType: mData = null; break;
      case PyMarkStringType:
        byte[] str = new byte[(int)bb.getLong()];
        bb.get(str);
        mData = new String(str);
      break;
      case PyMarkTupleType:
      case PyMarkListType:
      case PyMarkDictType:
        long length = bb.getLong();
        mData = new PyMarkObject[(int)length];
        for (int i = 0; i < length; i++) {
          ((PyMarkObject[])mData)[i] = new PyMarkObject(bb);
        }
      break;
      default: throw new IOException("Unknown typeId " + (int)mType);
    }
    
  }
  
  public static PyMarkObject UnpackObject(ByteBuffer bb) throws IOException {
    return new PyMarkObject(bb);
  }
  
  public static PyMarkObject Unpack(String filename) throws IOException {
    FileChannel channel = new FileInputStream(filename).getChannel();
    
    ByteBuffer bb = ByteBuffer.allocate((int)channel.size());
    bb.order(ByteOrder.LITTLE_ENDIAN);
    
    channel.read(bb);
    bb.rewind();
    
    byte[] magiccmp = new byte[]{'P','Y','M','A','R','K'};
    byte[] magic = new byte[6];
    bb.get(magic);
    
    if (!Arrays.equals(magiccmp, magic)) { throw new IOException("Invalid Magic Number"); }
    
    byte version = bb.get();
    if (version != 1) { throw new IOException("Invalid Version"); }
    
    PyMarkObject obj = UnpackObject(bb);
    
    channel.close();
    
    return obj;
  }
  
  public static void PackObject(ByteBuffer bb, PyMarkObject o) {
  
  }
  
  public static void Pack(String filename, PyMarkObject o) {
  
  }
  
}
