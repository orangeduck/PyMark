using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.IO;

/// <summary>
/// A C# Class that loads compiled PyMark data into native data structures.
/// </summary>
/// <remarks>
/// There are a couple of things to note here about the C# implementation:
/// 
///     1. Not type Strong
///         + Because this is dynamic construction of objects, we don't know the types at compile time. So it isn't (easily) possible to construct type data at run time. Not in a useful way anyway.
///         + This means that the whole thing isn't type strong. Which isn't so bad I suppose.
///         + Either way - some smart downcasts by the user programmer should work fine. He/She should have some idea of the data that is coming in as.
///     2. No real implementation of a Tuple.
///         + C# supports things which represent pairs, but a N-Dimensional Tuple is not embedded in the language - and I only wanted to use native types where possible.
///         + So instead we are simply using a List of Objects. Which works ok... I did not want to provide a library of propriatory classes for each langauge.
///     3. References
///         + Man I don't even know if its working or if I've just gone and done a clone rather than a reference. Something happens anyway.
///         + Either way it was a bitch - because enumerating over dictionaries isn't allow if you're planning on changing the values.
///         + If you prefer, just don't call the "BuildReferences" function and you'll have pseudo references in the form of Lists. It was automating the construction where things got complicated.
///         + I'm thinking at some point it might be worth refactoring anyway - adding Reference objects to a list in the class - then making parts of the modules point at that (keep it explicit we want these things to not be value variables) 
///         
/// </remarks>
class PyMarkLoader
{

    String path;
    List<String> moduleNames;
    Dictionary<String,Object> modules;
    String log;

    /// <summary>
    /// A Log of the PyMark Loader.
    /// </summary>
    public String Log
    {
        get { return log; }
    }

    /// <summary>
    /// The names of modules possible to load.
    /// </summary>
    public List<String> ModuleNames
    {
        get { return moduleNames; }
    }
    /// <summary>
    /// A Dictionary of the modules currently loaded.
    /// </summary>
    public Dictionary<String, Object> Modules
    {
        get { return modules;  }
    }

    /// <summary>
    /// PyMark type indicies
    /// </summary>
    public const short LIST 		= 1;
    public const short LONG_LIST    = 2;
    public const short DICT         = 3;
    public const short LONG_DICT    = 4;
    public const short TUPLE        = 5;
    public const short LONG_TUPLE   = 6;
    public const short STRING       = 7;
    public const short LONG_STRING  = 8;
    public const short INT          = 9;
    public const short LONG         = 10;
    public const short FLOAT        = 11;
    public const short DOUBLE       = 12;
    public const short REFERENCE    = 13;

    /// <summary>
    /// Builds the PyMarkLoader object.
    /// </summary>
    /// <param name="_path">Path to the PyMark directory (Where PyMark.py is located and the .py modules)</param>
    public PyMarkLoader(String _path)
    {
        path = _path;
        LoadModuleNames();
        modules = new Dictionary<String, Object>();
        LogMsg("PyMarkLoader constructed");
    }

    /// <summary>
    /// Writes a string to the internal log.
    /// </summary>
    /// <param name="s">String to write to log</param>
    void LogMsg(String s)
    {
        log += s + "\n";
    }

    /// <summary>
    /// Clears the internal log data.
    /// </summary>
    public void ClearLog()
    {
        log = "";
    }

    class Reference
    {
        public Queue<Object> linkList;

        public Reference(Queue<Object> _linkList)
        {
            linkList = _linkList;
        }
    }

    /// <summary>
    /// Reloades which modules are in the compiled directory avaliable to load.
    /// </summary>
    void LoadModuleNames()
    {
        List<String> files = Directory.GetFiles(path + "\\compiled").ToList();

        moduleNames = new List<String>();
        foreach (String file in files)
        {
            moduleNames.Add(Path.GetFileNameWithoutExtension(file));
        }

        LogMsg("Module Names Reloaded");
    }

    /// <summary>
    /// Recompiles the module .py source files by running PyMark.py,
    /// Assumes that python is installed and the PATH variable is set correctly.
    /// </summary>
    public String Compile()
    {
        String output;
        try
        {
            Process p = new Process();
            p.StartInfo.FileName = "python";
            p.StartInfo.Arguments = "\"" + path + "\\PyMark.py\"";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();

            output = p.StandardOutput.ReadToEnd();
            LogMsg("Module souce files recompiled");
        }
        catch (Exception e)
        {
            String errorString = "ERROR: Could not recompile source files: " + e.ToString();
            LogMsg(errorString);
            output = errorString;
        }

        /* Reload module names after recompile */
        LoadModuleNames();

        return output;
    }

    /// <summary>
    /// Recompiles a list of module .py source files by running PyMark.py,
    /// Assumes that python is installed and the PATH variable is set correctly.
    /// </summary>
    public String CompileModules(List<String> modules,String flags)
    {
        String output;

        String modulesString = "";
        foreach (String name in modules)
        {
            modulesString += " "+name;
        }
        
        try
        {
            Process p = new Process();
            p.StartInfo.FileName = "python";
            p.StartInfo.Arguments = "\"" + path + "\\PyMark.py\" " + modulesString + " " + flags;
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();

            output = p.StandardOutput.ReadToEnd();
            LogMsg("Module souce files recompiled");
        }
        catch (Exception e)
        {
            String errorString = "ERROR: Could not recompile source files: " + e.ToString();
            LogMsg(errorString);
            output = errorString;
        }

        /* Reload module names after recompile */
        LoadModuleNames();

        return output;
    }

    /// <summary>
    /// Loads an individual module. Will replace any existing module with the same name.
    /// </summary>
    /// <param name="name">name of the module to load</param>
    public void LoadModule(String name)
    {
        LogMsg("Loading Module \"" + name + "\"...");
        if (!moduleNames.Contains(name))
        {
            LogMsg("ERROR: Module \"" + name + "\" not in module names list!");
            return;
        }
        FileStream stream;
        try
        {
            String filename = "" + path + "\\compiled\\" + name + ".pm";
            stream = new FileStream(filename, FileMode.Open, FileAccess.Read);
            
        }
        catch (Exception e)
        {
            LogMsg("ERROR: Could not load data for module \"" + name + "\": " + e.ToString() + "");
            return;
        }

        Object module = CompileObject(stream);

        stream.Close();

        modules[name] = module;
    }

    /// <summary>
    /// Loads all modules
    /// </summary>
    public void Load()
    {
        LogMsg("Loading All Modules...");
        foreach (String name in moduleNames)
        {
            LoadModule(name);
        }
    }

    private Object FollowReference(Object o, List<Object> links)
    {
        return new Object();
    }

    /// <summary>
    /// Compiles the next object in the data stream.
    /// </summary>
    /// <remarks>
    /// Notice that the objects returned are of the class Object. This is because their type cannot be determined at compile time.
    /// It is expected that user programmers will have some idea of the types of the data coming in and can downcast appropriately.
    /// </remarks>
    /// <param name="stream">current data stream</param>
    /// <returns>Compiled Object</returns>
    private Object CompileObject(FileStream stream)
    {

        short type = readShort(stream);

        if ((type == LIST) || (type == TUPLE))
        {
            List<Object> retObject = new List<Object>();
            int len = readInt(stream);
            
            for (int i = 0; i < len; i++)
            {
                retObject.Add(CompileObject(stream));
            }

            return retObject;
        }
        else if ((type == LONG_LIST) || (type == LONG_TUPLE))
        {
            var retObject = new List<Object>();
            long len = readLong(stream);

            for (long i = 0; i < len; i++)
            {
                retObject.Add(CompileObject(stream));
            }

            return retObject;
        }
        else if (type == DICT)
        {
            var retObject = new Dictionary<Object, Object>();
            int len = readInt(stream);

            var pairList = new List<Object>();
            for (int i = 0; i < len; i++)
            {
                pairList.Add(CompileObject(stream));
            }
            foreach (Object item in pairList)
            {
                var listItem = (List<Object>)item;
                retObject[listItem[0]] = listItem[1];
            }

            return retObject;
        }
        else if (type == LONG_DICT)
        {
            var retObject = new Dictionary<Object, Object>();
            long len = readLong(stream);

            var pairList = new List<Object>();
            for (long i = 0; i < len; i++)
            {
                pairList.Add(CompileObject(stream));
            }
            foreach (Object item in pairList)
            {
                var listItem = (List<Object>)item;
                retObject[listItem[0]] = listItem[1];
            }

            return retObject;
        }
        else if (type == REFERENCE)
        {
            Queue<Object> refList = new Queue<Object>();
            int len = readInt(stream);

            for (int i = 0; i < len; i++)
            {
                refList.Enqueue(CompileObject(stream));
            }

            Reference retRef = new Reference(refList);
            Object retObject = new Object();
            retObject = retRef;

            return retObject;
        }
        else if (type == STRING)
        {
            return readString(stream);
        }
        else if (type == LONG_STRING)
        {
            return readLongString(stream);
        }
        else if (type == INT)
        {
            return readInt(stream);
        }
        else if (type == LONG)
        {
            return readLong(stream);
        }
        else if (type == FLOAT)
        {
            return readFloat(stream);
        }
        else if (type == DOUBLE)
        {
            return readDouble(stream);
        }
        else
        {
            throw new Exception("Unidentified type index:" + type + " Perhaps a badly formed .pm file?");
        }
    }

    public void BuildReferences()
    {
        Dictionary<String, Object> newModules = new Dictionary<String, Object>();
        foreach (String key in modules.Keys)
        {
            newModules[key] = FollowReferences(modules[key]);
        }
        modules = newModules;
    }

    private Object FollowReferences(Object o)
    {
        if (o is List<Object>)
        {
            List<Object> castDown = (List<Object>)o;

            for (int i = 0; i < castDown.Count; i++)
            {
                castDown[i] = FollowReferences(castDown[i]);
            }

            return castDown;
        }
        else if (o is Dictionary<Object, Object>)
        {
            Dictionary<Object, Object> castDown = (Dictionary<Object, Object>)o;
            Dictionary<Object, Object> newDict = new Dictionary<Object, Object>();

            foreach (String key in castDown.Keys)
            {
                newDict[key] = FollowReferences(castDown[key]);
            }

            return newDict;
        }
        else if (o is Reference)
        {
            Reference castDown = (Reference)o;

            // The first step down from modules must be done here, because it uses a Dictionary<String,Object> rather than a Dictionary<Object,Object> - and that fucks up the casts.
            Object nextObject = modules[(String)castDown.linkList.Dequeue()];
            o = BuildReference(castDown.linkList, nextObject);

            return o;
        }
        else
        {
            return o;
        }

    }

    private Object BuildReference(Queue<Object> linkList, Object o)
    {
        Object key = linkList.Dequeue();

        Object nextObject;
        if (key is String)
        {
            Dictionary<Object, Object> currentObject = (Dictionary<Object, Object>)o;
            nextObject = currentObject[(String)key];
        }
        else if (key is int)
        {
            List<Object> currentObject = (List<Object>)o;
            nextObject = currentObject[(int)key];
        }
        else
        {
            // ERROR
            nextObject = 0;
        }

        if (linkList.Count > 0)
        {
            return BuildReference(linkList, nextObject);
        }
        else
        {
            return nextObject;
        }
    }

    /* Functions for parsing certain types from the file mainly simply based on how many bytes they are. */

    private short readShort(FileStream stream)
    {
        short ret = (short)stream.ReadByte();
        return ret;
    }

    private int readInt(FileStream stream)
    {
        byte p1 = (byte)stream.ReadByte();
        byte p2 = (byte)stream.ReadByte();

        int ret = (p1 << 8) + (p2);

        return ret;
    }

    private long readLong(FileStream stream)
    {
        byte p1 = (byte)stream.ReadByte();
        byte p2 = (byte)stream.ReadByte();
        byte p3 = (byte)stream.ReadByte();
        byte p4 = (byte)stream.ReadByte();

        long ret = (p1 << 32) + (p2 << 16) + (p3 << 8) + (p4);

        return ret;
    }

    private string readString(FileStream stream)
    {
        int len = readInt(stream);
        string retString = "";
        for (int i = 0; i < len; i++)
        {
            retString += Convert.ToChar((short)stream.ReadByte());
        }

        return retString;
    }

    private string readLongString(FileStream stream)
    {
        long len = readLong(stream);
        string retString = "";
        for (long i = 0; i < len; i++)
        {
            retString += Convert.ToChar((short)stream.ReadByte());
        }

        return retString;
    }

    private float readFloat(FileStream stream)
    {
        byte p1 = (byte)stream.ReadByte();
        byte p2 = (byte)stream.ReadByte();
        byte p3 = (byte)stream.ReadByte();
        byte p4 = (byte)stream.ReadByte();

        float ret = BitConverter.ToSingle(new byte[] { p4, p3, p2, p1 }, 0);

        return ret;
    }

    private double readDouble(FileStream stream)
    {
        byte p1 = (byte)stream.ReadByte();
        byte p2 = (byte)stream.ReadByte();
        byte p3 = (byte)stream.ReadByte();
        byte p4 = (byte)stream.ReadByte();
        byte p5 = (byte)stream.ReadByte();
        byte p6 = (byte)stream.ReadByte();
        byte p7 = (byte)stream.ReadByte();
        byte p8 = (byte)stream.ReadByte();

        double ret = BitConverter.ToDouble(new byte[] { p8, p7, p6, p5, p4, p3, p2, p1 }, 0);

        return ret;
    }

}
