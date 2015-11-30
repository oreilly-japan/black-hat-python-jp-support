' Adapted from:
' http://gallery.technet.microsoft.com/scriptcenter/03f21031-07de-4a26-9a04-4871cd425870

strComputer = "." 
Set objWMIService = GetObject("winmgmts:" _ 
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_OperatingSystem") 
 
For Each objOperatingSystem in colSettings  
    Wscript.StdOut.Write "OS Name: " & objOperatingSystem.Name & vbCrLf
    Wscript.StdOut.Write "Version: " & objOperatingSystem.Version & vbCrLf
    Wscript.StdOut.Write "Service Pack: " & _ 
        objOperatingSystem.ServicePackMajorVersion _ 
            & "." & objOperatingSystem.ServicePackMinorVersion & vbCrLf
    Wscript.StdOut.Write "OS Manufacturer: " & objOperatingSystem.Manufacturer & vbCrLf
    Wscript.StdOut.Write "Windows Directory: " & _ 
        objOperatingSystem.WindowsDirectory & vbCrLf
    Wscript.StdOut.Write "Locale: " & objOperatingSystem.Locale & vbCrLf
    Wscript.StdOut.Write "Available Physical Memory: " & _ 
        objOperatingSystem.FreePhysicalMemory & vbCrLf
    Wscript.StdOut.Write "Total Virtual Memory: " & _ 
        objOperatingSystem.TotalVirtualMemorySize & vbCrLf
    Wscript.StdOut.Write "Available Virtual Memory: " & _ 
        objOperatingSystem.FreeVirtualMemory & vbCrLf
    Wscript.StdOut.Write "Size stored in paging files: " & _ 
        objOperatingSystem.SizeStoredInPagingFiles & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_ComputerSystem") 
 
For Each objComputer in colSettings  
    Wscript.StdOut.Write "System Name: " & objComputer.Name & vbCrLf
    Wscript.StdOut.Write "System Manufacturer: " & objComputer.Manufacturer & vbCrLf
    Wscript.StdOut.Write "System Model: " & objComputer.Model & vbCrLf
    Wscript.StdOut.Write "Time Zone: " & objComputer.CurrentTimeZone & vbCrLf
    Wscript.StdOut.Write "Total Physical Memory: " & _ 
        objComputer.TotalPhysicalMemory & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_Processor") 
 
For Each objProcessor in colSettings  
    Wscript.StdOut.Write "System Type: " & objProcessor.Architecture & vbCrLf
    Wscript.StdOut.Write "Processor: " & objProcessor.Description & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_BIOS") 
 
For Each objBIOS in colSettings  
    Wscript.StdOut.Write "BIOS Version: " & objBIOS.Version & vbCrLf
Next
