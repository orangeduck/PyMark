using System;
using System.Collections;
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
///         + So instead we are simply using a ArrayList. Which works ok... I did not want to provide a library of propriatory classes for each langauge.
///     3. References
///         + As you may have expected, C# really doesn't like the idea of data loaded at runtime being able to point somewhere in memory.
///         + Of course it isn't as simple as that, but that is in essence the problem.
///         + So I've added a middle-man class called "Reference", which can be used to lookup data elsewhere in the module without large amounts of data copying.
///         + Though it is fairly hard to actually edit data inside Hashtables and ArrayLists - so good luck with making much use of it anyway.
///         
/// </remarks>
class PyMarkLoader
{

    String path;
    /// <summary>
    /// The path to the directory in which PyMark.py is located.
    /// </summary>
    public String Path
    {
        get { return path;}
        set {path = value;}
    }

    /// <summary>
    /// The names of modules possible to load (in the Compiled directory).
    /// </summary>
    public ArrayList ModuleNames
    {
        get
        {
            List<String> files = Directory.GetFiles(Path + "\\compiled").ToList();
            ArrayList names = new ArrayList();
            foreach (String file in files)
            {
                names.Add(System.IO.Path.GetFileNameWithoutExtension(file));
            }
            return names;
        }
    }

    Hashtable modules;
    /// <summary>
    /// A Dictionary of the modules currently loaded.
    /// </summary>
    public Hashtable Modules
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
    public const short NONE         = 14;

    /// <summary>
    /// Class representing an internal unlinked reference.
    /// </summary>
    public class Reference
    {
        public Queue linkList;

        public Reference(Queue _linkList, Hashtable _domain)
        {
            linkList = _linkList;
        }
    }

    /// <summary>
    /// Builds a PyMarkLoader.
    /// </summary>
    /// <param name="_path">Path to the PyMark directory (where PyMark.py is located).</param>
    public PyMarkLoader(String _path)
    {
        path = _path;
        modules = new Hashtable();

        ClearLog();
        LogMsg("PyMarkLoader constructed");
    }

    void LogMsg(String s)
    {
        StreamWriter sw;
        sw = File.AppendText(path + @"\Logs\Csharp_loader.log");
        sw.WriteLine(s);
        sw.Close();
    }

    /// <summary>
    /// Clears the log located at: \Logs\Csharp_Loader.log
    /// </summary>
    public void ClearLog()
    {
        StreamWriter sw;
        sw = File.CreateText(path + @"\Logs\Csharp_loader.log");
        sw.WriteLine("");
        sw.Close();
    }

    /// <summary>
    /// Recompiles the module source files by running PyMark.py, assumes that python is installed and the PATH variable is set correctly.
    /// </summary>
    public void Compile()
    {
        String output;
        try
        {
            LogMsg("Compiling all modules...");

            Process p = new Process();
            p.StartInfo.FileName = "python";
            p.StartInfo.Arguments = "\"" + path + "\\PyMark.py\"";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();

            output = p.StandardOutput.ReadToEnd();

            LogMsg("\n>>>>>");
            LogMsg(output);
            LogMsg(">>>>>\n");
        }
        catch (Exception e)
        {
            String errorString = "ERROR: Could not recompile source files: " + e.ToString();
            LogMsg(errorString);
            output = errorString;
        }
    }

    /// <summary>
    /// Recompiles a list of modules by running PyMark.py, assumes that python is installed and the PATH variable is set correctly.
    /// </summary>
    /// <param name="modules">Modules to be compiled.</param>
    /// <param name="flags">Flag string to send to PyMark.py</param>
    public void CompileModules(ArrayList modules,String flags)
    {
        String output;

        String modulesString = "";
        foreach (String name in modules)
        {
            modulesString += " "+name;
        }
        
        try
        {
            LogMsg("Compiling modules: " + modulesString + "...");

            Process p = new Process();
            p.StartInfo.FileName = "python";
            p.StartInfo.Arguments = "\"" + path + "\\PyMark.py\" " + modulesString + " " + flags;
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardOutput = true;
            p.Start();

            output = p.StandardOutput.ReadToEnd();
            LogMsg("Module souce files recompiled");

            LogMsg("\n>>>>>");
            LogMsg(output);
            LogMsg(">>>>>\n");
        }
        catch (Exception e)
        {
            String errorString = "ERROR: Could not recompile source files: " + e.ToString();
            LogMsg(errorString);
            output = errorString;
        }
    }

    /// <summary>
    /// Loads a list of modules.
    /// </summary>
    /// <param name="name">Names of module to load</param>
    public void LoadModules(ArrayList names)
    {
        foreach (String name in names)
        {
            LogMsg("Loading Module \"" + name + "\"...");
            if (!ModuleNames.Contains(name))
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
    }

    /// <summary>
    /// Loads all modules
    /// </summary>
    public void Load()
    {
        LogMsg("Loading All Modules...");
        LoadModules(ModuleNames);
    }


    /// <summary>
    /// Links all Reference objects in the modules to where they point to.
    /// </summary>
    public void LinkReferences()
    {
        object[] keyList = new object[modules.Count];
        modules.Keys.CopyTo(keyList, 0);
        for (int i = 0; i < keyList.Length; i++)
        {
            var key = keyList[i];
            modules[key] = FollowReferences(modules[key]);
        }
    }

    private Object FollowReferences(Object o)
    {
        if (o is ArrayList)
        {
            ArrayList castDown = (ArrayList)o;

            for (int i = 0; i < castDown.Count; i++)
            {
                castDown[i] = FollowReferences(castDown[i]);
            }

            return castDown;
        }
        else if (o is Hashtable)
        {
            Hashtable castDown = (Hashtable)o;
            object[] keyList = new object[castDown.Count];
            castDown.Keys.CopyTo(keyList, 0);
            for (int i = 0; i < keyList.Length; i++)
            {
                var key = keyList[i];
                castDown[key] = FollowReferences(castDown[key]);
            }

            return castDown;
        }
        else if (o is Reference)
        {
            Reference o_ref = (Reference)o;
            return GetLinkList(o_ref.linkList,modules);
        }
        else
        {
            return o;
        }

    }

    private Object CompileObject(FileStream stream)
    {

        short type = readShort(stream);

        if ((type == LIST) || (type == TUPLE))
        {
            var retObject = new ArrayList();
            int len = readInt(stream);

            for (int i = 0; i < len; i++)
            {
                retObject.Add(CompileObject(stream));
            }

            return retObject;
        }
        else if ((type == LONG_LIST) || (type == LONG_TUPLE))
        {
            var retObject = new ArrayList();
            long len = readLong(stream);

            for (long i = 0; i < len; i++)
            {
                retObject.Add(CompileObject(stream));
            }

            return retObject;
        }
        else if (type == DICT)
        {
            var retObject = new Hashtable();
            int len = readInt(stream);

            var pairList = new ArrayList();
            for (int i = 0; i < len; i++)
            {
                pairList.Add(CompileObject(stream));
            }
            foreach (ArrayList item in pairList)
            {
                var listItem = item;
                retObject[listItem[0]] = listItem[1];
            }

            return retObject;
        }
        else if (type == LONG_DICT)
        {
            var retObject = new Hashtable();
            long len = readLong(stream);

            var pairList = new ArrayList();
            for (long i = 0; i < len; i++)
            {
                pairList.Add(CompileObject(stream));
            }
            foreach (ArrayList item in pairList)
            {
                var listItem = (ArrayList)item;
                retObject[listItem[0]] = listItem[1];
            }

            return retObject;
        }
        else if (type == REFERENCE)
        {
            Queue refList = new Queue();
            int len = readInt(stream);
            for (int i = 0; i < len; i++)
            {
                refList.Enqueue(CompileObject(stream));
            }
            return new Reference(refList, modules); 
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
        else if (type == NONE)
        {
            return null;
        }
        else
        {
            throw new Exception("Unidentified type index:" + type + " Perhaps a badly formed .pm file?");
        }
    }

    public Object Get(String reference)
    {
        return Get(reference, modules);
    }

    public Object Get(String reference, Object domain)
    {
        Queue linkList = new Queue();
        string[] splits = reference.Split(".".ToCharArray());
        foreach (string part in splits)
        {
            int output;
            if (int.TryParse(part, out output))
            {
                linkList.Enqueue(output);
            }
            else
            {
                linkList.Enqueue(part);
            }
        }

        return GetLinkList(linkList, domain);
    }

    public Object GetLinkList(Queue linkList, Object domain)
    {

        Object key = linkList.Dequeue();

        Object nextObject;
        if (key is String)
        {
            Hashtable currentObject = (Hashtable)domain;
            nextObject = currentObject[(String)key];
        }
        else if (key is int)
        {
            ArrayList currentObject = (ArrayList)domain;
            nextObject = currentObject[(int)key];
        }
        else
        {
            return null;
        }

        if (linkList.Count > 0)
        {
            return GetLinkList(linkList, nextObject);
        }
        else
        {
            return nextObject;
        }
    }

    /* Functions for parsing certain types from the file mainly based on how many bytes they are. */

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

        long ret = (p1 << 24) + (p2 << 16) + (p3 << 8) + (p4);

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
