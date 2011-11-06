import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

@SuppressWarnings("rawtypes")
public class PyMarkLoader {

	private HashMap<String, Object> modules;
	public HashMap<String, Object> getModules() { return modules; }
	
	private ArrayList<String> moduleNames;
	public ArrayList<String> getModuleNames(){ return moduleNames; }
	
	private String path;
	public String getPath(){ return path; }
	
    public final static short LIST 		   = 1;
    public final static short LONG_LIST    = 2;
    public final static short DICT         = 3;
    public final static short LONG_DICT    = 4;
    public final static short TUPLE        = 5;
    public final static short LONG_TUPLE   = 6;
    public final static short STRING       = 7;
    public final static short LONG_STRING  = 8;
    public final static short INT          = 9;
    public final static short LONG         = 10;
    public final static short FLOAT        = 11;
    public final static short DOUBLE       = 12;
    public final static short REFERENCE    = 13;
    public final static short NONE         = 14;	
	
    private final String REF_PREFIX = "*PYMARK-REFERENCE*";
    
	@SuppressWarnings("unchecked")
	public PyMarkLoader(String _path)
	{
		path = _path;
		modules = new HashMap();
		moduleNames = new ArrayList<String>();
		
		LoadModuleNames();
		
		ClearLog();
		
		LogMsg("PyMarkLoader Constructed");
	}
	
	private void LogMsg(String msg)
	{
	    try {

		      String logLoc = path+"\\Logs\\java_loader.log";
		    	
		      BufferedWriter out = new BufferedWriter(new FileWriter(logLoc, true)); 
		      out.write(msg+"\n");
		      out.close();
		    } catch (IOException e) {
		      e.printStackTrace();
		    }
	}
	
	private void ClearLog()
	{
	    try {

		      String logLoc = path+"\\Logs\\java_loader.log";
		    	
		      BufferedWriter out = new BufferedWriter(new FileWriter(logLoc, false)); 
		      out.write("");
		      out.close();
		    } catch (IOException e) {
		      e.printStackTrace();
		    }
	}
	
	
    private boolean procDone(Process p) {
        try {
            @SuppressWarnings("unused")
			int v = p.exitValue();
            return true;
        }
        catch(IllegalThreadStateException e) {
            return false;
        }
    }	
	
	public void Compile()
	{	
		try{
		
		LogMsg("Compiling all modules...");
		
		String command = "python \""+path+"\\PyMark.py\"";
		
        Process p = Runtime.getRuntime().exec(command);

        // read the standard output of the command

        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));

        String output = "";
		while (!procDone(p)) {
			String s;
			while((s = stdInput.readLine()) !=null){
				output += (s+"\n");
			}
		}
		stdInput.close();
		
        LogMsg("\n>>>>>");
        LogMsg(output);
        LogMsg(">>>>>\n");
		
		}
		catch(Exception e)
		{
			LogMsg("ERROR: Could not compile modules: "+e.toString());
		}
	}
	
	public void CompileModules(List<String> names,String flags)
	{
		try{
			
			String moduleNames = " ";
			for (int i=0;i<names.size();i++)
			{
				moduleNames += (names.get(i) + " ");
			}
			
			LogMsg("Compiling modules"+moduleNames);			
			
			String command = "python \""+path+"\""+moduleNames+" "+flags;
			
	        Process p = Runtime.getRuntime().exec(command);

	        // read the standard output of the command

	        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));

	        String output = "";
			while (!procDone(p)) {
				String s;
				while((s = stdInput.readLine()) !=null){
					output += (s+"\n");
				}
			}
			stdInput.close();
			
	        LogMsg("\n>>>>>");
	        LogMsg(output);
	        LogMsg(">>>>>\n");
			
			}
			catch(Exception e)
			{
				LogMsg("ERROR: Could not compile modules: "+e.toString());
			}		
	}
	
	private void LoadModuleNames()
	{
		moduleNames.clear();
		
		String directory = path+"\\Compiled";
		File dir = new File(directory);
		String[] children = dir.list();
		
		if (children == null) {} 
		else
		{ 
			for (int i=0; i<children.length; i++)
			{
				String name = children[i];
				if (name.endsWith(".pm"))
					moduleNames.add(name.substring(0, name.length()-3));
			}
		}
	}
	
	public void Load()
	{
		LogMsg("Loading all modules...");
		LoadModuleNames();
		
		LoadModules(moduleNames);
	}
	public void LoadModules(ArrayList<String> names)
	{
		for (int i=0;i<names.size();i++)
		{
			try{
			
			String name = names.get(i);
			
			LogMsg("Loading module "+name+"...");
			
			String file = path+"\\Compiled\\"+name+".pm";
			FileInputStream fstream = new FileInputStream(file);
			DataInputStream stream = new DataInputStream(fstream);
			
			modules.put(name, BuildObject(stream));
			}
			catch(Exception e)
			{
				String name = names.get(i);
				LogMsg("ERROR: Could not loade module \""+name+"\" :"+e.toString());
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public Object BuildObject(DataInputStream stream) throws Exception
	{
		short type = readShort(stream);
		
		if ((type == LIST) || (type == TUPLE))
		{
			ArrayList retObject = new ArrayList();
			int len = readInt(stream);
			
			for (int i = 0;i<len;i++)
			{
				retObject.add(BuildObject(stream));
			}
			return retObject;
		}
		else if ((type == LONG_LIST) || (type == LONG_TUPLE))
		{
			ArrayList retObject = new ArrayList();
			long len = readLong(stream);
			
			for (long i = 0;i<len;i++)
			{
				retObject.add(BuildObject(stream));
			}
			return retObject;
		}
		else if (type == DICT)
		{
			HashMap retObject = new HashMap();
			int len = readInt(stream);
			
			for (int i=0;i<len;i++)
			{
				ArrayList keypair = (ArrayList)BuildObject(stream);
				retObject.put(keypair.get(0), keypair.get(1));
			}
			
			return retObject;
		}
		else if (type == LONG_DICT)
		{
			HashMap retObject = new HashMap();
			long len = readLong(stream);
			
			for (long i=0;i<len;i++)
			{
				ArrayList keypair = (ArrayList)BuildObject(stream);
				retObject.put(keypair.get(0), keypair.get(1));
			}
			
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
		else if(type == LONG)
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
		else if (type == REFERENCE)
		{
			ArrayList retObject = new ArrayList();
			int len = readInt(stream);
			
			retObject.add(REF_PREFIX);
			for (int i = 0;i<len;i++)
			{
				retObject.add(BuildObject(stream));
			}
			return retObject;
		}
		else if (type == NONE)
		{
			return null;
		}
		else
		{
			throw new Exception("ERROR: Unknown type index: "+((Short)type).toString()+" perhaps a badly formed .pm file?");
		}
		
	}
	
	private double readDouble(DataInputStream stream) throws IOException
	{
		double p1 = stream.readDouble();
		return p1;
	}
	
	public void BuildReferences()
	{
        for ( String key : modules.keySet() )
        {
        	modules.put(key, FollowReferences(modules.get(key)));
        }
	}
	
	@SuppressWarnings("unchecked")
	public Object FollowReferences(Object o)
	{
		if (o == null)
		{
			return null;
		}
		if (o.getClass() == ArrayList.class) 
		{		
			/* if is reference */
			if (((ArrayList) o).get(0) == REF_PREFIX)
			{
				((ArrayList) o).remove(0); // Pop the reference off the list.
				o = Get((ArrayList) o,modules);
			}
			else
			{
				/* Follow all references for all of its objects */
				for(int i=0;i<((ArrayList)o).size();i++)
				{
					((ArrayList)o).set(i, FollowReferences(((ArrayList) o).get(i)) );
				}
			}
		}
		else if (o.getClass() == HashMap.class) 
		{
			/* Follow all references for all of its objects */
			for ( Object key : ((HashMap) o).keySet() )
			{
				 ((HashMap) o).put(key, FollowReferences(((HashMap) o).get(key)));
			}
		}
		
		return o;
	}
	
	public Object Get(String reference)
	{
		return Get(reference,modules);
	}
	
	@SuppressWarnings("unchecked")
	public Object Get(String reference,Object domain)
	{
		ArrayList linkList = new ArrayList();
		
		String[] splits = reference.split("\\.");
		for(int i=0;i<splits.length;i++)
		{	
			String s = splits[i];
			
			try{
				Integer.parseInt(s);
				linkList.add(Integer.parseInt(s));
			}
			catch (Exception e)
			{
				linkList.add(s);
			}
		}
		//Collections.reverse(linkList);
		
		return Get(linkList,domain);
	}
	
	public Object Get(ArrayList linkList,Object domain)
	{
		Object nextKey = linkList.remove(0);
		Object nextObject = null;
		
		if (domain.getClass() == HashMap.class)
		{
			nextObject = ((HashMap)domain).get(nextKey); 
		}
		else if (domain.getClass() == ArrayList.class)
		{
			nextObject = ((ArrayList)domain).get((Integer)nextKey);
		}
		
		if (linkList.size() == 0)
		{
			return nextObject;
		}
		else
		{
			return Get(linkList,nextObject);
		}
	}
	
	
	/* Functions for reading in values */
	
	private short readShort(DataInputStream stream) throws IOException
	{
		return (short)stream.read();
	}
	
	private int readInt(DataInputStream stream) throws IOException
	{
		short p1 = (short)stream.read();
		short p2 = (short)stream.read();
		
		return (p1 << 8) + p2;
	}
	
	private long readLong(DataInputStream stream) throws IOException
	{
		short p1 = (short)stream.read();
		short p2 = (short)stream.read();
		short p3 = (short)stream.read();
		short p4 = (short)stream.read();
		
		return (p1 << 24) + (p2 << 16) + (p3 << 8) + (p4);
	}
	
	private String readString(DataInputStream stream) throws IOException
	{
		int len = readInt(stream);
		String retString = "";
		for (int i = 0;i<len;i++)
		{
			retString += (char)stream.read();
		}
		return retString;
	}
	
	private String readLongString(DataInputStream stream) throws IOException
	{
		long len = readInt(stream);
		String retString = "";
		for (long i = 0;i<len;i++)
		{
			retString += (char)stream.read();
		}
		return retString;
	}
	
	private float readFloat(DataInputStream stream) throws IOException
	{
		float p1 = stream.readFloat();
		return p1;
	}	
}
