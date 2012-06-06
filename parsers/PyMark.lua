require "struct"

pymark_int_type     = 1
pymark_long_type    = 2
pymark_float_type   = 3
pymark_double_type  = 4
pymark_bool_type    = 5
pymark_none_type    = 6
pymark_string_type  = 7
pymark_tuple_type   = 8
pymark_list_type    = 9
pymark_dict_type    = 10

pymark_magic = "PYMARK"
pymark_version = 1

function pymark_unpack_object(f)
  local t = struct.unpack("b", f:read(1))
  
  if t == pymark_int_type then return struct.unpack("i", f:read(4))
  elseif t == pymark_long_type then return struct.unpack("l", f:read(8))
  elseif t == pymark_float_type then return struct.unpack("f", f:read(4))
  elseif t == pymark_double_type then return struct.unpack("d", f:read(8))
  
  elseif t == pymark_bool_type then
    if struct.unpack("b", f:read(1)) then return true
    else return false end
    
  elseif t == pymark_none_type then return nil
  
  elseif t == pymark_string_type then
    local length = struct.unpack("l", f:read(8))
    return f:read(length)
    
  elseif t == pymark_tuple_type or 
         t == pymark_list_type then
    local length = struct.unpack("l", f:read(8))
    local items = {}
    for i = 1, length do
      items[i] = pymark_unpack_object(f)
    end
    return items
    
  elseif t == pymark_dict_type then
    local length = struct.unpack("l", f:read(8))
    local items = {}
    for i = 1, length do
      tuple = pymark_unpack_object(f)
      items[tuple[1] or "None"] = tuple[2]
    end
    return items
    
  else error(string.format("Unknown TypeId %i", t))
  end
end

function pymark_unpack(filename)
  
  local f = io.open(filename, "rb")
  
  local magic = f:read(#pymark_magic)
  if magic ~= pymark_magic then
    error("Invalid magic number for pymark file")
  end
  
  local version = f:read(1)
  if string.byte(version) ~= pymark_version then
    error("Invalid version number for pymark file")
  end
  
  local obj = pymark_unpack_object(f)
  io.close(f)
  
  return obj
  
end

function pymark_pack_object(f, obj)
  
  local function is_integer(x)
    return math.floor(x) == x
  end
  
  local function is_array(x)
    return x[1]
  end
  
  if type(obj) == "number" and is_integer(obj) then return f:write(struct.pack("bi", pymark_int_type, obj))
  elseif type(obj) == "number" then return f:write(struct.pack("bd", pymark_double_type, obj))
  
  elseif type(obj) == "boolean" then
    if obj then f:write(struct.pack("bb", pymark_bool_type, 1))
    else f:write(struct.pack("bb", pymark_bool_type, 0)) end
    
  elseif type(obj) == "nil" then f:write(struct.pack("b", pymark_none_type))
  
  elseif type(obj) == "string" then
    f:write(struct.pack("bl", pymark_string_type, #obj))
    f:write(obj)
    
  elseif type(obj) == "table" and is_array(obj) then
    f:write(struct.pack("bl", pymark_list_type, #obj))
    for k, v in pairs(obj) do pymark_pack_object(f, v) end
    
  elseif type(obj) == "table" then
    f:write(struct.pack("bl", pymark_dict_type, #obj))
    for k, v in pairs(obj) do pymark_pack_object(f, {k, v}) end
    
  else error(string.format("Unknown Type %s", type(obj)))
  end
end

function pymark_pack(filename, obj)
  local f = io.open(filename, "wb")
  f:write(pymark_magic)
  f:write(string.char(pymark_version))
  pymark_pack_object(f, obj)
  io.close(f)
end

